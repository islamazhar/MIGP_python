#!/bin/bash

echo "----DAS2014----"
g++ NDSS2014_openVersion.cpp -o das2014 && chmod +x das2014
./das2014 ../test_files/rnn_attack_das.txt 10
./das2014 ../test_files/rnn_attack_das.txt 20
./das2014 ../test_files/rnn_attack_das.txt 30
./das2014 ../test_files/rnn_attack_das.txt 40
./das2014 ../test_files/rnn_attack_das.txt 50
./das2014 ../test_files/rnn_attack_das.txt 60
./das2014 ../test_files/rnn_attack_das.txt 70
./das2014 ../test_files/rnn_attack_das.txt 80
./das2014 ../test_files/rnn_attack_das.txt 90
./das2014 ../test_files/rnn_attack_das.txt 100

rm das2014

python dasr_fig5.py
python wEdit_fig5.py
python rnn_fig5.py
