from django.shortcuts import render
import requests

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser

from django.http import JsonResponse, HttpResponseRedirect


from .blockchain import Blockchain
from . import schnorr

import json
import time
import random


blockchain = Blockchain()
"""
    TODO:

        - node identifier -> public key
        - uncomment forward TX - done
        - make wait random time and test for block forwards and timing ?
        - register for both nodes and test for communications

        - multi threading for forward tx and continue ?
        
        - show log

"""
@api_view(['GET'])
def api(request):
    response = {
        "/mine": "mine current block",
        "/lbh": "request last block hash",
        "/new_block": "Send new mined block",
        "/new_tx": "create new transaction",
        "/full_chain": "request full block chain",
        "/block/<int:block_num>": "retrieve block of number block_num",
        "/register_nodes": "Register a new Node",
        "/consensus": "Resolution of chain with Nodes",
    }

    return JsonResponse(response)

@api_view(['GET'])
def mine(request):
    # We run the proof of work algorithm to get the next proof...
    last_block = blockchain.last_block
    proof = blockchain.proof_of_work(last_block)

    # We must receive a reward for finding the proof.
    # The sender is "0" to signify that this node has mined a new coin.

    # for now nodeidentifier is 1
    node_identifier = 376436439478
    blockchain.new_transaction(
        sender = 0,
        recipient = node_identifier,
        amount = 100,
        sign1 = 1,
        sign2 = 1,
    )

    # Forge the new Block by adding it to the chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    # Forward Mined block
    time.sleep(random.uniform(1,4))
    blockchain.forwardBlock(json.dumps(block))

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    print(response)
    return JsonResponse(response)

@api_view(['POST'])
def new_block(request):

    print("Received Block...")
    values = request.data

    proof = int(values["proof"])

    # check if all data is received.

    last_proof = blockchain.last_block["proof"]
    #print(blockchain.last_block)
    last_hash = blockchain.hash(blockchain.last_block)

    chain = blockchain.chain
    print(type(chain))

    if (values not in chain) and blockchain.valid_proof(last_proof, proof, last_hash):
        print("Proof Matched, adding block....")
        blockchain.chain.append(values) 
        response = {
            'new block':'verified and accepted'
        }
    else:
        print('proof not matching or block already exists')
        response ={
            'error':'proof not matching or block already exists'
        }

    
    


    return JsonResponse(response)



@api_view(['GET'])
def last_block_hash(request):
    last_block = blockchain.last_block
    previous_hash = blockchain.hash(last_block)

    response = {
        'last-block-hash':previous_hash
    }
    return JsonResponse(response)



@api_view(['POST'])
@parser_classes([JSONParser])
def new_transaction(request):
    values = request.data
    
    # Check that the required fields are in the POST data
    required = ['sender', 'recipient', 'amount', 'sign1','sign2']
    if not all(k in values for k in required):
        response = {
            "error":"missing values"
        }
        return JsonResponse(response)
    
    #print(values)
    
    """
    M = {
        "sender": values['sender'],
        "recipient": values['recipient'],
        'amount': values['amount'],
        'sign1': values['sign1'],
        'sign2': values['sign2'],
        'gen': values['gen'],
        'prime': values['prime'],
        'type':micro
    }
    """

    M = json.dumps(values)

    print("Transaction Received")

    # Verify transaction
    
    block = blockchain.current_transactions

    if not schnorr.verifySigner(M):
        print("sign cannot be verified")
        return JsonResponse({'error':'Signature cannot be verified'})
    elif values in block:
        print("Same Tx exists in block")
        return JsonResponse({'error':'Same transaction exists in this block'})

    print("Transaction Verified, Adding and Forwarding transaction...")
    # Create a new Transaction  
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'], values['sign1'], values['sign2'])
    time.sleep(random.uniform(1,4))
    blockchain.forwardTx(M)    # Forwarding Transaction to other nodes.


    print(f"Transaction Added to Block {index}...")

    # Mining Block after 10 transactions in current block
    if len(blockchain.current_transactions) == 10:
        print(f"10 Transactions in block {index}, mining...")
        return HttpResponseRedirect('/mine')

    response = {'message': f'Signature Verified, Transaction will be added to block {index}'}
    return JsonResponse(response)



@api_view(['GET'])
def full_chain(request):
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return JsonResponse(response)

@api_view(['GET'])
def block(request,block_num):
    response={
        'block':blockchain.chain[block_num]
    }
    return JsonResponse(response)



@api_view(['POST'])
@parser_classes([JSONParser])
def register_nodes(request):
    values = request.data

    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return JsonResponse(response)


@api_view(['GET'])
def consensus(request):
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }

    return JsonResponse(response)


