set -e
echo "" > ../results/performance_simulation.tsv # add a if condition to check if file exists
IDBServerPORT1=8774
IDBServerPORT2=8775

MIGPServerPORT1=8183 #n=100
MIGPServerPORT2=8184 #n=100

# IDB-16(GPC), IDB-20
# serverURL="http://13.58.12.89"
#serverURL="http://13.58.12.89"
M=1 #don't need to run it many times since it is on localhost. 
serverURL="http://0.0.0.0"
timelogging=1
prefix_len=16
for method in "IDB"
do 
        for prefix_len in 16 20
        do 
                echo -e  "Method\t$method l=$prefix_len" >> ../results/performance_simulation.tsv
                for rate_limiting in 0 1
                do
                        if [[ prefix_len -eq 16 ]]
                        then
                                IDBServerPORT=$IDBServerPORT1
                        else
                                IDBServerPORT=$IDBServerPORT2
                        fi

                        for i in {1..$M}
                        do
                                python3.8 IDB_client.py --username Alice --password 123456 --serverURL $serverURL --serverPORT $IDBServerPORT --prefix_len $prefix_len --rate_limiting $rate_limiting --timelogging $timelogging
                        done
                done
                echo "Done $method-$prefix_len" 
        done
        
done


# WR19-Bloom

prefix_len=20
setSize=89492
cd WR_19_20/src/pmt-go
echo -e  "Method\tWR-19-Bloom l=$prefix_len" >> ../../../../results/performance_simulation.tsv
for rateLimiting in 0 1
do
        for i in {1..$M}
        do
                go run WR_19.go -keyLength=256 -setSize=$setSize -numThreads=1 -enablePC=true -requesterInput="Simba" -rateLimiting=$rateLimiting >> ../../../../results/performance_simulation.tsv
        done
done
# WR20-Cuckoo
echo -e "Method\tWR20-Cuckoo l=$prefix_len" >> ../../../../results/performance_simulation.tsv
for rateLimiting in 0 1
do
        for i in {1..$M}
        do
                go run WR_20.go -keyLength=256 -setSize=$setSize -numThreads=1 -enablePC=true -requesterInput="Simba" -rateLimiting=$rateLimiting >> ../../../../results/performance_simulation.tsv
        done
done
cd ../../..



# # MIGP-Server l = 20
MIGPServerPORT=8183 #n=100
prefix_len=20
echo -e "Method\tMIGP-Server l=20" >> ../results/performance_simulation.tsv
for rate_limiting in 0 1
do
        if [[ prefix_len -eq 16 ]]
        then
                MIGPServerPORT=$MIGPServerPORT1
        else
                MIGPServerPORT=$MIGPServerPORT2
        fi

        for i in {1..$M}
        do
                python3.8 MIGP_client.py --username Alice --password 123456 --serverURL $serverURL --serverPORT $MIGPServerPORT --prefix_len $prefix_len --rate_limiting $rate_limiting --timelogging $timelogging --n 100
        done
done
echo "Done MIGP-Server l=20" 
# # MIGP-Client l = 16
prefix_len=16
echo -e "Method\tMIGP-Client l=$prefix_len" >> ../results/performance_simulation.tsv
for rate_limiting in 0 1
do
        if [[ prefix_len -eq 16 ]]
        then
                MIGPServerPORT=$MIGPServerPORT1
        else
                MIGPServerPORT=$MIGPServerPORT2
        fi

        for i in {1..$M}
        do
                python3.8 MIGP_client.py --username Alice --password 123456 --serverURL $serverURL --serverPORT $MIGPServerPORT --prefix_len $prefix_len --rate_limiting $rate_limiting --timelogging $timelogging --n 10
        done
done
echo "Done MIGP-Client l=16"
# # MIGP-Client l = 20
prefix_len=16
echo -e "Method\tMIGP-Client l=16" >> ../results/performance_simulation.tsv
for rate_limiting in 0 1
do
        if [[ prefix_len -eq 16 ]]
        then
                MIGPServerPORT=$MIGPServerPORT1
        else
                MIGPServerPORT=$MIGPServerPORT2
        fi

        for i in {1..$M}
        do
                python3.8 MIGP_client.py --username Alice --password 123456 --serverURL $serverURL --serverPORT $MIGPServerPORT --prefix_len $prefix_len --rate_limiting $rate_limiting --timelogging $timelogging --n 10
        done
done

echo "Done MIGP-Client l=16"
# # MIGP-Client l = 20
prefix_len=20
echo -e "Method\tMIGP-Client l=20" >> ../results/performance_simulation.tsv
for rate_limiting in 0 1
do
        if [[ prefix_len -eq 16 ]]
        then
                MIGPServerPORT=$MIGPServerPORT2
        else
                MIGPServerPORT=$MIGPServerPORT1
        fi

        for i in {1..$M}
        do
                python3.8 MIGP_client.py --username Alice --password 123456 --serverURL $serverURL --serverPORT $MIGPServerPORT --prefix_len $prefix_len --rate_limiting $rate_limiting --timelogging $timelogging --n 10
        done
done

# echo "Done MIGP-Client l = 20"


#MIGP-Hybrid l = 20
prefix_len=20
echo -e "Method\tMIGP-Hybrid l=$prefix_len" >> ../results/performance_simulation.tsv
for rate_limiting in 0 1
do
        if [[ prefix_len -eq 16 ]]
        then
                MIGPServerPORT=$MIGPServerPORT1
        else
                MIGPServerPORT=$MIGPServerPORT2
        fi

        for i in {1..$M}
        do
                python3.8 MIGP_client.py --username Alice --password 123456 --serverURL $serverURL --serverPORT $MIGPServerPORT --prefix_len $prefix_len --rate_limiting $rate_limiting --timelogging $timelogging --n 10
        done
done

echo -e  "Method\tFinish!" >> ../results/performance_simulation.tsv
# Generate the Figure 11
python3.8 Figure_11.py