
set -xe
IDBServerPORT1=8774
IDBServerPORT2=8775

MIGPServerPORT1=8184 #n=100
MIGPServerPORT2=8183 #n=100

# Run the servers...
python3.8 MIGP_server.py --port $MIGPServerPORT1 --prefix_len 16&
python3.8 MIGP_server.py --port $MIGPServerPORT2 --prefix_len 20&

python3.8 IDB_server.py --port $IDBServerPORT1 --prefix_len 16&
python3.8 IDB_server.py --port $IDBServerPORT2 --prefix_len 20&
wait