from hashlib import sha256
from random import randint
from Crypto.Util import number 
import json


"""
    TODO:
"""


def hashThis(r, M):
    hash=sha256()
    hash.update(str(r).encode())
    hash.update(M.encode())
    return int(hash.hexdigest(),16)

def produceKeys():
    
    # generator g , initially it was 2
    g = 10

    # Prime q 
    q = number.getPrime(64)
    
    ## Key generation:

    #Private signing key x

    
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
            "sender": y, 
            "recipient": 123, 
            "amount": 10,
        }
    #print(M,type(M))
    
    M = json.dumps(M)
    #print(M,type(M))
    


    e = hashThis(r, M) % q # part 1 of signature

    s = (k - (x * e)) % (q-1) # part 2 of signature

    M = json.loads(M)
    M["sign1"] = s
    M["sign2"] = e
    #M["gen"] = g
    #M["prime"] = q

    #print(M,type(M))
    M = json.dumps(M)
    #print(M,type(M))


    return M


def verifySigner(M):

    M = json.loads(M)

    s = M["sign1"]
    M.pop("sign1")
    e = M["sign2"]
    M.pop("sign2")
    y = M["sender"]
    #M.pop("sender")

    if M["amount"] >1000:
        q = 76443937932047922915202785024949244450942401384750373484858624451650688927493
        g = 5
    else:
        q = 338269374607933819018612063891041467693
        g = 3
    
    M = json.dumps(M)
    #print(M,type(M))
        

    rv = (pow(g, s, q) * pow (y, e, q)) % q  
    ev = hashThis(rv, M) % q

    # e should equal ev 
    #print(str(e))
    #print(str(ev))

    #print("in verifySigner")

    if str(e) == str(ev):
        return True
    else:
        return False

"""
x,y,g,q = produceKeys()
M = signTransaction(x,y,g,q)
print(verifySigner(M))
"""