#!/usr/bin/env bash


FOLDER_HOST=$1
PATTERN=$2
YYYY=${PATTERN:0:4}
MM=${PATTERN:5:2}
previous_MM="$((10#$MM - 1))"
printf -v previous_MM "%02d" $previous_MM
DIR=$3
SEPARATE=$4
TEAM=${5:-MADA}

#Sample call
# bash /home/d.nguyen/panel/application/export_calcul_to_op21.sh IMMO_DE 2019_07 /home/d.nguyen/panel N 
# or bash /home/d.nguyen/panel/application/export_calcul_to_op21.sh IMMO_FR.SELOGER 2019_07 /home/d.nguyen/panel N TUNIS

LOGDIR=$DIR/application/export_log
[[ -e $LOGDIR ]] || mkdir -p $LOGDIR
LOG=$LOGDIR/Export_${FOLDER_HOST}_${PATTERN}.log
TEMPDIR=$DIR/application/temporary_${FOLDER_HOST}_${PATTERN}
[[ -e $TEMPDIR ]] || mkdir -p $TEMPDIR
DESTDIR=$DIR/data/input

#transfer function
transfer () {
  ssh -l d.nguyen -L 2222:127.0.0.1:22 -4 tele@46.105.109.54  -fN
  if [[ $1 == Y ]] && [[ $FOLDER_HOST == "VO_FR" ]]; then
    scp -P 2222 tele@127.0.0.1:/home/livraison_user/upload/${FOLDER_HOST}/*VO_VO_${YYYY}_${previous_MM}* ${TEMPDIR}
  elif [[ $1 == Y ]] && [[ $FOLDER_HOST == "NPV_CA" ]]; then
    scp -P 2222 tele@127.0.0.1:/home/livraison_user/upload/${FOLDER_HOST}/VO_NPV_${PATTERN}* ${TEMPDIR}
  elif [[ $1 == Y ]] && [[ $FOLDER_HOST == "NPV_UK" ]]; then
    scp -P 2222 tele@127.0.0.1:/home/livraison_user/upload/${FOLDER_HOST}/VO_NPVUK_${PATTERN}* ${TEMPDIR}
  elif [[ $1 == Y ]] && [[ $FOLDER_HOST == "CAMION" ]]; then
    scp -P 2222 tele@127.0.0.1:/home/livraison_user/upload/${FOLDER_HOST}/VO_CAMION[A-Z][A-Z]_${PATTERN}* ${TEMPDIR}
  elif [[ $1 == Y ]]; then
    scp -P 2222 tele@127.0.0.1:/home/livraison_user/upload/${FOLDER_HOST}/*${FOLDER_HOST}_${PATTERN}* ${TEMPDIR}
  else
    scp -P 2222 tele@127.0.0.1:/home/livraison_user/upload/${FOLDER_HOST}/*${PATTERN}* ${TEMPDIR}
  fi
  gunzip -rf ${TEMPDIR} 
  
  #parsing file, changing delimiter to semicolon, spliting file if necessary
  if [[ $TEAM != "TUNIS" ]]; then
    for file in ${TEMPDIR}/*.csv
    do
      if [[ ${file} == *"_TOTAL_"* ]] || [[ ${file} == *"_PRO_"* ]] || [[ ${file} == *"_DOUBLON_"* ]] || [[ ${file} == *"_TEL_"* ]] || [[ ${file} == *"_SUMMARY_"* ]]; then
        rm -rf $file
        continue
      fi
      
      if [[ $FOLDER_HOST == "CAMION" ]]; then
        base=$(basename ${file})
        country=${base:9:2}
        market_country="CAMION_${country}"
        cat ${file} | python3 $DIR/application/parsing.py ${market_country} ${PATTERN} ${TEMPDIR} $SEPARATE $(basename ${file}) $TEAM
      else
        cat ${file} | python3 $DIR/application/parsing.py ${FOLDER_HOST} ${PATTERN} ${TEMPDIR} $SEPARATE $(basename ${file}) $TEAM
      fi
    
      if [[ $1 == "Y" ]]; then
        rm -rf $file
      elif [[ $1 == "N" ]]; then
        rm -rf $(dirname ${file})/TEM_$(basename ${file})
      fi
    done
    #Format name of files to match with Grafana
    for file in ${TEMPDIR}/*.csv
    do
      fix_name $file $FOLDER_HOST
    done

    for file in ${TEMPDIR}/*.csv
    do
      fix_folder_name $file $FOLDER_HOST
    done
  fi   
  #Transfer files to /data/input folder and get files ready to be calculated
  for file in ${TEMPDIR}/*.csv
  do
      #check if any of website has been uploaded
      if [[ -e $LOG ]] && ( [[ ${FOLDER_HOST:0:2} != "VO" ]] && [[ ${FOLDER_HOST:0:3} != "NPV" ]] ); then
        if grep -q $(basename ${file}) $LOG; then
          echo "$(basename ${file}) has been already transferred, then it will not be uploaded this time"
          continue
        fi
      elif [[ -e $LOG ]]; then
        if grep -q $(basename ${file}) $LOG; then
          logdate=$(grep $(basename ${file}) $LOG)
          datelog_plus3=$(date -d "${logdate:0:10} +3 days")
          current_date_time=$(date)
          echo $datelog_plus3
          #echo $current_date_time
          if [[ $current_date_time != $datelog_plus3 ]]; then
            echo "$(basename ${file}) has been already transferred, it will be uploaded again on day ${datelog_plus3}"
            continue
          fi
        fi
      fi

      #don't transfer file which is smaller than 100 bytes
      size="$(wc -c <"$file")"
      if [[ $size < 100 ]]; then
        continue
      fi
      config_name="${$(basename ${file})::-12}_general.json"
      echo "$config_name"
      config_file=$DIR/application/config/json_config/config_name
      if test -f "$config_file"; then
        rsync $file $DESTDIR/ 
        echo "$(basename ${file}) has been transferred"
        #make log file
        current_date_time="`date "+%Y-%m-%d %H:%M:%S"`"
        touch $LOG
        echo "$current_date_time : Exporting $(basename ${file}) into dir=$DESTDIR" >> $LOG
      else
        continue       
      fi
  done
  echo "transfer files completed"
}

fix_name() {
  declare -A arr
  arr["_IDEALISTAES_"]="_IDEALISTA_"
  arr+=( ["_AUTOSCOUT_"]="_AUTOSCOUT24_" ["_GUMTREEUK_"]="_GUMTREE_" ["_IDEALISTAIT_"]="_IDEALISTA_" ["_KIJIJIIT_"]="_KIJIJI_" )
  arr+=( ["_FACEBOOK_MARKETPLACE_"]="_FACEBOOK_" ["_KIJIJICA_"]="_KIJIJI_" ["_LESPAC_"]="_LESPACS_" )
  for key in ${!arr[@]};
  do
      if [[ $1 == *"${key}"* ]]; then mv "$1" "${1/$key/${arr[${key}]}}"; fi
  done
  echo "changing website name completed"
}

fix_folder_name() {
  if [[ $FOLDER_HOST == "IMMO_UK" ]]; then
      echo "$1"
      echo "${1/\/IMMO_/\/IMMO_UK_}"
      mv "$1" "${1/\/IMMO_/\/IMMO_UK_}"
      echo "$1"
  elif [[ $FOLDER_HOST == "IMMO_CA" ]]; then
      mv "$1" "${1/\/IMMO_/\/IMMO_CA_}"
  elif [[ $FOLDER_HOST == "VO_BE" ]]; then
      if [[ $1 == *"_MOBILEDE_"* ]]; then
        mv "$1" "${1/_MOBILEDE_/_MOBILE_}"
      elif [[ $1 == *"_VLANAUTO_"* ]]; then
        mv "$1" "${1/_VLANAUTO_/_AUTOVLAN_}"
      fi
  elif [[ $FOLDER_HOST == "JOBS" ]]; then
      name=$1
      name="${name/VO_/JOB_FR_}"
      name="${name%_*}.csv"
      mv "$1" "$name"
  fi
  echo "changing folder name completed"  
}

#check if data is transferred already, if yes, stop program. Exceptional, for VO market, data will be re-calculated at day D+3
#if [[ -e $LOG ]] && [[ ${FOLDER_HOST:0:2} == "VO" ]]; then
#    line=$(tail -n 1 $LOG)
#    head_=$(head -n 1 $LOG)
#    datelog=${head_:0:10}
#    #datelog= $(date -d ${datelog} + "+%Y-%m-%d")
#    current_date_time=$date
#    if [[ $current_date_time == $(date -d "${datelog} +3 days") ]]; then
#      echo $current_date_time
#      echo $datelog
#      transfer $SEPARATE
#    elif [[ "$line" == "$head_" ]]; then
#      transfer $SEPARATE
#    else
#      rm -rf $TEMPDIR
#      exit 0
#    fi
#else
transfer $SEPARATE
#fi
rm -rf $TEMPDIR
