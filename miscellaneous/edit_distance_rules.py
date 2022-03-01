# coding: utf-8
#!/usr/bin/env python3
import sys
sys.path.append("..")

import json
import os

from word2keypress import Keyboard
from ast import literal_eval
from miscellaneous.utilities import filter_ws
from miscellaneous.hash_functions import get_random_string

kb = Keyboard()
dir_path = os.path.dirname(os.path.realpath(__file__))


def path2word_kb_feasible(word, path, print_path=False):
    '''
    This function decodes the word in which the given path transitions the input word into.
    This is the KeyPress version, which handles the keyboard representations.
    If one of the parts components is not feasible (e.g removing a char from out of range index), it skips it
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


def _apply_edits(wordkeyseq, path):
    """A slightly faster variant of path2word_kb_feasible. Good to be used from tweaking_rules.
    @wordkeypress: key-press representation of the word
    @path: an array of edits
    """
    word = wordkeyseq
    if not path:
        return kb.keyseq_to_word(word)
    final_word = []
    word_len, path_len = len(word), len(path)
    i, j = 0, 0
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
    return kb.keyseq_to_word(''.join(final_word))
    

# load the transformation rules and their count
with open(dir_path+'/transition_count_1_index.json') as f:
    count = json.load(f)
count_sort_1 = sorted(count.items(), key=lambda kv: kv[1], reverse = True)

with open(dir_path+'/transition_count_2_index.json') as f:
    count = json.load(f)
count_sort_2 = sorted(count.items(), key=lambda kv: kv[1], reverse = True)

with open(dir_path+'/transition_count_3_index.json') as f:
    count = json.load(f)

# take top 200 from paths of length 1,2 and 3 and sort them based on count
count_sort_3 = sorted(count.items(), key=lambda kv: kv[1], reverse = True)

temp_cs = count_sort_1[:200] + count_sort_2[:200] + count_sort_3[:200]
temp_cs_sort = sorted(temp_cs, key=lambda kv: kv[1], reverse = True)
rules_list = temp_cs_sort


# function to get n tweaks for a word
P_LIST = []
def get_tweaks_rules(word, K, BL=[]):

    tweaks = set()
    global P_LIST
    if not P_LIST:
        for pathstr, f in rules_list:
            edits = pathstr.split('+')
            path_list = []
            for e in edits:
                path = literal_eval(e)
                if path[2]<0:
                    path = (path[0], path[1], path[2]+(len(word)+1))
                path_list.append(path)
            P_LIST.append(path_list)
            if len(P_LIST) > 10 * K:
                #print(f"P_LIST size {len(P_LIST)}")
                break
    MAX_TWEAKS = K
    wordkeyseq = kb.word_to_keyseq(word)
    for p in P_LIST:
        tw = _apply_edits(wordkeyseq, p)
        if tw != word and tw not in BL and filter_ws(tw):
            tweaks.add(tw)
        if len(tweaks) >= MAX_TWEAKS:
            break
    #assert len(list(tweaks)) == MAX_TWEAKS, f'Can not generate {MAX_TWEAKS}; generated {len(list(tweaks))}'
    while len(list(tweaks)) < MAX_TWEAKS:
        tweaks.add(get_random_string(6))
    return list(tweaks)