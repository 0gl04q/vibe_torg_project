FROM postgres:15
LABEL authors="0gl04q"

COPY db_init.sh /docker-entrypoint-initdb.d/db_init.sh

COPY start.sh /start.sh

RUN chmod +x /docker-entrypoint-initdb.d/db_init.sh /start.sh

ENTRYPOINT ["/start.sh"]