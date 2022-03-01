# coding: utf-8
#!/usr/bin/env python3
import sys
sys.path.append("..")

import time
import numpy as np

from miscellaneous.utilities import get_pws_variations
from miscellaneous.hash_functions import _argon2, sha256bin
from petlib.ec import EcGroup


fname = 'random.10k.pws.txt'
''' computing the time to get variations '''
ks = [10, 100]
for k in ks:
    time_arr = np.zeros(10000)
    with open(fname, 'r') as f:
        
        i = 0
        for pw in f:
            s1 = time.time()
            res = get_pws_variations(pw.strip(),k, [])
            time_arr[i] = time.time()-s1
            i +=1
    print(f'pws_variations\tk={k}\t{np.mean(time_arr)}\t{np.std(time_arr)}')

''' computing the time to get PRF value '''

G = EcGroup(714)
q = G.order()
server_key = q.random() 

prf_time = np.zeros(10000)
argon_2_time = np.zeros(10000)
username = "Mazharul"

with open('random.10k.pws.txt', 'r') as f:
    for i, pw in enumerate(f):
        prf_tim = 0.0
        s1 = time.time()
        bucketID = sha256bin(username.encode())[0:5]
        password = pw.strip('\n')
        x = len(username).to_bytes(1, 'little') + username.encode() + \
                            len(password).to_bytes(1, 'little') + password.encode()
        prf_tim += (time.time() - s1)
        
        s1 = time.time()
        argon2_hash = _argon2(x)
        
        argon_2_time[i] = (time.time() - s1)
        prf_tim += argon_2_time[i]
        s1 = time.time()
        H = G.hash_to_point(argon2_hash)
        H_k = H.__rmul__(server_key).export().hex()
        prf_tim += (time.time() - s1)
        prf_time[i] = prf_tim
        
print(f'Argon2 computation time {np.mean(argon_2_time)}, {np.std(argon_2_time)}')
print(f'PRF computation time {np.mean(prf_time)}, {np.std(prf_time)}')                      

                        

                        
                        