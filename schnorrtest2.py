from hashlib import sha256
from random import randint
from Crypto.Util import number 
import json

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
    #M = "This is the message"
    
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
    M["sign"] = s

    print(M,type(M))


    return e,M


def verifySigner(g,q,e,M):
    s = M["sign"]
    rv = (pow(g, s, q) * pow (y, e, q)) % q
    M.pop("sign")
    M = json.dumps(M)
    ev = hashThis(rv, M) % q

    #print ("e " + str(e) + " should equal ev " + str(ev))
    # e should equal ev 

    if str(e) == str(ev):
        return "Author Verified!"
    else:
        return "Nope"


x,y,g,q = produceKeys()
e,M = signTransaction(x,y,g,q)
print(verifySigner(g,q,e,M))