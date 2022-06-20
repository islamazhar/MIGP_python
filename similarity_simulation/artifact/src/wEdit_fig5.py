from helper import *
count = {}
print("---------wEdit------------")
FILE_LIST = ['../test_files/rnn_attack.txt']
N_VALUES = [10,20,30,40,50,60,70,80,90,100]

for n in N_VALUES:
    for i in range(1):
        c = 0
        t = 0
        filename = FILE_LIST[i]
        file_r = open(filename,'r')
        for line in file_r:
            t = t + 1
            words = line.strip().split('\t')
            tweaks = get_tweaks_rules_edr(words[0],n)

            if words[1] in tweaks:
                c = c + 1
        file_r.close()   
        
        print("n = "+str(n)+" Accuracy ="+ str((c*100)/t))
       
            