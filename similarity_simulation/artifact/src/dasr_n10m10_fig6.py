from helper import *
import ast
#pred_c = 1000

preds= {}
test_cases = set()
file_r1 = open('../models/pass2path_1667500_migp_attack_dasr_100.txt.predictions','r')
file_r2 = open('../test_files/migp_attack_dasr_g.txt')
import pdb
for test_line in file_r2:
    
    orig_2, target,guesses = test_line.strip().split('\t')
    test_cases.add(orig_2)

for pred_line in file_r1:
    ori_1, p_list = pred_line.split('\t')
    if ori_1 in test_cases:
        predictions_and_scores = json.loads(p_list)
        predictions = [pred[0] for pred in predictions_and_scores]
        preds[ori_1] = predictions

print("Das-R n = 10 and m = 10")
for pred_c in [10, 100, 1000]:
    count = 0
    total = 0
    for test_line in open('../test_files/migp_attack_dasr_g.txt'):

        orig_2, target, guesses = test_line.strip().split('\t') 
        migp_p = ast.literal_eval(guesses)
        pred_final = []
        p = 0
        if orig_2 not in preds:
            continue
        for elem in preds[orig_2]:
            if p == pred_c:
                break
           # pred_final.append(elem)
           # p = p + 1 

            if elem == '':
                continue
            if elem not in set(migp_p) and len(set(get_tweaks_rules_dasr(elem,10)).intersection(set(migp_p)))==0:
                pred_final.append(elem)
                p = p + 1      

        if target in set(pred_final):
            count = count+ 1
        total = total +1 

    print("q - "+str(pred_c)+", Test accuracy - "+str((count*100)/total))
