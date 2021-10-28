#/!bin/bash
# Run script as root please

NAME=$1
CONTAINER=$2
#NAME=`date '+%Y%m%d-%H%M%S'`
DIR="/home/admin/CROCUS/zMeasures/"
HOST=`hostname`
MEASUREFREQUENCY=2
FILE="$DIR/measure-$HOST-$CONTAINER-$NAME.txt"
if [ $CONTAINER == 'onos1' ] || [ $CONTAINER == 'onos2' ] 
then
    docker cp $CONTAINER:/root/onos/apache-karaf-4.2.8/data/decanter/appender.csv "$DIR/decanter-$HOST-$NAME-ini.csv"
fi
echo "" > $FILE

while :
do 
    curDate=`date +%s`
    echo "#########:$curDate" >> $FILE
    # --oneline is only supported in the most recent versions.
    #ss -i -m --oneline >> $FILE
    #ss -i -m -n -t -u --oneline >> $FILE 
    docker exec $CONTAINER ss -i -m -n -t -u >> $FILE 
    sleep  $MEASUREFREQUENCY
done

