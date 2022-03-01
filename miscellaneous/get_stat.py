# coding: utf-8
#!/usr/bin/env python3

import sys
sys.path.append("..")

from pathlib import Path

import time
DATASET_FOLDER = Path("/pwdata/mazharul/new_mixed_full/")
DATASET_FILE = "mixed_full_leak_data_40_1.txt"
BREACH_FNAME = DATASET_FOLDER / DATASET_FILE

from miscellaneous.utilities import filter_ws
upw_count = 0
with open(BREACH_FNAME, 'r') as f:
    i = 0
    for l in f:
        i +=1
        if i % 100000000 == 0:
            print(f"Done with reading {i} lines")
        ll = l.rstrip('\n').split('\t', 1) #username\tabpws1\tabpws2 ...
        if len(ll) != 2: continue
        u, w = ll[0], ll[1]
        count = 0
        for _w in w.rstrip('\n').split('\t'):
            if filter_ws(_w):
                    count +=1
                    
        if count <= 1000:
            upw_count += count
                        
print(f'x <= 30 and len(pws) <= 1000: {upw_count}')