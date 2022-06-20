import json

print("---------p2p------------")
FILE_LIST = ['../test_files/rnn_attack.txt','../test_files/su_attack.txt']
N_VALUES = [10,100]
RNN_PRED_LIST = ['../models/pass2path_pred_rnn_attack.txt.predictions',
                 '../models/pass2path_pred_su_attack.txt.predictions']

                    
for n in N_VALUES:
    print("n or m = "+str(n))
   
    for i in range(2):
        preds = {}
        file_rnn_preds = RNN_PRED_LIST[i]
        for pred_line in open(file_rnn_preds,'r'):
            ori_1, p_list = pred_line.split('\t')
            predictions_and_scores = json.loads(p_list)
            predictions = [pred[0] for pred in predictions_and_scores]
            preds[ori_1] = predictions
        c = 0
        t = 0
        filename = FILE_LIST[i]
        file_r = open(filename,'r')
        
        for line in file_r:
 
            words = line.strip().split('\t')
            if words[0] not in preds:
                continue
            if words[1] in preds[words[0]][:n]:
                c = c + 1
            t = t + 1
        print(t,c)
        file_r.close()   
        if i == 0:
            print("True Positives-"+ str((c*100)/t))
        else:
            print("False Positives-"+ str((c*100)/t))