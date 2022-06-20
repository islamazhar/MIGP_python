set -xe
echo "" > ../results/performance_simulation.tsv # add a if condition to check if file exists

# IDB-16(GPC), IDB-20
# serverURL="http://13.58.12.89"
#serverURL="http://13.58.12.89"
M=1
serverURL="http://0.0.0.0"
timelogging=1
IDBServerPORT=8774
prefix_len=16
# for method in "IDB"
# do 
#         for prefix_len in 16 20: 
#                 echo -e  "Method\t$method-$prefix_len" >> ../results/performance_simulation.tsv
#                 for rate_limiting in 0 1
#                 do
#                         for i in {1..$M}
#                         do
#                                 python3 IDB_client.py --username Alice --password 123456 --serverURL $serverURL --serverPORT $IDBServerPORT --prefix_len $prefix_len --rate_limiting $rate_limiting --timelogging $timelogging
#                         done
#                 done 
#         done
#         echo "Done $method-$prefix_len"
# done

# # echo "Done IDB-16"
# # prefix_len=20
# # echo -e  "Method\tIDB-$prefix_len" >> ../results/performance_simulation.tsv
# # for rate_limiting in 0 1
# # do
# #         for i in {1..$M}
# #         do
# #                 python3 IDB_client.py --username Alice --password 123456 --serverURL $serverURL --serverPORT $IDBServerPORT --prefix_len $prefix_len --rate_limiting $rate_limiting --timelogging $timelogging
# #         done
# # done 

# # echo "Done IDB-20"

# # # MIGP-Server l = 20
# MIGPServerPORT=8183 #n=100
# prefix_len=20
# echo -e "Method\tMIGP-Server-20" >> ../results/performance_simulation.tsv
# for rate_limiting in 0 1
# do
#         for i in {1..$M}
#         do
#                 python3 MIGP_client.py --username Alice --password 123456 --serverURL $serverURL --serverPORT $MIGPServerPORT --prefix_len $prefix_len --rate_limiting $rate_limiting --timelogging $timelogging
#         done
# done
# echo "Done MIGP-Server l = 20" 
# # # MIGP-Client l = 16
# prefix_len=16
# echo -e "Method\tMIGP-Client-$prefix_len" >> ../results/performance_simulation.tsv
# for rate_limiting in 0 1
# do
#         for i in {1..$M}
#         do
#                 python3 MIGP_client.py --username Alice --password 123456 --serverURL $serverURL --serverPORT $MIGPServerPORT --prefix_len $prefix_len --rate_limiting $rate_limiting --timelogging $timelogging --n 100
#         done
# done
# echo "Done MIGP-Client l=16"
# # # MIGP-Client l = 20
# prefix_len=20
# echo -e "Method\tMIGP-Client-$prefix_len" >> ../results/performance_simulation.tsv
# for rate_limiting in 0 1
# do
#         for i in {1..$M}
#         do
#                 python3 MIGP_client.py --username Alice --password 123456 --serverURL $serverURL --serverPORT $MIGPServerPORT --prefix_len $prefix_len --rate_limiting $rate_limiting --timelogging $timelogging --n 100
#         done
# done
# # echo "Done MIGP-Client l = 20"


# #MIGP-Hybrid l = 20
# prefix_len=20
# echo "MIGP-Hybrid,$prefix_len" >> ../results/performance_simulation.csv
# for rate_limiting in 0 1
# do
#         for i in {1..$M}
#         do
#                 python3 MIGP_client.py --username Alice --password 123456 --serverURL $serverURL --serverPORT $MIGPServerPORT --prefix_len $prefix_len --rate_limiting $rate_limiting --timelogging $timelogging
#         done
# done


# WR19-Bloom
prefix_len=20
setSize=10 # Extrapolated setSize from Table from our paper.
echo "WR19-Bloom,$prefix_len" >> ../results/performance_simulation.csv
cd WR-19-20/pmt-go
for rateLimiting in 0 1
do
        for i in {1..$M}
        do
                go run WR_19.go -keyLength=256 -setSize=$setSize -numThreads=1 -enablePC=true -requesterInput="Simba" -rateLimiting=$rateLimiting
        done
done

# WR20-Cuckoo
echo "WR20-Cuckoo,$prefix_len" >> ../results/performance_simulation.csv
for rateLimiting in 0 1
do
        for i in {1..$M}
        do
                go run WR_20.go -keyLength=256 -setSize=$setSize -numThreads=1 -enablePC=true -requesterInput="Simba" -rateLimiting=$rateLimiting
        done
done

echo -e  "Method\tFinish!" >> ../results/performance_simulation.tsv
# Generate the Figure 11
cd ../..
python3 Figure_11.py