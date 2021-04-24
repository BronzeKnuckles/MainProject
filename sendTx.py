import json
import requests
import random
import time 

import schnorr


nodes = ['127.0.0.1:8000']
t = []


for i in range(100):

    for node in nodes:

        s = time.time()
        x,y,g,q = schnorr.produceKeys()
        recipient = random.randint(999,q)
        amount = random.randint(1,1001)
        M = schnorr.signTransaction(x,y,g,q,recipient,amount) 
        response = requests.post(f'http://{node}/new_tx', json= json.loads(M))
        r = response.json
        type(r)
        f = time.time()

        t.append(f-s)
        
    
    if (i+1) % 10 == 0:

        r = requests.get(f'http://{node}/mine')
        print("mining...")
        print(type(r))
    

s = 0
for i in t:
    s = s + i*1000
    
print(s/(len(t)))