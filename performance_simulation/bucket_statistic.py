# coding: utf-8
#!/usr/bin/env python3

import sys
sys.path.append("..")

import time
import numpy as np

from miscellaneous.utilities  import get_pws_variations, filter_ws, get_block_list, filter_ws
from miscellaneous.hash_functions import sha256bin 
from pathlib import Path

PORT = 8084
K = 100
bl = 1000

DIR = Path("/pwdata/mazharul/password_research_dataset_Jan/")
breach_fname = 'mixed_full_leak_data_40_1_with-pws-counts.txt'
fname = DIR / breach_fname

results_file_name = "/u/m/a/mazharul/private/MIGP_Final/results/bucket_size.csv"
pw_leak_file = '/pwdata/mazharul/password_research_dataset_Jan/username_full_leak_100.txt'
hash_pw_leak_file = '/pwdata/mazharul/password_research_dataset_Jan/mixed_full_leak_data_100.precomputed.k.1000'
## Size 31600511320 bytes (790,012,783 users)

################################################################################
############# Another attempt ##################################################
import struct
FORMAT = "<32s2Q" # "<32s4H"
LINE_SIZE = 48 # 32+4*8

ST = struct.Struct(FORMAT)

def sprep_line(h,nbl_nws,  bl_npws):
    """
    Everything will be stored in binary. 
    h: 32-byte hash of username
    npws and nsimpws: 2-byte unsigned ints (k=10) / 8-byte unsigned long long (k=100)
    """
    return ST.pack(h, nbl_nws, bl_npws) # 

def parse_from_file(fbuf):
    """Returns an iterator of the file"""
    return ST.unpack_from(fbuf)

BL_PWS = get_block_list(fname, k=K, bl=bl) 

def create_all_hashes(pw_leak_file, hash_pw_leak_file, user_in_diff_lines=False):
    """the file is formatted as follows
    u\tpw1\tpw2...
    """
    print("Creating all hashes..")
    s1 = time.time()
    assert not BL_PWS is None, "BL_PWS need to be set prior to calling this function"
    with open(pw_leak_file, 'r') as fpw, open(hash_pw_leak_file, 'wb') as whashf:
        for i, l in enumerate(fpw):
            if len(l.rstrip('\n').split('\t')) < 2:
                continue

            u, all_ws = l.rstrip('\n').split('\t', 1)
            h = sha256bin(u.encode())
            
            ws = set([w for w in all_ws.rstrip('\n').split('\t') if filter_ws(w)])
           # print("ws = ", ws)
            nbl_nws = len(ws)
            if nbl_nws   == 0:
                continue
            bl_npws  = len([ _ws for _ws in ws if _ws not in BL_PWS])
            '''
            sim_pws = list(ws)
            for w in ws:
                for _w in get_pws_variations(word=w, K=K,BL=[]):
                    if filter_ws(_w):
                        sim_pws.append(_w)
            '''
            #nbl_nsimpws = nbl_nws * K
            #bl_nsimpws =  len([ _ws for _ws in sim_pws if _ws not in BL_PWS])
            #bl_nsimpws = bl_npws * K
            #print(h, nbl_nws, nbl_nsimpws, bl_npws, bl_nsimpws)
            whashf.write(sprep_line(h, nbl_nws,bl_npws))
            
            if i % 100000000 == 0:
                print("Done with {} lines in {} seconds...".format(i, time.time()-s1))

################################################################################

def get_results(pcompfile, prefixLength):
    names = ['IDB']
    bcs = ['0', '1000']
    buckets = {}
    for name in names:
        for bc in bcs:
            buckets[name+ bc] = np.zeros(2**prefixLength)

    no = 0
    PREFIX_LEN = prefixLength//4
    s1 = time.time()


    with open(pcompfile, 'rb') as whashf:
        it = whashf.read(LINE_SIZE)
        while it:
            h, nbl_nws, bl_npws = parse_from_file(it)
            #print(h, migp_npws, migp_nsimpws, idbp_npws, idbp_nsimpws)
            h = h.hex()[0:PREFIX_LEN]
            #print(h)
            bucketID = int(h, 16)
            #print(bucketID)
            #bucketID = h[0:PREFIX_LEN]
            no +=1
            if no % 100000000 == 0:
                print("PrefixLength = {}, Done with {} lines in {} seconds...".format(prefixLength, no, time.time()-s1))
                #break
            buckets[names[0] + bcs[0]][bucketID] += nbl_nws
            buckets[names[0] + bcs[1]][bucketID] += bl_npws
            it = whashf.read(LINE_SIZE)

    # write results
    print("Writing to result file...for prefix length =", prefixLength)                
    with open(results_file_name+'.csv', "a+") as result:
        for name in names:
            for bc in bcs:
                values = []
                for val in buckets[name + bc]:
                    if val > 0:
                        values.append(val)
                                
                avg = np.mean(values)
                std = np.std(values)
                #print(values)
                #print(avg, std)
                #print(prefixLength,name,bc,avg,std)
                result.write("{}\t{}\t{}\t{}\t{}\n".format(prefixLength,name,bc,avg,std))    
    
if __name__ == "__main__":

    #opt = parse_args()
    
    create_all_hashes(pw_leak_file = pw_leak_file, hash_pw_leak_file = hash_pw_leak_file)
    prefixLengths = [16, 20, 24]
    for prefix in prefixLengths:
        get_results(hash_pw_leak_file, prefix)