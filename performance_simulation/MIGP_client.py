# coding: utf-8
#!/usr/bin/env python3

import sys
import os
from tokenize import Token 
parent_dir = os.path.join(os.getcwd(), "..") 
sys.path.insert(0, parent_dir)


import argparse
import requests
import time

from miscellaneous.hash_functions import sha256bin, _argon2
from miscellaneous.utilities import parse_args_client, write_performance_result, get_pws_variations_serial

from petlib.ec import EcGroup, EcPt

 
if __name__ == "__main__":
    opt = parse_args_client()
    username = opt.username
    password = opt.password
    RATE_LIMITING = opt.rate_limiting
    PREFIX_LEN = opt.prefix_len
    serverURL = opt.serverURL
    serverPORT =opt.serverPORT
    timelogging = opt.timelogging
    n= opt.n # password variations
    
    suffix = "w/o rate limit" if RATE_LIMITING == 0 else "w/ rate limit" 
    total  = 0
    stat = time.time()
    bucket_id  = sha256bin(username.encode())[0:PREFIX_LEN]

    ''' 714 SECG curve over a 256 bit prime field (secp256k1) '''
    G = EcGroup(714)
    q = G.order()

    client_key = q.random()
    client_inverse_key = client_key.mod_inverse(q)
    passwords = [password]
    passwords.extend(get_pws_variations_serial(password, n, [])) # assuming no BL
    #print(passwords)
    total = 0
    pr_values = ''
    for i in range(len(passwords)):
        password_to_check = passwords[i]
                     
        x = len(username).to_bytes(1, 'little') + username.encode() + \
            len(password).to_bytes(1, 'little') + password_to_check.encode()

        if RATE_LIMITING == 0:
            hash  = sha256bin(x)
        else:
            hash  = _argon2(x)
    
        H = G.hash_to_point(hash)
        pr_value = H.__rmul__(client_key)
        pr_value = pr_value.__str__()
        #print(len(pr_value))
        pr_values += pr_value
        
    
    data = dict(bucket_id=bucket_id, pr_values=pr_values)
    #print("Sending POST data to MIGP server:\n {}".format(data))

    query_prep_time = time.time() - stat
    total += query_prep_time
    write_performance_result(f'Query Prep. {suffix}', query_prep_time, timelogging) 
        
        
    # SENDING THE DATA
    stat = time.time()
    resp = requests.post(f'{serverURL}:{serverPORT}/check/', data=data)
    API_call_time = time.time() - stat
    total += API_call_time
    write_performance_result(f'API call', API_call_time, timelogging) 
    #print(f'=========size of the response is {len(resp.content)} bytes=======')
    write_performance_result(f'B/w (MB)', (len(resp.content) + len(data))/32e6, timelogging) 
        
        

    stat = time.time()
    ys = resp.content[0:n*33]
    z_b = resp.content[n*33:]
    idx = 0
    exact_checking = False
    similar_checking = False
    #print(ys)
    while idx < len(ys):
        y = ys[idx:idx+33]
        #print(y, i )
        idx +=33
        y = EcPt.from_binary(y, G)
        #print("Received y = ", y)
        H_k = y.__rmul__(client_inverse_key)
        
        F_k = sha256bin(x + bytes.fromhex(H_k.__str__()))
        
        z_0 = F_k
        if i == 0:
            z_1 = int.from_bytes(z_0, byteorder='big', signed=False) ^ 1
            z_1 = z_1.to_bytes(32,  byteorder='big', signed=False)
            similar_checking = similar_checking or z_1 in z_b
            exact_checking = z_0 in z_b
        else:
            exact_checking = exact_checking or z_0 in z_b
        i +=1
        
        
    Finalize_time = time.time() - stat
    total += Finalize_time
    write_performance_result(f'Finalize', Finalize_time, timelogging)
    write_performance_result(f'total_{suffix}', total, timelogging)  # + len(data)?? 
    #print(z_b[0])
    # time_file.write(f'after_call\t{after}\n')
    if timelogging == 0:    
        if exact_checking:
            print("Exact password present has been leaked!")
        elif similar_checking:
            print("Not exact but similar password present has been leaked!")
        else:
            print("Exact or similar password has NOT been leaked!")
    else:
        #print("Done with IDB API Call with params = ", opt)
        pass
        