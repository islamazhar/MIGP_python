set -xe 
for bl in  100 1000 10000
do 
    python3  sample_pws.py --bl  $bl&
done
wait