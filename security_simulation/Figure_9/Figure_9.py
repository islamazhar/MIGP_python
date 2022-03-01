import numpy as np
import matplotlib.pyplot as plt
#plt.style.use('seaborn-whitegrid')

fname = 'success_rates_log.tsv'

Y1 = np.zeros(1002)
Y2 = np.zeros(1002)
Y3 = np.zeros(1002)
Y4 = np.zeros(1002)
BL = 0
K = 10
with open(fname, 'r') as fin:
    for l in fin:
        id, in1, in2, bl, k = [int(x) for x in l.strip('\n').split('\t')]
        if bl != BL: continue
        if k == 100:
            Y1[in1] += 1
            Y2[in2] += 1

        else:
            Y3[in1] +=1
            Y4[in2] +=1

for i in range(2,1002):
    Y1[i] += Y1[i-1]
    Y2[i] += Y2[i-1]
    Y3[i] += Y3[i-1]
    Y4[i] += Y4[i-1]

# print(Y1[0:20])
#print(Y2[0:20])
      
YY1 = [Y1[i]/250 for i in range(1, 1002, 50)]
YY2 = [Y2[i]/250 for i in range(1, 1002, 50)]
YY3 = [Y3[i]/250 for i in range(1, 1002, 50)]
YY4 = [Y4[i]/250 for i in range(1, 1002, 50)]

# plt.plot(range(1,1002, 50), YY1, marker='v', label='Inside ball, k=100', color='red')
plt.plot(range(1,1002, 50), YY2, marker='D', label='n=100', color='red')
# plt.plot(range(1,1002, 50), YY3, marker='x', label='Inside ball, k=10', color='black')
#plt.plot(range(1,1001, 50), YY4, 'o', label='success, k=10')
plt.plot(range(1,1002, 50), YY4, marker='o', label='n=10', color='blue')

plt.legend(loc="lower right")
plt.grid(True, linestyle="--", linewidth='0.5')
plt.xlabel('Guess budget q')
plt.ylabel('Attack success rate %')
plt.ylim([0, 20])
plt.savefig(f'Figure_9.jpg', format = 'jpg', dpi = 500)
#plt.show()

# import tikzplotlib
# tikzplotlib.save("Figure_8.tex")
