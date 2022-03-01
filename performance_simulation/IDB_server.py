# coding: utf-8
#!/usr/bin/env python3

import sys
import os 
parent_dir = os.path.join(os.getcwd(), "..") 
sys.path.insert(0, parent_dir)


# Precomputation time and size
# Call time. // this can be done by extrapolating values from   



import numpy as np
import flask
import math
import time



from random import seed
from petlib.ec import EcGroup, EcPt 
from flask import request

from miscellaneous.hash_functions import sha256bin, _argon2
from miscellaneous.utilities import parse_args_server

''' Values taken from Figure 11 second column of our paper dentoting av.g bucket size 
for l = [16, 20] withblocklisting'''
MEAN =  { 16: 1431.876, 20: 10} #89492
STD =   { 16: 30.107, 20: 7.513}



opt = parse_args_server()
PREFIX_LEN = opt.prefix_len
RATE_LIMITING = opt.rate_limiting
PORT = opt.port
n = 1 


''' 714 SECG curve over a 256 bit prime field (secp256k1) '''
G = EcGroup(714) 
q = G.order()
server_key = q.random()


bucket_hashes_byte_array = b''
bucket_hashes_list = []
username = "Alice"
password = "123456" 

def add_to_bucket(username, password):
    x = len(username).to_bytes(1, 'little') + username.encode() + \
        len(password).to_bytes(1, 'little') + password.encode()
    
    if RATE_LIMITING == 0:
        hash = sha256bin(x) # fash hashing
    else:
        hash = _argon2(x) #argon2 slow hashing.
        
    H = G.hash_to_point(hash)
    H_k = H.__rmul__(server_key)
    pr_value = sha256bin(x + bytes.fromhex(H_k.__str__()))
    pr_value = int.from_bytes(pr_value, byteorder='big', signed=False)
    pr_value = pr_value.to_bytes(32,  byteorder='big', signed=False)
    #print(len(pr_value), pr_value)
    bucket_hashes_list.append(pr_value)
    #print(bucket_hashes)



''' Pre-computation: preparing the hashes stored on the server for req_type = 1'''
add_to_bucket(username, password)


# Now pushing random hashes...
N = math.ceil(MEAN[PREFIX_LEN])
keeper = os.urandom(32)           
for i in range(N-2):
    #print(i)
    bucket_hashes_list.append(keeper)
    bucket_hashes_byte_array+= keeper

for pr_value in bucket_hashes_list:
    bucket_hashes_byte_array += pr_value



print('Done with preloading hashes')


def get_hashes_from_bucket(bucketID):
    '''This one uses bytearrays'''        
    return bucket_hashes_byte_array
        

app = flask.Flask(__name__)


def process_request(bucketID, pr_values):
    
    z_b = get_hashes_from_bucket(bucketID)
    resp = b''
    idx = 0
    while idx+66 < len(pr_values):
        val = EcPt.from_binary(bytes.fromhex(pr_values[idx:idx+66]), G)
        y =  val.__rmul__(server_key) 
        y = bytes.fromhex(y.__str__())
        #print(y)
        resp  += y
        idx+=66 
        #print(resp[0:33])
    #print(len(resp), resp)
    resp += z_b
    return resp

@app.route('/check/', methods=['GET', 'POST'])
def check():
    response_message = {}
    pr_values = request.form['pr_values']
    bucketID = request.form['bucket_id']
    print(f'=============\npr_values = {pr_values}; bucketID = {bucketID}=========\n')
    
    #stat = time.time()
    response_message = process_request(bucketID = bucketID, pr_values = pr_values)
    #print(f'process request time = {time.time() - stat}')
    return response_message
        



if __name__ == "__main__":
    ''' Running the server ''' 
    app.run(host='0.0.0.0', port=PORT, debug=True)