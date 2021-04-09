from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.http import JsonResponse

from blockchain import Blockchain
import schnorr


blockchain = Blockchain()
"""
    TODO:
        - return block based on block number? get req.
        - /api for all available apis
        - node identifier -> public key
        - save block after every transdaction 
        - delete and save block after consensus change

"""
@api_view(['GET'])
def api(request):
    response = {
        "/mine": "mine current block",
        "/lbh": "request last block hash",
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
    node_identifier = "1"
    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
    )

    # Forge the new Block by adding it to the chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return JsonResponse(response), 200

@api_view(['GET'])
def last_block_hash(request):
    last_block = blockchain.last_block
    previous_hash = blockchain.hash(last_block)
    return previous_hash



@api_view(['POST'])
def new_transaction(request):
    values = request.get_json()

    # Check that the required fields are in the POST data
    required = ['sender', 'recipient', 'amount', 'sign1','sign2']
    if not all(k in values for k in required):
        return 'Missing values', 400
    
    M = {
        'sender': values['sender'],
        'recipient': values['recipient'],
        'amount': values['amount'],
        'sign1': values['sign1'],
        'sign2': values['sign2'],
        'gen': values['gen'],
        'prime': values['prime'],
    }

    # Verify transaction
    if not schnorr.verifySigner(M):
        return 'Signature cannot be verified', 400 

    # Create a new Transaction  
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'], values['sign1'], values['sign2'], values['gen'], values['prime'])


    response = {'message': f'Signature Verified, Transaction will be added to Block {index}'}
    return JsonResponse(response), 201


@api_view(['GET'])
def full_chain(request):
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return JsonResponse(response), 200

@api_view(['GET'])
def block(request,block_num):
    response={
        'block':blockchain.chain[block_num+1]
    }
    return JsonResponse(response), 200



@api_view(['POST'])
def register_nodes(request):
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return JsonResponse(response), 201


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

    return JsonResponse(response), 200


