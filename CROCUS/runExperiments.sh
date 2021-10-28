#/!bin/bash
# Run script as root please
TOPO=$1

IF="eth0"
DIR="/home/admin/CROCUS/zPcapfiles/"
DIRME="/home/admin/CROCUS/zMeasures/"

NAME=`date '+%Y%m%d-%H%M%S'`
DIR="/home/admin/CROCUS"

node1="10.3.1.203"
node2="10.3.1.160"

ONOS1="onos1"
ONOS2="onos2"

ATOMIX1="atomix-1"
ATOMIX2="atomix-2"

mn -c
mn -c

# Should run on the remote machines with ONOS
# 
# requires public key of admin
#
echo "starting mearusments on $node1"
#ssh -i admin.pem root@$node1 'bash -s ' < $DIR/runTshark.sh $NAME &
ssh -i admin.pem root@$node1 'bash -s ' < $DIR/runMeasure.sh $NAME $ONOS1 &
ssh -i admin.pem root@$node1 'bash -s ' < $DIR/runMeasure.sh $NAME $ATOMIX1 &

echo "starting mearusments on $node2"
#ssh -i admin.pem root@$node2 'bash -s ' < $DIR/runTshark.sh $NAME  &
ssh -i admin.pem root@$node2 'bash -s ' < $DIR/runMeasure.sh $NAME $ONOS2 &
ssh -i admin.pem root@$node2 'bash -s ' < $DIR/runMeasure.sh $NAME $ATOMIX2 &

echo "To start in 3s"
sleep 3
python3 runTopologies.py $TOPO

ssh -i admin.pem root@$node1 'bash -s ' < $DIR/runEndExperiment.sh $NAME $ONOS1 &
ssh -i admin.pem root@$node1 'bash -s ' < $DIR/runEndExperiment.sh $NAME $ATOMIX1 &

ssh -i admin.pem root@$node2 'bash -s ' < $DIR/runEndExperiment.sh $NAME $ONOS2 &
ssh -i admin.pem root@$node2 'bash -s ' < $DIR/runEndExperiment.sh $NAME $ATOMIX2 &

sleep 3
mn -c

END=`date '+%Y%m%d-%H%M%S'`
echo "ini:$NAME,topo:$TOPO,end:$END" >> "$DIRME/tests"

scp -i admin.pem root@$node1:/home/admin/CROCUS/zMeasures/* zMeasures/onos1/
scp -i admin.pem root@$node2:/home/admin/CROCUS/zMeasures/* zMeasures/onos2/

