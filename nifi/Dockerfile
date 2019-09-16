FROM docker.autobiz.pro/infra/nifi_autobiz:latest

COPY requirements.txt /tmp

USER root

RUN  pip3 install --upgrade numpy==1.16.2 &&  pip3 install --upgrade pip -r /tmp/requirements.txt

COPY --chown=nifi:nifi ./conf /opt/nifi/nifi-current/conf
COPY --chown=nifi:nifi ./application /usr/local/src
COPY --chown=nifi:nifi ./data /usr/local/data

USER nifi

EXPOSE 8080
