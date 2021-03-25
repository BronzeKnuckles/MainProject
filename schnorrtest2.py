from hashlib import sha256
from random import randint
from Crypto.Util import number 
import json


"""
    TODO:
         - getPrime parameter number?
         - g = 10? universal?
         - where all is q needed?
         - Can't Compute e again in verifySigner() like in signTransaction() WTF
"""


def hashThis(r, M):
    hash=sha256()
    hash.update(str(r).encode())
    hash.update(M.encode())
    return int(hash.hexdigest(),16)

def produceKeys():
    ## Notation
    # generator g
    g = 10

    # Prime q (for educational purpose I use explicitly a small prime number - for cryptographic purposes this would have to be much larger)
    q = number.getPrime(70)

    ## Key generation
    #Private signing key x

    #x = 32991
    # x <- Secret Key
    x = randint(1,q-1)

    # calculate public verification key y
    y = pow(g, x, q)

    return x,y,g,q

def signTransaction(x,y,g,q):
    # M is message/ transactuion to sign
    
    k = randint(1, q - 1)
    r = pow(g, k, q)

    M = {
            'sender': y, 
            'recipient': "bake2", 
            'amount': 10,
        }
    print(M,type(M))
    
    M = json.dumps(M)
    print(M,type(M))
    


    e = hashThis(r, M) % q # part 1 of signature

    s = (k - (x * e)) % (q-1) # part 2 of signature

    M = json.loads(M)
    M["sign1"] = s
    M["sign2"] = e

    print(M,type(M))


    return M


def verifySigner(g,q,M):

    s = M["sign1"]
    M.pop("sign1")
    e = M["sign2"]
    M.pop("sign2")

    M = json.dumps(M)
        

    rv = (pow(g, s, q) * pow (y, e, q)) % q  
    ev = hashThis(rv, M) % q

    # e should equal ev 
    print(str(e))
    print(str(ev))

    if str(e) == str(ev):
        return "Author Verified!"
    else:
        return "Nope"


x,y,g,q = produceKeys()
M = signTransaction(x,y,g,q)
print(verifySigner(g,q,M))