import ast
import json
preds= {}
test_cases = set()
file_r1 = open('../models/pass2path_1667500_test_full_email_100000.txt.predictions','r')
file_r2 = open('../test_files/test_full_email_10000.txt')
import pdb


for test_line in file_r2:
    ori_test, target = test_line.strip().split('\t')
    test_cases.add(ori_test)
file_r2.close()    
for pred_line in file_r1:
    ori, p_list = pred_line.split('\t')
    if ori in test_cases:
        predictions_and_scores = json.loads(p_list)
        predictions = [pred[0] for pred in predictions_and_scores]
        preds[ori] = predictions

print("Exact Check")
for pred_c in [10,100,1000]:
    total = 0
    count = 0
    for test_line in open('../test_files/test_full_email_10000.txt'):
        total = total + 1

        ori_test, target = test_line.strip().split('\t')
        if ori_test not in preds:
            continue
        if target in preds[ori_test][:pred_c]:
            count = count + 1
    print("q - "+str(pred_c)+", Test accuracy - "+str((count*100)/total))
