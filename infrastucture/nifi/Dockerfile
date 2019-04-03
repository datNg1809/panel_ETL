FROM alpine:3.7

ENV PATH $PATH:/nifi/bin

ARG NIFI_VERSION=1.7.1

ARG TAR=nifi-${NIFI_VERSION}-bin.tar.gz

LABEL Description="Nifi" \
      "Nifi Version"="$NIFI_VERSION"

WORKDIR /

RUN set -euxo pipefail && \
    apk add --no-cache bash openjdk8-jre-base
RUN apk add --no-cache nss

ENV JAVA_HOME /usr/lib/jvm/java-1.8-openjdk
RUN export JAVA_HOME

RUN set -euxo pipefail && \
    apk add --no-cache wget tar && \
    url="http://www.apache.org/dyn/closer.lua?filename=nifi/${NIFI_VERSION}/${TAR}&action=download"; \
    url_archive="http://archive.apache.org/dist/nifi/${NIFI_VERSION}/${TAR}"; \
    wget -t 10 --max-redirect 1 --retry-connrefused -O "${TAR}" "$url" || \
    wget -t 10 --max-redirect 1 --retry-connrefused -O "${TAR}" "$url_archive" && \
    tar zxf "${TAR}" && \
    test -d "nifi-$NIFI_VERSION" && \
    ln -sv "nifi-${NIFI_VERSION}" nifi && \
    rm -fv  "${TAR}" && \
    apk del tar wget

RUN apk add --no-cache alpine-sdk  && \
    apk add --no-cache python3 python3-dev alpine-sdk openblas-dev && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools   && \
   if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
   if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi

COPY nifi/requirements.txt /tmp
RUN     pip3 install --upgrade numpy==1.16.2 # separate from requirements.txt due to a probable bug in pandas 0.4.1 installer

RUN     pip3 install --upgrade pip -r /tmp/requirements.txt

RUN mkdir -p /data/input && \
    mkdir -p /data/backup && \
    chmod -R 777 /data && \
    mkdir -p /usr/local/src

EXPOSE 8080

CMD nifi.sh start; tail -f /dev/null /nifi/log*/*

