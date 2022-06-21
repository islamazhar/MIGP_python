# coding: utf-8
#!/usr/bin/env python3

import sys
sys.path.append("..")

import argparse
import itertools
import numpy as np
import marisa_trie

from word2keypress import Keyboard
from multiprocessing import Pool
from pathlib import Path

from miscellaneous.utilities import get_pws_variations, get_pws, get_block_list , parse_args

kb = Keyboard()



opt = parse_args()


def generate_variation_trie(DIR, breach_fname, N, k, bl):
    """
    1. write variations to a file in /tmp/variations.pws
    2. run marisa-build to create a trie in /noback folder
    3. use /tmp/variations.pws and the trie in /nobackup folder to create numpy array
    """
    fname = DIR / breach_fname
    #assert k == 100, f"TODO: change the function for k != 100. Got k={k}"
    tmpf = '/tmp/variations.pws'
    K = k
    BL = get_block_list(fname, k, bl)
    all_pws = []
    print(len(BL), K)
    with open(tmpf, 'w') as of, Pool(20) as p:
        pws = [w for _, w in get_pws(fname, n=N)]
        args = zip(
            pws, itertools.repeat(k), itertools.repeat(BL)
        )
        result = p.imap(get_pws_variations, args, chunksize=10000)
        print(result, len(pws))
        for i, (w, ws) in enumerate(zip(pws, result)):
            if i<5:
                print(w, len(ws))
            of.write("{}\t{}\n".format(w, '\t'.join(ws)))
            all_pws.append(w)
            all_pws.extend(ws)
            if i%10000 == 0:
                print(f"Done {i} passwords. all_pws={len(all_pws)}")
        T = marisa_trie.Trie(list(set(all_pws)))
    a = np.zeros((N, k), dtype=np.int32)
    b = np.zeros(N, dtype=np.int32)
    b_reverse = np.zeros(len(T), dtype=np.int32)
    b_reverse.fill(-1)
    with open (tmpf) as f:
        for i, l in enumerate(f):
            if i>N: break
            w, *ws = l.rstrip('\n').split('\t')
            a[i] = np.array([T[tw] for tw in ws]) #len(ws) != k
            b[i] = T[w]
            b_reverse[T[w]] = i
    print(len(T))
    T.save(f'data_files/variations/{N}.{bl}.{k}.variations.trie')
    np.savez_compressed(f'data_files/variations/{N}.{bl}.{k}.variations.npz', var=a, pws=b, pws_r=b_reverse)

N = int(1e6)   # Number of passwords to consider

#DIR = Path("/pwdata/mazharul/password_research_dataset_Jan/")
DIR = Path("data_files/")
breach_fname = 'mixed_full_leak_data_40_1_with-pws-counts.txt'

if __name__ == "__main__":
    generate_variation_trie(DIR, breach_fname, N, opt.k, opt.bl)