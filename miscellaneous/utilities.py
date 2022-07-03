# coding: utf-8
#!/usr/bin/env python3

import sys
import os
sys.path.append("..")

from pathlib import Path
import numpy as np

DIR = os.getcwd()
SECURITY_SIMU_RES_FNAME =  os.path.join(DIR, "..", "results/security_simulation.tsv")
PERFORMANCE_SIMU_RES_FNAME = os.path.join(DIR, "..","results/performance_simulation.tsv")


def filter_ws(w):
    """should a w be considerd or not"""
    return 4 <= len(w) <= 30 and all(32 < ord(c) < 128 for c in w)


from miscellaneous.edit_distance_rules import get_tweaks_rules
from miscellaneous.top_20_rules import get_das_R_rules


##  For generating tweaks in parallel
def get_pws_variations(args):
    K = args[1]
    if K == 0:
        return []
    if K == 10:
        return get_das_R_rules(*args)
    elif K == 100:    
        return get_tweaks_rules(*args)
    
##  For generating tweaks serially
def get_pws_variations_serial(pw, k, BL):
    if k == 1:
        return []
    if k == 10:
        return get_das_R_rules(pw, k, BL)
    elif k == 100:    
        return get_tweaks_rules(pw, k, BL)    
    


from multiprocessing import Pool
import itertools

def get_pws(fname, n=int(1e9), BL=[]):
    with open(fname) as f:
        for l in f:
            ll = l.rstrip('\n').split('\t')
            if len(ll) != 2: continue
            c, w = ll[0], ll[1]
            if filter_ws(w) and w not in BL:
                yield (c, w)
                n -= 1
                if n<=0: break

def get_block_list(fname, k, bl):
    if bl<=0: return set()
    bl_pws = list(w for _, w in get_pws(fname, n=bl))
    BL = {}
    args = zip(
            bl_pws, itertools.repeat(k), itertools.repeat(BL)
    )
    with Pool(20) as p:
        bl_pws.extend(itertools.chain(*p.map(get_pws_variations, args, chunksize=10000)))
    return set(bl_pws)


def write_results(success, tpws, qc, bl, k):
    result_arry  = np.zeros(len(tpws)//5000)
    attack_success = 0
    for i, is_success in enumerate(success):
        if is_success: 
            attack_success +=1
            print(tpws[i])
            #print(f'Guess No {i}; success = {success}')
        if (i+1) % 5000 == 0:
            print(f'Done with {i+1} pws; success = {attack_success}')
            result_arry[i//5000] = (attack_success/5000)*100
            attack_success = 0
                       
    out_file = open(SECURITY_SIMU_RES_FNAME, 'a+')
    out_file.write(f'{k}\t{bl}\t{qc}\t{result_arry.mean()}\t{result_arry.std()}\n')
    out_file.close()
    print(f'{k}\t{bl}\t{qc}\t{result_arry.mean()}\t{result_arry.std()}\n')
    

################## PERFORMANCE SIMULATION UTILS ##########################
import argparse
def parse_args_client():
    parser = argparse.ArgumentParser()
    parser.add_argument('--username', action='store', dest='username',type=str, help='username', default="Alice")
    parser.add_argument('--password', action='store', dest='password',type=str, help='password',default="123456")
    parser.add_argument('--rate_limiting', action='store', dest='rate_limiting',type=int, help='Adding argon2 to rate limit client', default=0)
    parser.add_argument('--prefix_len', action='store', dest='prefix_len',type=int, help='Prefix Length \in [16, 20]', default=20)
    parser.add_argument('--serverURL', action='store', dest='serverURL',type=str, help='Server URL', default="http://0.0.0.0")
    parser.add_argument('--serverPORT', action='store', dest='serverPORT',type=int, help='serverPORT', default=8774)
    parser.add_argument('--timelogging', action='store', dest='timelogging',type=int, help='Log the time or not', default=0)
    parser.add_argument('--n', action='store', dest='n',type=int, help='number of variations to consider on client side', default=1)
    return parser.parse_args()

def parse_args_server():
    parser = argparse.ArgumentParser()
    parser.add_argument('--prefix_len', action='store', dest='prefix_len',type=int, help='Prefix Length \in [16, 20]', default=20)
    parser.add_argument('--rate_limiting', action='store', dest='rate_limiting',type=int, help='Adding argon2 to rate limit client', default=0)
    parser.add_argument('--port', action='store', dest='port',type=int, help='port to run the server', default=8774)
    parser.add_argument('--n', action='store', dest='n',type=int, help='number of password variations to consider', default=10)
    
    return parser.parse_args()

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--qc', action='store', dest='qc', type=int,
                        help='value of query budget', default=10)
    parser.add_argument('--bl', action='store', dest='bl', type=int,
                        help='number of blocklisted passwords')
    parser.add_argument('--k', action='store', dest='k', type=int,
                        help='number of variations to consider')
    return parser.parse_args()


def write_performance_result(col_name, val, timelogging):
    if timelogging == 1: 
        out_file = open(PERFORMANCE_SIMU_RES_FNAME, 'a+')
        out_file.write(f'{col_name}\t{val}\n')
        out_file.close()

