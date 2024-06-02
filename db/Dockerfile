FROM postgres:15
LABEL authors="0gl04q"

# Копируем скрипт инициализации
COPY db_init.sh /docker-entrypoint-initdb.d/db_init.sh

# Копируем наш стартовый скрипт
COPY start.sh /start.sh

# Устанавливаем права на выполнение скриптов
RUN chmod +x /docker-entrypoint-initdb.d/db_init.sh /start.sh

# Заменяем стандартный entrypoint на наш скрипт
ENTRYPOINT ["/start.sh"]