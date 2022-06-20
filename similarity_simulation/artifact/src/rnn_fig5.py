import json 

print("---------rnn------------")
FILE_LIST = ['../test_files/rnn_attack.txt']
N_VALUES = [10,20,30,40,50,60,70,80,90,100]
RNN_PRED_LIST = '../models/pass2path_pred_rnn_attack.txt.predictions'
preds = {}
file_rnn_preds = RNN_PRED_LIST
for pred_line in open(file_rnn_preds,'r'):
    ori_1, p_list = pred_line.split('\t')
    predictions_and_scores = json.loads(p_list)
    predictions = [pred[0] for pred in predictions_and_scores]
    preds[ori_1] = predictions
            
for n in N_VALUES:
   
    for i in range(1):
        c = 0
        t = 0
        filename = FILE_LIST[i]
        file_r = open(filename,'r')
        
        for line in file_r:

            t = t + 1
            words = line.strip().split('\t')
            if words[0] not in preds:
                continue
            if words[1] in preds[words[0]][:n]:
                c = c + 1
        
        file_r.close()   
        
        print("n = "+str(n)+" Accuracy ="+ str((c*100)/t))