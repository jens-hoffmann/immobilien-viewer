FROM solr:9

USER root
RUN mkdir /haystackcore_conf
RUN cp -R /opt/solr/server/solr/configsets/_default/conf/* /haystackcore_conf
RUN cp /opt/solr/server/solr/configsets/sample_techproducts_configs/conf/currency.xml /haystackcore_conf
COPY ./solrconfig.xml /haystackcore_conf
COPY ./managed-schema.xml /haystackcore_conf
RUN chown solr:solr /haystackcore_conf
USER $SOLR_UID


