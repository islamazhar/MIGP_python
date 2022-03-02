echo "" > ../results/performance_simulation_results.tsv # add a if condition to check if file exists

# IDB-16(GPC), IDB-20
# serverURL="http://13.58.12.89"
serverURL="http://13.58.12.89"
timelogging=1

# serverPORT=8181
# prefix_len=16
# echo -e  "Method\tIDB-$prefix_len" >> ../results/performance_simulation.tsv
# for rate_limiting in 0 1
# do
#         for i in {1..5}
#         do
#                 python3 IDB_client.py --username Alice --password 123456 --serverURL $serverURL --serverPORT $serverPORT --prefix_len $prefix_len --rate_limiting $rate_limiting --timelogging $timelogging
#         done
# done 
# echo "Done IDB-16"
# serverPORT=8182
# prefix_len=20
# echo -e  "Method\tIDB-$prefix_len" >> ../results/performance_simulation.tsv
# for rate_limiting in 0 1
# do
#         for i in {1..5}
#         do
#                 python3 IDB_client.py --username Alice --password 123456 --serverURL $serverURL --serverPORT $serverPORT --prefix_len $prefix_len --rate_limiting $rate_limiting --timelogging $timelogging
#         done
# done 
# echo "Done IDB-20"

# # # MIGP-Server l = 20
# serverPORT=8183 #n=100
# prefix_len=20
# echo -e "Method\tMIGP-Server-20" >> ../results/performance_simulation.tsv
# for rate_limiting in 0 1
# do
#         for i in {1..5}
#         do
#                 python3 MIGP_client.py --username Alice --password 123456 --serverURL $serverURL --serverPORT $serverPORT --prefix_len $prefix_len --rate_limiting $rate_limiting --timelogging $timelogging
#         done
# done
# echo "Done MIGP-Server l = 20" 
# # # MIGP-Client l = 16
# serverPORT=8184 #n=100
# prefix_len=16
# echo -e "Method\tMIGP-Client-$prefix_len" >> ../results/performance_simulation.tsv
# for rate_limiting in 0 1
# do
#         for i in {1..5}
#         do
#                 python3 MIGP_client.py --username Alice --password 123456 --serverURL $serverURL --serverPORT $serverPORT --prefix_len $prefix_len --rate_limiting $rate_limiting --timelogging $timelogging --n 100
#         done
# done
echo "Done MIGP-Client l=16"
# # MIGP-Client l = 20
serverPORT=8183 #n=100
prefix_len=20
echo -e "Method\tMIGP-Client-$prefix_len" >> ../results/performance_simulation.tsv
for rate_limiting in 0 1
do
        for i in {1..5}
        do
                python3 MIGP_client.py --username Alice --password 123456 --serverURL $serverURL --serverPORT $serverPORT --prefix_len $prefix_len --rate_limiting $rate_limiting --timelogging $timelogging --n 100
        done
done
# echo "Done MIGP-Client l = 20"


# #MIGP-Hybrid l = 20
# serverPORT=8776 #n=100
# for prefix_len in 20
# do
#         echo "MIGP-Hybrid,$prefix_len" >> ../results/performance_simulation.csv
#         for rate_limiting in 0 1
#                 do
#                         for i in {1..25}
#                         do
#                                 python3 MIGP_client.py --username Alice --password 123456 --serverURL $serverURL -- serverPORT $serverPORT --prefix_len $prefix_len --rate_limiting $rate_limiting --timelogging $timelogging
#                         done
#                 done
#         done 
# done

# # WR19-Bllom
# # WR20-Cuckoo
echo -e  "Method\tFinish!" >> ../results/performance_simulation.tsv
# Generate the Figure 11
python3 Figure_11.py
