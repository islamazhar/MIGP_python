rm -rf performance_simulation_results.csv # add a if condition to check if file exists
echo -e "col_type\ttime" >> ../results/performance_simulation.csv
# serverURL="http://13.58.12.89"
serverURL="http://0.0.0.0"
timelogging=1


# IDB-16(GPC), IDB-20
serverPORT=8774
for prefix_len in 16 20
do
        for rate_limiting in 0 1
        do
                for i in {1..1}
                do
                        python3 IDB_client.py --username Alice --password 123456 --serverURL $serverURL --serverPORT $serverPORT --prefix_len $prefix_len --rate_limiting $rate_limiting --timelogging $timelogging
                done
        done 
done
# # MIGP-Server l = 20
# serverPORT=8774 #n=100
# prefix_len=20
# echo "MIGP-Server,20" >> ../results/performance_simulation.csv
# for rate_limiting in 0 1
# do
#                 for i in {1..1}
#                 do
#                         python3 MIGP_client.py --username Alice --password 123456 --serverURL $serverURL --serverPORT $serverPORT --prefix_len $prefix_len --rate_limiting $rate_limiting --timelogging $timelogging
#                 done
# done 
# # MIGP-Client l = 16
# serverPORT=8775 #n=100
# for prefix_len in 16 20
# do
#         echo "MIGP-Client,$prefix_len" >> ../results/performance_simulation.csv
#         for rate_limiting in 0 1
#                 do
#                         for i in {1..25}
#                         do
#                                 python3 MIGP_client.py --username Alice --password 123456 --serverURL $serverURL -- serverPORT $serverPORT --prefix_len $prefix_len --rate_limiting $rate_limiting --timelogging $timelogging
#                         done
#                 done
#         done 
# done


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

