#!/usr/bin/env bash

ssh -l d.nguyen -L 2222:127.0.0.1:22 -4 tele@46.105.109.54  -fN
#scp -P 2222 tele@127.0.0.1:/home/livraison_user/upload/AUTO_AU/CARSALES_* /home/d.nguyen/panel/test/


FOLDER_HOST=$1
PATTERN=$2
YYYY=${PATTERN:0:4}
MM=${PATTERN:5:2}
DIR=$3

#Sample call
# bash /home/d.nguyen/panel/application/export_calcul_to_op21.sh IMMO_DE 2019_07 /home/d.nguyen/panel/



LOGDIR=$DIR/application
LOG=$LOGDIR/Export_${PATTERN}.log
TEMPDIR=$DIR/application/temporary
[[ -e $TEMPDIR ]] || mkdir -p $TEMPDIR
DESTDIR=$DIR/data/input

scp -P 2222 tele@127.0.0.1:/home/livraison_user/upload/${FOLDER_HOST}/*${PATTERN}* ${TEMPDIR}
gunzip -r ${TEMPDIR}

for file in ${TEMPDIR}/*
do
    if [[ "DOUBLON" == *${file}* ]] || [[ "_TEL_" == *${file}* ]]; then
        continue
    fi

    cat file | python ${LOGDIR}/parsing.py ${FOLDER_HOST} ${PATTERN} ${DESTDIR}

    rsync file $DESTDIR/
    current_date_time="`date "+%Y-%m-%d %H:%M:%S"`"
    touch $LOG
    echo "At time {$current_date_time}, exporting data $file into dir=$DESTDIR" >> $LOG
done
rm -rf $TEMPDIR

#|sed "s/'/\'/;s/\",\"/\";\"/g;s/\t/\";\"/g;s/^/\"/;s/$/\"/;s/\n//g;s/NULL//g"
