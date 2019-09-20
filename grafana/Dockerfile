FROM grafana/grafana:6.3.5
USER root
RUN rm -rf /var/lib/grafana/
COPY ./config/ /etc/grafana/
COPY ./data/ /var/lib/grafana/
RUN chown -R grafana:grafana /var/lib/grafana/
USER grafana
