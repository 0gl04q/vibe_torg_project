# VibeTorgLending
Реализация лендинга компании ВайбТорг

## Подгатовка и запуск

На этапе подготовки необходимо добавить `.env` файл со следющим содержанием:
```dotenv
# Секретный ключ Djngo
SECRET_KEY=...

# True / False
DEBUG=...

# ALLOWED_HOSTS необходио записывать через символ '|'
ALLOWED_HOSTS=...
```

Команды создания образа и запуска контейнера:
```shell
docker build --tag vibe_torg:latest
docker run --env-file=.env.dev -d -p 8000:8000 vibe_torg:latest
```