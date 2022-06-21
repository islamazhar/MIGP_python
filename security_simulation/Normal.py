# coding: utf-8
#!/usr/bin/env python3

import sys
sys.path.append("..")


import numpy as np

from pathlib import Path
from miscellaneous.utilities import  get_block_list, get_pws, write_results
from security_simulation.get_variations import parse_args


PRE = False
opt = parse_args()

''' parameters '''
bl = opt.bl
qc = opt.qc
k = opt.k
N = int(1e6)

''' file locations '''
DIR = Path("data_files/")
breach_fname = 'mixed_full_leak_data_40_1_with-pws-counts.txt'
test_file = 'target_pws_25000.S2.txt'
leak_fname = DIR / breach_fname
target_fname =  DIR / test_file

def normal_login(tpws, qc, bl):
    
    bl_list = get_block_list(leak_fname, 0, bl)
    top_q_quess = [w for _, w in get_pws(leak_fname, n=qc, BL= bl_list)]
    success = np.zeros((len(tpws)), dtype=bool)
    for i, tpw in enumerate(tpws):
        if tpw in top_q_quess:
            success[i] = True
    return success
         
 
if __name__ == '__main__':
    
    with open(target_fname, 'r') as fin:
        tpws = [w.strip('\n') for w in fin]
        print(f'Size of the target pws = {len(tpws)}')
        # get the top q quesses from the pw-count file.
        assert k == 0, 'K can not be non zero'
        success = normal_login(tpws, qc, bl)
        #print(success.sum())
        write_results(success, tpws, qc, bl, k)

     
    
    
        
    