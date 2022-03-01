# coding: utf-8
#!/usr/bin/env python3
import sys
sys.path.append("..")

from itertools import count
import marisa_trie
import os.path
import time
import json
import pickle5 as pickle
import numpy as np
import shelve
from pathlib import Path

from security_simulation.get_variations import parse_args
from miscellaneous.utilities import get_block_list, filter_ws

PRE = False
opt = parse_args()

def get_count(DIR, breach_fname, n, bc, pass_trie, k, BL):
    count_fname = f'/nobackup/mazharul/{breach_fname}.{n}.{bc}.{k}.counts.npz'
    fname = DIR / breach_fname
    
    if os.path.exists(count_fname) and PRE:
        count_array = np.load(count_fname)['counts']
    else:
        count_array = np.zeros(len(pass_trie))
        with open(fname) as f:
            for l in f:
                ll = l.rstrip('\n').split('\t')
                if len(ll) != 2: continue
                c, w = ll[0], ll[1]
                if filter_ws(w):
                    if w not in BL: #not a blocklisted password.
                        id = pass_trie[w]
                        count_array[id] = int(c.strip())
                    n -= 1
                    if n<=0: break
        np.savez_compressed(count_fname, counts=count_array)
    return count_array


def build_ball_reverse(pws, pws_variations):
    
    ball_reverse = {}
    for i, uid in enumerate(pws):
        for  vid in pws_variations[i]:
            # uid --> vid
            if vid not in ball_reverse.keys():
                ball_reverse[vid]  = []
            ball_reverse[vid].append(uid) 
    return ball_reverse


def build_password_sum(pass_trie, ball_reverse, counts):

    password_sum = np.zeros(len(pass_trie), dtype=np.int32)
    for i, (vid, uids) in enumerate(ball_reverse.items()):        
        weight = counts[vid]
        if i%10000000 == 0:
            print(f"Done {i} passwords. all_pws={len(pass_trie)}")
        for uid in uids:
            weight = weight + counts[uid]
        password_sum[vid] = weight
    return password_sum


def get_guess_ranks(bl, k, qc):
  
    
    BL = get_block_list(fname, k, bl)
    
    # Load Marise trie
    pass_trie = marisa_trie.Trie()
    #print(f'/nobackup/mazharul/{breach_fname}.{N}.{bl}.{k}.variations.trie')
    pass_trie.load(f'/nobackup/mazharul/{breach_fname}.{N}.{bl}.{k}.variations.trie')
    counts = get_count(DIR, breach_fname, N, bl, pass_trie, k, BL)
    #print(counts.shape)
    # Load variations and pws array
    numpy_array = np.load(f'/nobackup/mazharul/{breach_fname}.{N}.{bl}.{k}.variations.npz')
    pws_variations = numpy_array['var']
    pws = numpy_array['pws']
    pws_r = numpy_array['pws_r']

    # Create balls and writing to a file.
    
    ball_fname = f'/nobackup/mazharul/{breach_fname}.{N}.{bl}.{k}.balls.txt'
    if  os.path.exists(ball_fname) and PRE:
        print('Already exists just loading the password balls...')
        with open(ball_fname, 'rb') as handle:
                ball_reverse = pickle.load(handle)
    else:
        print('Creating password balls...')
        ''' I think using shelves to save the `ball_reverse` would be better '''
        ball_reverse = build_ball_reverse(pws, pws_variations)
        with open(ball_fname, 'wb') as handle:
                pickle.dump(ball_reverse, handle, pickle.HIGHEST_PROTOCOL)
    
    print('Done with creating password balls')
    return 
    '''
    Blocklisted pws are inside ball_reverse and pws_variaitons array.
    The way they do not contribute to the weight of the pw ball is by 
    eleminatng them in get_count function. 
    '''
 
    
    
    # Given a list of pws generate the password sum?
    password_sum_fname = f'/nobackup/mazharul/{breach_fname}.{N}.{bl}.{k}.password_sum.npy'
    if  os.path.exists(password_sum_fname) and PRE:
        password_sum = np.load(password_sum_fname)
    else:
        '''
        Do not use save use np.savez_compressed.
        '''
        password_sum = build_password_sum(pass_trie, ball_reverse, counts)
        np.save(password_sum_fname, password_sum)

        
    #generate greedy guess ranks.
    budget = 0
    
    
    while budget < qc:
        max_ps = password_sum.argmax()
        guess = pass_trie.restore_key(max_ps)
        
        #np.savez_compressed(f'/nobackup/mazharul/{breach_fname}.{N}.{bl}.{k}.{budget}.password_sum.npz', guess=guess, password_sum=password_sum)
        # TODO: improve this there are too many files.
        np.savez_compressed(f'{DIR}/Guess/{breach_fname}.{N}.{bl}.{k}.{budget}.password_sum.npz', guess=guess) #password_sum=password_sum) # Takes 70M space!
        
        if budget < 30:
            print('Guess rank = {}; Guess pws {}; Weight of the ball of is {}'.format(budget, guess, password_sum.max()))
        
        # update the pass_distribution.
        for uid in ball_reverse[max_ps]:
            password_sum[uid] = 0
            uid_idx = pws_r[uid]
            if uid_idx == -1: continue # Does not have any variaitons i.e., outside top N passwords.
            for vid in pws_variations[uid_idx]:
                password_sum[vid] -=  counts[uid]
        
        password_sum[max_ps] = 0
        for vid in pws_variations[pws_r[max_ps]]:
                password_sum[vid] -=  counts[max_ps]
        '''
        if guess in BL:
            print('Error should not get an blocklisted password while guessing...')
            exit(1)
        '''        
        budget +=1
    return 
        
DIR = Path("/pwdata/mazharul/password_research_dataset_Jan/")
breach_fname = 'mixed_full_leak_data_40_1_with-pws-counts.txt'
fname = DIR / breach_fname

N = int(1e6)
if __name__ == '__main__':
    get_guess_ranks(opt.bl, opt.k, opt.qc)
        
