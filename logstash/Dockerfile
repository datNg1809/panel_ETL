ARG ELK_VERSION

# https://github.com/elastic/logstash-docker
FROM docker.elastic.co/logstash/logstash:${ELK_VERSION}

RUN rm /usr/share/logstash/config/logstash.yml

COPY ./config/logstash.yml /usr/share/logstash/config/logstash.yml

COPY ./pipeline /usr/share/logstash/pipeline
