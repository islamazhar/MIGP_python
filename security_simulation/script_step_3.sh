#!/bin/bash
set -xe


max_threads=2
cur_theads=0
for k in $1
do
    for qc in  $2
    do
        for bl in 0 10 100 1000 10000
        do
            if [ $max_threads -eq $cur_theads ] 
            then 
                wait #wait for all threads to finish.
                cur_theads=0 
            fi 
            if [ $k -eq 0 ] 
            then 
                python3  Normal.py --bl  $bl --k $k --qc $qc&
            else 
                python3  MIGP.py --bl  $bl --k $k --qc $qc&
            fi
            cur_theads=`expr $cur_theads + 1`
        done
    done
done
wait