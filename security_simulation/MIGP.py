import sys
sys.path.append("..")
sys.setrecursionlimit(10000)

import numpy as np
#import pickle
import pickle5 as pickle
import marisa_trie
import itertools
import copy

from multiprocessing import Pool
from pathlib import Path

from miscellaneous.utilities import get_pws_variations_serial, get_block_list, filter_ws, write_results
from security_simulation.get_variations import parse_args
from security_simulation.get_guess_ranks  import get_count

PRE = False
opt = parse_args()

''' parameters '''
bl = opt.bl
qc = opt.qc
k = opt.k
N = int(1e6)

''' file locations '''
# DIR = Path("/pwdata/mazharul/password_research_dataset_Jan/")
DIR = Path("data_files/")
breach_fname = 'mixed_full_leak_data_40_1_with-pws-counts.txt'
target_fname = DIR/f'target_pws_25000.S2.txt'
leak_fname = DIR / breach_fname


''' global vars '''
ball_fname = f'data_files/{N}.{bl}.{k}.balls.txt'
print(ball_fname)
with open(ball_fname, 'rb') as handle: ball_reverse = pickle.load(handle)
print("Done loading file")
pass_trie = marisa_trie.Trie()
pass_trie.load(f'data_files/variations/{N}.{bl}.{k}.variations.trie')
BL =  get_block_list(leak_fname, k, bl)
count_array = get_count(DIR, breach_fname, N, bl,pass_trie,k,BL)
numpy_array = np.load(f'data_files/variations/{N}.{bl}.{k}.variations.npz')
pws_variations = numpy_array['var']

def get_last_guess(guess_list):
    ''' get the last guess outside of guess_list'''
    fname = DIR / breach_fname
    with open(fname) as f:
        for l in f:
            ll = l.rstrip('\n').split('\t')
            if len(ll) != 2: continue
            _, w = ll[0], ll[1]
            if filter_ws(w) and  w not in guess_list:
                return w
    return '123456'
                
                

def MIGP_inside_ball(rbudget, tpw, candidate_pws, tvariations, not_pws):
    if rbudget == 0 or len(candidate_pws) == 0:
        return get_last_guess(not_pws)
        
    
    password_sum = np.zeros(len(pass_trie), dtype=np.int32)
    for uid in candidate_pws:
        weight = count_array[uid]
        if uid in ball_reverse:        
            weight += count_array[list(set(ball_reverse[uid]) & candidate_pws)].sum()
        password_sum[uid] = weight
        
    if password_sum.max() == 0:
        ''' This corresponds to all the `pws` inside  `candidate_pws` sum have zero count (i.e., a variation leak pws) '''
        for i,can in enumerate(candidate_pws):
            if i < rbudget: 
                if tpw == can:
                    return tpw
            else: 
                return can
        
        return get_last_guess(not_pws)
            
            #return list(candidate_pws)[0]    
        
    max_ps = password_sum.argmax()
    guess = pass_trie.restore_key(max_ps)        
    #print(guess, rbudget, len(candidate_pws))

    if guess == tpw:
        return guess
    else:
        not_pws.add(guess)
        candidate_pws.remove(max_ps)
        return MIGP_inside_ball(rbudget-1, tpw, candidate_pws, tvariations, not_pws)

    # TODO: Get an statistics on which password can get inside the ball of the target password but can not guess....
    # TODO: Attacker already know the top 1000 passwords..right?
    # TODO: Use the password sorting mechanism
        
def MIGP(tpws, qc, BL):
    
    not_pws = set()
    tvariations = dict() 
    for tpw in tpws:
        tvariations[tpw] = get_pws_variations_serial(tpw, k, BL)
        
    success = np.zeros((len(tpws)), dtype=bool)
    
    with open(f'data_files/guess_ranks/{bl}.{k}.1000', 'rb') as handle:
                guesses = pickle.load(handle)
                
    print('Starting MIGP....')       
    for budget in range(qc):
        
        guess = guesses[budget]
        #password_sum = np_array['password_sum']
        print(f'Guess rank = {budget}; Guess pw = {guess}')
        
        for i,tpw in enumerate(tpws):
            if guess == tpw and success[i] == False:
                #print(f'Success; Guess Rank = {budget}; Guess pw = {tpw}')
                success[i] = True
            if guess in tvariations[tpw] and success[i] == False:
                    # Inside ball of the target pw. create the pw ball again.
                    rbudget = qc - budget # remaining budget
                    candidate_pws = set([ pw for pw in ball_reverse[pass_trie[guess]] if pw not in not_pws]) - set([pass_trie[guess]])  
                    #print(f'Going inside the ball for  guess={guess}')
                    not_pws_copy = copy.deepcopy(not_pws)       
                    guess_inside_the_ball = MIGP_inside_ball(rbudget, tpw, candidate_pws, tvariations[tpw], not_pws_copy)
                    if guess_inside_the_ball == tpw:
                        #print(f'Success after inside the MIGP ball...for pw={tpw} in rank={budget}')
                        success[i] = True  
        not_pws.add(guess)
        not_pws.update(ball_reverse[pass_trie[guess]])
            
        print(f'attack sucess after {budget} guess is = {success.sum()}')
    #print(f'No success for target pw = {tpw}')
    ttpw = get_last_guess(not_pws)
    print(f' Last password guess is {ttpw}')
    
    for i, tpw in enumerate(tpws):
        if tpw == ttpw:
            success[i] = True
    
    return success

 
if __name__ == '__main__':
    with open(target_fname, 'r') as f:
        tpws = [w.strip('\n') for w in f]
        print(f'Size of the target pws = {len(tpws)}')
        success = MIGP(tpws, qc, BL) 
        write_results(success, tpws, qc, bl, k)