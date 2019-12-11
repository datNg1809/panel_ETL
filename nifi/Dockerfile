FROM docker.autobiz.pro/infra/nifi_autobiz:latest

USER root
COPY ./requirements.txt /tmp

RUN  pip3 install -r /tmp/requirements.txt && \
     mkdir -p /usr/local/data && mkdir -p /usr/local/bin/src && \
		 chown nifi:nifi /usr/local/data && chown nifi:nifi /usr/local/bin/src

COPY --chown=nifi:nifi ./conf /opt/nifi/nifi-current/conf
COPY --chown=nifi:nifi ./application /usr/local/src
COPY --chown=nifi:nifi ./data /usr/local/data

USER nifi
