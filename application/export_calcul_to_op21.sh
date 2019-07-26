#!/usr/bin/env bash


FOLDER_HOST=$1
PATTERN=$2
YYYY=${PATTERN:0:4}
MM=${PATTERN:5:2}
DIR=$3

#Sample call
# bash /home/d.nguyen/panel/application/export_calcul_to_op21.sh IMMO_DE 2019_07 /home/d.nguyen/panel/

LOGDIR=$DIR/application
LOG=$LOGDIR/Export_${FOLDER_HOST}_${PATTERN}.log
TEMPDIR=$DIR/application/temporary_${FOLDER_HOST}_${PATTERN}
[[ -e $TEMPDIR ]] || mkdir -p $TEMPDIR
DESTDIR=$DIR/data/input

#transfer function
transfer () {
  ssh -l d.nguyen -L 2222:127.0.0.1:22 -4 tele@46.105.109.54  -fN
  scp -P 2222 tele@127.0.0.1:/home/livraison_user/upload/${FOLDER_HOST}/*${PATTERN}* ${TEMPDIR}
  gunzip -rf ${TEMPDIR}

  for file in ${TEMPDIR}/*.csv
  do
      if [[ ${file} == *"DOUBLON"* ]] || [[ ${file} == *"_TEL_"* ]]; then
          continue
      fi
      cat ${file} | python3 $DIR/application/parsing.py ${FOLDER_HOST} ${PATTERN} ${TEMPDIR}
      #rsync $file $DESTDIR/
      rm -rf $file
  done

  for file in ${TEMPDIR}/*.csv
  do
      rsync $$file $DESTDIR/
      current_date_time="`date "+%Y-%m-%d %H:%M:%S"`"
      touch $LOG
      echo "$current_date_time : Exporting $(basename ${file}) into dir=$DESTDIR" >> $LOG
  done
  rm -rf $TEMPDIR
}

#check if data is transferred already
if [[ -e $LOG ]] && [[ ${FOLDER_HOST:0:2} == "VO" ]]; then
    line= tail -n 1 $LOG
    datelog= ${line:0:10}
    datelog= ${date --date=$datelog +%F}
    current_date_time=${date + "%Y-%m-%d"}
    if [[ $current_date_time == $(datelog -d "+3 days") ]]; then
      transfer
    else
      exit 0
    fi
elif [[ ! -e $LOG ]]; then
  transfer
fi


#|sed "s/'/\'/;s/\",\"/\";\"/g;s/\t/\";\"/g;s/^/\"/;s/$/\"/;s/\n//g;s/NULL//g"
