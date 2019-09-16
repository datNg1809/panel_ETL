FROM docker.autobiz.pro/infra/nifi_autobiz:latest

COPY nifi/requirements.txt /tmp
RUN     pip3 install --upgrade numpy==1.16.2 &&  pip3 install --upgrade pip -r /tmp/requirements.txt

RUN mkdir -p /data/input && \
    mkdir -p /data/backup && \
    chmod -R 777 /data && \
    mkdir -p /usr/local/src

EXPOSE 8080

CMD nifi.sh start; tail -f /dev/null /nifi/log*/*

