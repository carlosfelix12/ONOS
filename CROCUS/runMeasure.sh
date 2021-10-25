#/!bin/bash
# Run script as root please

NAME=$1
CONTAINER=$2
#NAME=`date '+%Y%m%d-%H%M%S'`
DIR="/home/admin/CROCUS/zMeasures/"
HOST=`hostname`
MEASUREFREQUENCY=1
FILE="$DIR/measure-$HOST-$NAME.txt"
docker cp $CONTAINER:/root/onos/apache-karaf-4.2.8/data/decanter/appender.csv "$DIR/decanter-$HOST-$NAME-ini.csv"

echo "" > $FILE
while :
do 
    curDate=`date +%s`
    echo "#########:$curDate" >> $FILE
    #ss -i -m --oneline >> $FILE
    ss -i -m -n -t -u --oneline >> $FILE
    sleep  $MEASUREFREQUENCY
done

