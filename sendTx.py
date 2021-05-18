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
        
        
        amount = random.randint(1,3000)

        if amount > 1000:
            q = 76443937932047922915202785024949244450942401384750373484858624451650688927493
            g = 5 
        else:
            q = 338269374607933819018612063891041467693
            g = 3
        recipient = random.randint(999,q)
        x,y,g,q = schnorr.produceKeys(q,g)
        M = schnorr.signTransaction(x,y,g,q,recipient,amount) 
        response = requests.post(f'http://{node}/new_tx', json= json.loads(M))
        r = response.json
        type(r)
        f = time.time()
        print(i)
        t.append(f-s)
        
    """
    if (i+1) % 10 == 0:

        r = requests.get(f'http://{node}/mine')
        print("mining...")
        print(type(r))
        """
    

s = 0
for i in t:
    s = s + i*1000
    
print(s/(len(t)))