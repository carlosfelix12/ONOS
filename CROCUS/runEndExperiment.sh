#/!bin/bash
# Run script as root please

NAME=$1
CONTAINER=$2
IF="eth0"
DIR="/home/admin/CROCUS/zPcapfiles/"
DIRME="/home/admin/CROCUS/zMeasures/"

HOST=`hostname`
FILE="$DIR/measure-$HOST-$NAME.txt"

sudo pkill -9 -f runMeasure.sh
sudo pkill -9 -f runMeasure.sh

sudo pkill -9 -f runTshark.sh
sudo pkill -9 -f runTshark.sh
sudo pkill -9 tshark

mv "/tmp/tshark-$HOST-$NAME.pcap" "/$DIR/tshark-$HOST-$NAME.pcap"
sudo chown admin:admin -R "$DIR*"

docker cp $CONTAINER:/root/onos/apache-karaf-4.2.8/data/decanter/appender.csv "$DIRME/decanter-$HOST-$NAME-zend.csv"
