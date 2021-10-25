#/!bin/bash
# Run script as root please

NAME=$1
IF="eth0"
DIR="/home/admin/CROCUS/zPcapfiles/"

HOST=`hostname`
FILE="$DIR/measure-$HOST-$NAME.txt"

mkdir -p $DIR

tshark -i $IF -w "/tmp/tshark-$HOST-$NAME.pcap" -q  &

#tshark -i $IF -f "port 9876 or port 6653 or port 8181 or port 6640 or port 8101 or port 6633" -w "/tmp/file$NAME.pcap" -q  &
#cmd="tshark -i $IF -f \"port 9876 or port 6653 or port 8181 or port 6640 or port 8101 or port 6633\" -w \"/tmp/file$NAME.pcap\" -q "
#$cmd &

