#/!bin/bash
# Run script as root please

NAME=$1
CONTAINER=$2
IF="eth0"
DIR="/home/admin/CROCUS/zPcapfiles/"
DIRME="/home/admin/CROCUS/zMeasures/"

HOST=`hostname`
FILE="$DIR/measure-$HOST-$NAME.txt"

pkill -9 -f runMeasure.sh
pkill -9 -f runMeasure.sh

# pkill -9 -f runTshark.sh
# pkill -9 -f runTshark.sh
pkill -9 -f tshark
pkill -9 -f dumpcap

#mv "/tmp/tshark-$HOST-$NAME.pcap" "/$DIR/tshark-$HOST-$NAME.pcap"
#chown admin:admin -R "$DIR"

/usr/bin/docker cp $CONTAINER:/root/onos/apache-karaf-4.2.8/data/decanter/appender.csv "$DIRME/decanter-$HOST-$CONTAINER-$NAME-zend.csv"

pkill -9 -f "bash -s $NAME $CONTAINER"
pkill -9 -f "sshd: root"

pgrep -f "ssh: root" 
pgrep -f "ssh: root"