# coding: utf-8
#!/usr/bin/env python3


import sys

from numpy.core.fromnumeric import var
sys.path.append("..")
sys.setrecursionlimit(10000)

import numpy as np
import marisa_trie
import pickle
import itertools
from multiprocessing import Pool

from pathlib import Path


from security_simulation.get_guess_ranks import get_count
from miscellaneous.utilities import get_block_list, get_pws_variations_serial, get_pws_variations


''' parameters '''
bl = 0
ks = [100]
N = int(1e6)

''' file locations '''
DIR = Path("/pwdata/mazharul/password_research_dataset_Jan/")
breach_fname = 'mixed_full_leak_data_40_1_with-pws-counts.txt'
fname = DIR / breach_fname

if __name__ == '__main__':
    '''
    for budget in range(10):
        np_array = np.load(f'{DIR}/Guess/{breach_fname}.{N}.{bl}.{k}.{budget}.password_sum.npz')
        guess = str(np_array['guess'])
        weight = int(np_array['weight'])
        print(guess, weight)
    '''
    variations = []
    
    for k in ks:
        
        pass_trie = marisa_trie.Trie()
        
        BL = get_block_list(fname, k, bl)
        pass_trie.load(f'/nobackup/mazharul/{breach_fname}.{N}.{bl}.{k}.variations.trie')
        print(pass_trie['123456..'])
        counts = get_count(DIR, breach_fname, N, bl, pass_trie, k, BL)
        print(counts[pass_trie['123456..']])
        '''
        print(counts[pass_trie['123456']])
        password_sum_fname = f'/nobackup/mazharul/{breach_fname}.{N}.{bl}.{k}.password_sum.npy'
        password_sum = np.load(password_sum_fname)
        print(password_sum[pass_trie['123456']])
        ball_fname = f'/nobackup/mazharul/{breach_fname}.{N}.{bl}.{k}.balls.txt'
        with open(ball_fname, 'rb') as handle:
            ball_reverse = pickle.load(handle)
             
        print(len(ball_reverse[pass_trie['123456']]))
        _varations = set()
        for i in ball_reverse[pass_trie['123456']]:
            _varations.add(pass_trie.restore_key(i))
        variations.append(_varations)
        '''
        '''
        numpy_array = np.load(f'/nobackup/mazharul/{breach_fname}.{N}.{bl}.{k}.variations.npz')
        pws_variations = numpy_array['var']
        pws = numpy_array['pws']
        pws_r = numpy_array['pws_r']
        uid = pws_r[pass_trie['123456..']]
        #print(uid)
        _variations = set()
        for ii,i in enumerate(pws_variations[uid]):
            #print(pass_trie.restore_key(i))
            _variations.add(pass_trie.restore_key(i))
          
        variations.append(_variations)
        '''
        _variations  = []
        BL = get_block_list(fname, k, bl)
        with Pool(20) as p:
            pws = ['123456..']
            args = zip(
                pws, itertools.repeat(k), itertools.repeat(BL)
            )
            result = p.imap(get_pws_variations, args, chunksize=10000)
            for i, (w, ws) in enumerate(zip(pws, result)):
                    if i<5:
                        print(w, len(ws))
                    #_variations.append(w)
                    _variations.extend(ws)
                    
        variations.append(_variations)    
        _variations = get_pws_variations_serial('123456..', k, [])
        variations.append(_variations)
        
    
    print(len(variations[0]))
    print(len(variations[1]))
    print(variations[0])
    print(variations[1])
    if '123456' in variations[0]:
        print('okay')
    print('Difference...')
    '''
    for i in variations[0]:
        if i not in variations[1]:
            print(i)    
    '''
    #print(variations[0] - variations[1])
    '''
    #assert k == 100, f"TODO: change the function for k != 100. Got k={k}"
    tmpf = '/tmp/variations.pws'
    BL = get_block_list(fname, 100, bl)
    all_pws = []
    with open(tmpf, 'w') as of, Pool(20) as p:
        pws = ['123456..']
        args = zip(
            pws, itertools.repeat(100), itertools.repeat(BL)
        )
        result = p.imap(get_pws_variations, args, chunksize=10000)
        print(result, len(pws))
        for i, (w, ws) in enumerate(zip(pws, result)):
            if i<5:
                print(w, len(ws))
            of.write("{}\t{}\n".format(w, '\t'.join(ws)))
            #all_pws.append(w)
            all_pws.extend(ws)
    l1 = all_pws
    l2 = get_pws_variations_serial('123456..',100, [])
    print(type(l1))
    print(type(l2))
    print(len(l1))
    print(len(l2))
    if '123456' not in l1:
        print('not okay')
    if '123456' not in l2:
        print('not okay')
    '''
    