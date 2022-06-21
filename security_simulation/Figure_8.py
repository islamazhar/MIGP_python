import sys
sys.path.append("..")
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#plt.style.use('seaborn-whitegrid')

fname = '../results/security_simulation.tsv'
names = ["k", "bl", "qc", "success", "std"]
df = pd.read_csv(fname, names=names, sep='\t')
#print(df)
results = [ ["bl", "k", "qc=10", "qc=100", "qc=1000"] ]
results.append("linebreak")  

for bl in [0, 10, 100, 1000, 10000]:
    for k in [0, 10,100]:
        line = []
        if  k == 0:
            line.append(bl)
        else:
            line.append(" ")
        line.append(k)    
        for qc in [10, 100, 1000]:
            val = df[(df["k"] ==k) & (df["bl"] == bl) & (df["qc"] == qc)]
            #print(val.iloc[0]["success"], val.iloc[0]["std"] ) 
            if len(val) == 1:
                line.append("{:.2f} ± {:.2f}".format(val.iloc[0]["success"],val.iloc[0]["std"]))
            else:
                line.append("-")
        results.append(line)
    results.append("linebreak")        

for result in results:
    # if len(result) == 3:
    #     print(result)
    if result == "linebreak":
        print("===========================================================================================")
    else:
        print("".join(format(str(x), '<20')  for x in result))

                             
                
