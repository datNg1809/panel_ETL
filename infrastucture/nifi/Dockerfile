FROM alpine:latest

ENV PATH $PATH:/nifi/bin

ARG NIFI_VERSION=1.7.1

ARG TAR=nifi-${NIFI_VERSION}-bin.tar.gz

LABEL Description="Nifi" \
      "Nifi Version"="$NIFI_VERSION"

WORKDIR /

RUN set -euxo pipefail && \
    apk add --no-cache bash openjdk8-jre-base

ENV JAVA_HOME /usr/lib/jvm/java-1.8-openjdk
RUN export JAVA_HOME

RUN set -euxo pipefail && \
    apk add --no-cache wget tar && \
    url="http://www.apache.org/dyn/closer.lua?filename=nifi/${NIFI_VERSION}/${TAR}&action=download"; \
    url_archive="http://archive.apache.org/dist/nifi/${NIFI_VERSION}/${TAR}"; \
    # --max-redirect - some apache mirrors redirect a couple times and give you the latest version instead
    #                  but this breaks stuff later because the link will not point to the right dir
    #                  (and is also the wrong version for the tag)
    wget -t 10 --max-redirect 1 --retry-connrefused -O "${TAR}" "$url" || \
    wget -t 10 --max-redirect 1 --retry-connrefused -O "${TAR}" "$url_archive" && \
    tar zxf "${TAR}" && \
    # check tarball was extracted to the right place, helps ensure it's the right version and the link will work
    test -d "nifi-$NIFI_VERSION" && \
    ln -sv "nifi-${NIFI_VERSION}" nifi && \
    rm -fv  "${TAR}" && \
    #{ rm -rf nifi/docs; : ; } && \
    apk del tar wget

RUN apk add --no-cache alpine-sdk  && \
    apk add --no-cache python3 python3-dev alpine-sdk openblas-dev && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools   && \
    pip3 install --upgrade pip  great_expectations elasticsearch python-dotenv phonenumbers xlrd&& \
   if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
   if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
    rm -r /root/.cache && \
    mkdir /usr/local/bin/src
#    mkdir /nifi/logs && \
#    chmod -R 777 /nifi/logs
#

RUN mkdir -p /data/input && \
    mkdir -p /data/input

EXPOSE 8080


CMD nifi.sh start; tail -f /dev/null /nifi/log*/*

