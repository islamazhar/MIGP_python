#!/bin/bash
#set -xe
max_threads=$1
cur_theads=0
for k in 100
do
    for qc in  $2
    do
        for bl in 0 10 100 1000 10000
        do
            cur_theads=`expr $cur_theads + 1`
            if [ $max_threads -eq $cur_theads ] 
            then 
                wait
                cur_theads=0  
            elif [ $k -eq 0 ] 
            then 
                echo python3  Normal.py --bl  $bl --k $k --qc $qc&
            else 
                echo python3  MIGP.py --bl  $bl --k $k --qc $qc&
            fi
        done
    done
done

python3 Figure_8.py
# Add a screen-shot.