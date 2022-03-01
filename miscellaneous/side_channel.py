# coding: utf-8
#!/usr/bin/env python3

import sys
sys.path.append("..")

import time
import numpy as np
import itertools

from miscellaneous.utilities  import get_pws_variations, filter_ws, get_block_list, filter_ws
from miscellaneous.hash_functions import sha256bin 
from pathlib import Path
from multiprocessing import Pool


k = 100
bl = int(1e4)

DIR = Path("/pwdata/mazharul/password_research_dataset_Jan/")
results_fname = "side_channel.txt"
FULL_LEAK_FNAME = '/pwdata/mazharul/password_research_dataset_Jan/username_full_leak_100.txt'
fname = DIR / FULL_LEAK_FNAME
#BL = get_block_list(fname, k=k, bl=bl)

import struct
FORMAT = "<32s2q" # "<32s4H"
LINE_SIZE = 48 # 32+4*8
PREFIX_LENGTH = 32
ST = struct.Struct(FORMAT)

def sprep_line(h,a,  b):
    """
    Everything will be stored in binary. 
    h: 32-byte hash of username
    npws and nsimpws: 2-byte unsigned ints (k=10) / 8-byte unsigned long long (k=100)
    """
    return ST.pack(h, a, b)

def parse_from_file(fbuf):
    """Returns an iterator of the file"""
    return ST.unpack_from(fbuf)
    
def calculate():
    s1 = time.time()
    with open(fname) as fin, open(DIR/results_fname, 'wb') as whashf:
        no = 0
        for i, l in enumerate(fin):
            if i == int(1e4):
                break
            if len(l.rstrip('\n').split('\t')) < 2:
                continue
            u, all_ws = l.rstrip('\n').split('\t', 1)
            h = sha256bin(u.encode())
            
            ws = set([w for w in all_ws.rstrip('\n').split('\t') if filter_ws(w)])
            if len(ws) == 0: continue
            no +=1
            wv = list(ws)
            args = zip(
                ws, itertools.repeat(k), itertools.repeat(BL)
            )
            with Pool(20) as p:
                wv.extend(itertools.chain(*p.map(get_pws_variations, args, chunksize=10000)))
            
            #print(len(ws))
            a = len(ws)*(k+1)
            b = len(set(wv))
            #print(f'h = {h}\ta = {a}\tb = {b}')
            whashf.write(sprep_line(h, a, b))
            # hash_usernanme, total_pws_of_the user_with blocklisting, set size we have w blocklisting.
            if no % 1000 == 0:
                print(f"Done with {i} lines in {time.time() - s1} seconds...")
                break
def generate_graph():
    with open(DIR/results_fname, 'rb') as whashf:
        it = whashf.read(LINE_SIZE)
        no = 0
        c = 0
        diff = []
        while it:
            h, tpwod, tpwd = parse_from_file(it)
            if tpwod != tpwd: 
                c +=1
            #print(h.hex()[0:PREFIX_LENGTH], tpwod, tpwd, c, no)
            it = whashf.read(LINE_SIZE)
            d = tpwod - tpwd
            assert d >= 0
            if d!= 0:
                diff.append(d)
            no +=1    
        #print(no, c)
    l = len(diff)
    diff = np.array(diff)
    print(np.mean(diff), np.std(diff), np.max(diff), np.min(diff))
if __name__ == "__main__":
    #calculate()
    generate_graph()