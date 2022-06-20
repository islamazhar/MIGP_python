import sys
sys.path.append("..")
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#plt.style.use('seaborn-whitegrid')

fname = '../results/performance_simulation.tsv'
names = ["col_type", "time"]
df = pd.read_csv(fname, names=names, sep='\t')
# print(df)
column_names = ["Method", "B/w (MB)", "Query Prep. w/o rate limit", "Query Prep. w/ rate limit", "API call", "Finalize", "total_w/o rate limit", "total_w/ rate limit"]
# print("".join(x.ljust(30) for x in column_names))
cur_line = {}
dff = {}
# for col in column_names:
#     dff[col] = []
for col, val in zip(df["col_type"], df["time"]):
    if col == "Method":
        #print(val)
        if len(cur_line.keys()) > 0:
            # print the line
            print(cur_line)
            for  col_name in column_names:
                if col_name == "Method":
                    if col_name == "Finish!": break
                    #print(cur_line["Method"])
                    #print("Method = ", cur_line["Method"])
                    dff[cur_line["Method"]] = []
                else:
                    print(col_name)
                    res = np.array(cur_line[col_name])
                    dff[cur_line["Method"]].append(np.mean(res))
                    #print(res)
                    #print("{} = {:.2f}".format(col_name, np.mean(res)))
                    
            #print("=================================================================")
        cur_line.clear()
        cur_line["Method"] = val
            
    else:
        if col not in cur_line.keys():
            cur_line[col] = []
        cur_line[col].append(float(val))

#print(dff)
pd.options.display.float_format = "{:,.2f}".format
dff = pd.DataFrame.from_dict(dff, orient='index', columns=column_names[1:len(column_names)])
print(dff)

                             
                
