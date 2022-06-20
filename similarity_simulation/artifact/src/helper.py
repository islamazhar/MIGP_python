from collections import Counter
import csv
import string
import json

### Dasr rules ##############


lower = string.ascii_lowercase
upper = string.ascii_uppercase
rules = []
#bigram = ['08','01','07','23','06','09','12','05','21','04','11','22','02','13','03','69','00','10','88','20']
trigram = ['123','087','007','083','084','089','086','666','085','man','143','boy','321','101','420','456','000','001','777','ita']
leet = [('0','o'),('a','@'),('7','t'),('3','e')]
subs = [('qwer','1234'),('qwer','1qaz'),('qwe','qaz'),('qwe','qwer'),('asd','asdf'),('asd','wsx'),('wsx','2wsx'),('wsx','wer'),
       ('asdf','1234'),('asdf','zxcv'),('5678','qwer'),('5678','1234'),('qa','qwe'),('qa','qaz')]
rules.append(('c','none',0))
rules.append(('c','none',0))
rules.append(('d','none',1))
rules.append(('d','none',2))
rules.append(('d','none',3))
rules.append(('d','none',-1))
rules.append(('d','none',-2))
rules.append(('d','none',-3))
for i in range(100):
    rules.append(('i',str(i),0))
    rules.append(('i',str(i),-1))
for i in lower:
    rules.append(('i',i,0))
    rules.append(('i',i,-1))
for i in upper:
    rules.append(('i',i,0))
    rules.append(('i',i,-1))
for i in leet:
    rules.append(('s',i[0],i[1]))
for i in leet:
    rules.append(('s',i[1],i[0]))
for i in subs:
    rules.append(('s',i[0],i[1]))
for i in subs:
    rules.append(('s',i[1],i[0]))
#for i in bigram:
 #   rules.append(('i',i,0))
  #rules.append(('i',i,-1))
for i in trigram:
    rules.append(('i',i,0))
    rules.append(('i',i,-1))
for i in leet:
    rules.append(('s',i[0],i[1]))
    
def apply_rule(word,r):
    tw = word
    
    if r[0] == 'c':
        tw = word.capitalize()
        if word == tw:
            if word[0].isalpha():
                tw = word[:1].lower() + word[1:]
    if r[0] == 'd':
        if r[2]<0:
            tw = word[:r[2]]
        else:
            tw = word[r[2]:]
    if r[0] == 's':
        if r[1] in word:
            tw = word.replace(r[1], r[2])
    if r[0] == 'i':
        if r[2] == 0:
            tw = word+(r[1])
        else:
            tw = r[1]+(word)
    return tw

with open('../models/count_dasr.json') as f:
    count_sort = [tuple(x) for x in json.load(f)]

import pdb
def get_tweaks_rules_dasr(word,n):
    tweaks = set()
    MAX_TWEAKS = n
    for elem in count_sort:
        if len(tweaks) == MAX_TWEAKS:
            break
        tw = apply_rule(word,rules[elem[0]])        
        if tw == word:
            continue
        else:
            tweaks.add(tw)
    #pdb.set_trace()
    return(list(tweaks))

### WEdit rules ##############

import json

with open('/hdd/c3s/tal/transition_count_1_index.json') as f:
    count = json.load(f)
count_sort_1 = sorted(count.items(), key=lambda kv: kv[1], reverse = True)

with open('/hdd/c3s/tal/transition_count_2_index.json') as f:
    count = json.load(f)
count_sort_2 = sorted(count.items(), key=lambda kv: kv[1], reverse = True)

with open('/hdd/c3s/tal/transition_count_3_index.json') as f:
    count = json.load(f)
count_sort_3 = sorted(count.items(), key=lambda kv: kv[1], reverse = True)

temp_cs = count_sort_1[:1000]+count_sort_2[:1000]+count_sort_3[:1000]
temp_cs_sort = sorted(temp_cs, key=lambda kv: kv[1], reverse = True)
rules_list = temp_cs_sort

from word2keypress import Keyboard
kb = Keyboard()
from ast import literal_eval
def path2word_kb_feasible(word, path, print_path=False):
    '''
    This function decodes the word in which the given path transitions the input word into.
    This is the KeyPress version, which handles the keyboard representations.
    If one of the parts components is not
    feasible (e.g removing a char from out of range index), it skips it
    Input parameters: original word, transition path
    Output: decoded word
    '''
    
    word = kb.word_to_keyseq(word)
    if not path:
        return kb.keyseq_to_word(word)
    path = [literal_eval(p) for p in path]
    if (print_path):
        print(path)
   # print(path)
   # print(word)
    final_word = []
    word_len = len(word)
    path_len = len(path)
    i = 0
    j = 0
    while (i < word_len or j < path_len):
        if ((j < path_len and path[j][2] == i) or (i >= word_len and path[j][2] >= i)):
            if (path[j][0] == "s"):
                # substitute
                final_word.append(path[j][1])
                i += 1
                j += 1
            elif (path[j][0] == "d"):
                # delete
                i += 1
                j += 1
            else:
                # "i", insert
                final_word.append(path[j][1])
                j += 1
        else:
            if (i < word_len):
                final_word.append(word[i])
                i += 1
            if (j < path_len and i > path[j][2]):
                j += 1
    return (kb.keyseq_to_word(''.join(final_word)))

import pdb
from ast import literal_eval
def get_tweaks_rules_edr(word,n):
    tweaks = set()
    MAX_TWEAKS = n
    for elem in rules_list:
        if len(tweaks) == MAX_TWEAKS:
            break
        edits = elem[0].split('+')
        path_list = []
        for e in edits:
            path = literal_eval(e)
            if path[2]<0:
                path = (path[0],path[1],path[2]+(len(word)+1))
            path_list.append(str(path))
        tw = (path2word_kb_feasible(word, path_list))
        if tw == word:
            continue
        else:
            tweaks.add(tw)
    return(list(tweaks))

def apply_tweak_edr(word,rule):
   
    elem = rule
    edits = elem[0].split('+')
    path_list = []
    for e in edits:
        path = literal_eval(e)
        if path[2]<0:
            path = (path[0],path[1],path[2]+(len(word)+1))
        path_list.append(str(path))
    tw = (path2word_kb_feasible(word, path_list))
        
    return tw