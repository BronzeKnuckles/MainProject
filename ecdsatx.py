
from node.schnorr import verifySigner
import ecdsa
import json
import ast
from hashlib import sha256
import time 

def produceKeys():
  
  sk = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1) 
  vk = sk.get_verifying_key()

  return sk,vk


def signTx(sk,vk):
  
  print(vk.to_pem().decode(),sk.to_pem().decode())
  
  #print(vk)

  vk = vk.to_pem().decode()
  m = {
    "sender": vk,
    "recipient": 123456789101110293732647,
    "amount": 10,
  }

  
  m = json.dumps(m).encode('utf-8')

  sig = sk.sign(m)

  
  # Turn Sig into json serializable
  sig = sig.decode(errors='ignore')
  
  

  
  m = json.loads(m.decode('utf-8'))

  m["sign"] = sig

  m = json.dumps(m)
  #print(m)

  return m
   



def verifySign(m):

  m = json.loads(m)
  

  vk = m["sender"]
  vk = vk.encode()

  sig = m["sign"]
  sig = sig.encode()

  m.pop("sign")

  m = json.dumps(m, indent=2).encode('utf-8')

  vk = ecdsa.VerifyingKey.from_string(vk, curve=ecdsa.SECP256k1, hashfunc=sha256) # the default is sha1
  
  return vk.verify(sig, m)



"""

sk, vk = produceKeys()
m = signTx(sk,vk)
print(verifySign(m))


"""


def doEcdsa():

  l_time1 = []
  l_time2 = []
  l_time3 = []

  for i in range(100):
    t1 = time.time()
    sk = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1) 
    vk = sk.get_verifying_key()
    t2 = time.time()
    
    l_time1.append(t2-t1)

    m = b'{"sender":sender,"recipient":sender,"amount:amount}'

    t1 = time.time()
    sig = sk.sign(m)
    t2 = time.time()
    l_time2.append(t2-t1)

    t1 = time.time()
    assert vk.verify(sig,m)
    t2 = time.time()
    l_time3.append(t2-t1)

  
  print("time for producing key:", l_time1)
  print("time for signing:", l_time2)
  print("time for verifying:", l_time3)

  return l_time1,l_time2,l_time3


def doSchnorr():
  l_time1 = []
  l_time2 = []
  l_time3 = []

  from hashlib import sha256
  from random import randint
  from Crypto.Util import number 
  import json



  def hashThis(r, M):
      hash=sha256()
      hash.update(str(r).encode())
      hash.update(M.encode())
      return int(hash.hexdigest(),16)

  for i in range(100):
    g = 10
    q = number.getPrime(70)

    
    t1 = time.time()      
    x = randint(1,q-1)    
    y = pow(g, x, q)
    t2  = time.time()

    l_time1.append(t2-t1)

    

    recipient = 123 
    amount = 10

      # M is message/ transactuion to sign
      


    M = {
              "sender": y, 
              "recipient": recipient, 
              "amount": amount,
          }
      #print(M,type(M))
      
    M = json.dumps(M)
      #print(M,type(M))


    t1 = time.time()
    k = randint(1, q - 1)
    r = pow(g, k, q)  


    e = hashThis(r, M) % q # part 1 of signature

    s = (k - (x * e)) % (q-1) # part 2 of signature

    t2 = time.time()

    l_time2.append(t2-t1)

    M = json.loads(M)
    M["sign1"] = s
    M["sign2"] = e
    M["gen"] = g
    M["prime"] = q

    #print(M,type(M))
    M = json.dumps(M)
    #print(M,type(M))


    




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
      

      
    M = json.dumps(M)


    t1 = time.time()
    rv = (pow(g, s, q) * pow (y, e, q)) % q  
    ev = hashThis(rv, M) % q
    t2 = time.time()

    assert str(e) == str(ev)

    l_time3.append(t2-t1)

  print("time for producing key:", l_time1)
  print("time for signing:", l_time2)
  print("time for verifying:", l_time3)

  return l_time1,l_time2,l_time3



print("For Schnorr: ")
s1,s2,s3 = doSchnorr()
print("For Ecdsa: ")
e1,e2,e3 = doEcdsa()

from matplotlib import pyplot as plt
import numpy as np



difference = []
zip_object = zip(s1,e1)

for s, e in zip_object:

    difference.append(s-e)

print("1 difference:",difference)


difference = []
zip_object = zip(s2,e2)

for s, e in zip_object:

    difference.append(s-e)

print("2 difference:",difference)

difference = []
zip_object = zip(s3,e3)

for s, e in zip_object:

    difference.append(s-e)

print("3 difference:",difference)
plt.figure(figsize=(12, 3))
plt.subplot(131)
plt.plot(s1, label="schnorr sign", ls="-")
plt.plot(e1, label="ecdsa sign", ls="-")


plt.subplot(132)
plt.plot(s2, label="schnorr signing", ls="--")
plt.plot(e2, label="ecdsa signing", ls="--")


plt.subplot(133)
plt.plot(s3, label="schnorr verification", ls="-.")
plt.plot(e3, label="ecdsa verification", ls="-.")

plt.show()
plt.savefig("matplotlib.png")  #savefig, don't show