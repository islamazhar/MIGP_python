from helper import *

print("---------dasr------------")
FILE_LIST = ['../test_files/rnn_attack.txt','../test_files/su_attack.txt']
N_VALUES = [10,100]

for n in N_VALUES:
    print("n or m = "+str(n))
   
    for i in range(2):
        c = 0
        t = 0
        filename = FILE_LIST[i]
        file_r = open(filename,'r')
        
        for line in file_r:

            t = t + 1
            words = line.strip().split('\t')
            tweaks = get_tweaks_rules_dasr(words[0],n)

            if words[1] in tweaks:
                c = c + 1
        
        file_r.close()   
        if i == 0:
            print("True Positives-"+ str((c*100)/t))
        else:
            print("False Positives-"+ str((c*100)/t))

N_HYBRID_VALUES = [10]
for n in N_HYBRID_VALUES:
    print("n and m = "+str(n))
    
    for i in range(2):
        c = 0
        t = 0
        filename = FILE_LIST[i]
        file_r = open(filename,'r')
        for line in file_r:
            t = t + 1
            words = line.strip().split('\t')
            
            tweaks_1 = get_tweaks_rules_dasr(words[0],n)
            tweaks_2 = get_tweaks_rules_dasr(words[1],n)
            if words[1] in tweaks_1:
                c = c + 1
            else:
                if words[0] in tweaks_2:
                    c = c + 1
                else:
                    if set(tweaks_1).intersection(set(tweaks_2)):
                        c = c + 1
        file_r.close()   
        if i == 0:
            print("True Positives-"+ str((c*100)/t))
        else:
            print("False Positives-"+ str((c*100)/t))

### Greedy Hybrid approach ####

with open('../models/count_dasr_hybrid.json') as f:
    count_dasr_hybrid = [tuple(x) for x in json.load(f)]
    
c_var = [] #client variants
s_var = [] #server variants
max_len = 10
for elem in count_dasr_hybrid:
    if len(c_var) == max_len and len(s_var) == max_len:
        break
    if len(c_var) < max_len:
        if elem[0][0] not in c_var:
            c_var.append(elem[0][0])
    if len(s_var) < max_len:
        if elem[0][1] not in s_var:
            s_var.append(elem[0][1])
            
def get_tweaks_rules_hybrid(word,n,htype):
    tweaks = set()
    MAX_TWEAKS = n
    if htype == 0:
        elems = c_var
    else:
        elems = s_var
    for elem in elems:
        if len(tweaks) == MAX_TWEAKS:
            break
        tw = apply_rule(word,rules[elem])   
        if tw == word:
            continue
        else:
            tweaks.add(tw)
   
    return(list(tweaks))

for n in N_HYBRID_VALUES:
    print("n and m = "+str(n) +"(Greedy approach)")
   
    for i in range(2):
        c = 0
        t = 0
        filename = FILE_LIST[i]
        file_r = open(filename,'r')
      
        for line in file_r:
            words = line.strip().split('\t')

            t = t + 1
            tweaks_c = get_tweaks_rules_hybrid(words[0],n,0)
            tweaks_s = get_tweaks_rules_hybrid(words[1],n,1)
            if words[1] in tweaks_c:
                c = c + 1
                continue
            else:
                if words[0] in tweaks_s:
                    c = c + 1
                    continue
                else:
                    if len(set(tweaks_c).intersection(set(tweaks_s)))>0:
                        c = c + 1
                        continue
        file_r.close()   
        if i == 0:
            print("True Positives-"+ str((c*100)/t))
        else:
            print("False Positives-"+ str((c*100)/t))