#!/bin/bash
set -xe
for k in 100
do
    for qc in  1000 
    do
        for bl in 0 10 100 1000 10000
        do 
            python3  get_guess_ranks.py --bl  $bl --k $k --qc $qc
        done
    done 
done