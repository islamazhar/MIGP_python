#!/bin/bash
set -xe
for k in 100
do
    for bl in 0 10 100 1000 10000
    do
        python3  get_variations.py --bl  $bl --k $k
        # [PLEASE]: do not run multiple instances of this command simultaneously. 
        # You may get memory error by doing so since  the code inside 
        # `get_variations.py` is already parallelize.  
    done
done