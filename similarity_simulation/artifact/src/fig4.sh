#!/bin/bash

echo "----DAS2014----"
g++ NDSS2014_openVersion.cpp -o das2014 && chmod +x das2014
echo "True Positives"
./das2014 ../test_files/rnn_attack_das.txt 10
echo "False Positives"
./das2014 ../test_files/su_attack.txt 10
echo "True Positives"
./das2014 ../test_files/rnn_attack_das.txt 100
echo "False Positives"
./das2014 ../test_files/su_attack.txt 100

rm das2014

python dasr_fig4.py
python wEdit_fig4.py
python rnn_fig4.py
python PPSM_fig_4.py
