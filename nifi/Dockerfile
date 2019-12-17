FROM docker.autobiz.pro/infra/nifi_autobiz:latest

USER root
COPY ./requirements.txt /tmp

RUN  pip3 install -r /tmp/requirements.txt && \
     mkdir -p /usr/local/data && mkdir -p /usr/local/bin/src && \
		 chown nifi:nifi /usr/local/data && chown nifi:nifi /usr/local/bin/src

COPY --chown=nifi:nifi ./conf /opt/nifi/nifi-current/conf
COPY --chown=nifi:nifi ./logs/nifi /opt/nifi/nifi-current/logs
COPY --chown=nifi:nifi ./application /usr/local/src
COPY --chown=nifi:nifi ./data /usr/local/data

RUN  mkdir -p /usr/local/src/config/final_config && \
     chown nifi:nifi /usr/local/src/config/final_config && \
     chmod -R 775 /usr/local/src/config/final_config

USER nifi
