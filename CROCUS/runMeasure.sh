#/!bin/bash
# Run script as root please

NAME=$1
#NAME=`date '+%Y%m%d-%H%M%S'`
DIR="/home/admin/CROCUS/zMeasures/"
HOST=`hostname`
MEASUREFREQUENCY=1
FILE="$DIR/measure-$HOST-$NAME.txt"
echo "" > $FILE
while :
do 
    curDate=`date +%s`
    echo "#########:$curDate" >> $FILE
    ss -i -m --oneline >> $FILE
    sleep  $MEASUREFREQUENCY
done


