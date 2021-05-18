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
    #g = 10
    g = 14244512588445236029
    # Prime q 
    #q = number.getPrime(70)
    q = 26460387200485559731440593670635573609795914018099130774800409471006104753558009440604528497421809368596963451379452454512489166220409498394014491662973198259248527560037105935698793009198416233333897091380760575663340866532220328171924079068779415714805208834545548689753300149956869941673571654836174500832606712891993011877275488483699503045306675294185705827246652554539329245604767675065047776327249662107836785056734518019346850166635081958872363026002280314142914235535770434780129948281574927145259735178868893354002240222827800678656615228929738492983631535037887460228401120661647351628311985966219689710027

    ## Key generation:

    #Private signing key x

    
    # x <- Secret Key
    x = randint(1,q-1)

    # calculate public verification key y
    y = pow(g, x, q)

    return x,y,g,q

def signTransaction(x,y,g,q,recipient = 123, amount = 10):
    # M is message/ transactuion to sign
    
    k = randint(1, q - 1)
    r = pow(g, k, q)

    M = {
            "sender": y, 
            "recipient": recipient, 
            "amount": amount,
        }
    #print(M,type(M))
    
    M = json.dumps(M)
    #print(M,type(M))
    


    e = hashThis(r, M) % q # part 1 of signature

    s = (k - (x * e)) % (q-1) # part 2 of signature

    M = json.loads(M)
    M["sign1"] = s
    M["sign2"] = e
    M["gen"] = g
    M["prime"] = q

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
    g = M["gen"]
    M.pop("gen")
    q = M["prime"]
    M.pop("prime")
    y = M["sender"]
    #M.pop("sender")

    
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