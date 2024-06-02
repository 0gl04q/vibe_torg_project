###########
# BUILDER #
###########

FROM python:3.11.0-alpine as builder

LABEL authors="0gl04q"

WORKDIR /var/www/VibeTorg

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update
RUN apk add postgresql-dev gcc python3-dev musl-dev
RUN pip install --upgrade pip

# Copy requirements for both projects
COPY lending/requirements.txt lending-requirements.txt
COPY manager/requirements.txt manager-requirements.txt

# Build wheels for both projects
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /var/www/VibeTorg/wheels -r lending-requirements.txt
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /var/www/VibeTorg/wheels -r manager-requirements.txt

##############
# BASE IMAGE #
##############

FROM python:3.11.0-alpine as base

RUN addgroup -S django && adduser -S django -G django

ENV HOME=/home/django
ENV APP_HOME=/home/django/web

WORKDIR $APP_HOME

RUN apk update && apk add libpq

COPY --from=builder /var/www/VibeTorg/wheels /wheels
COPY --from=builder /var/www/VibeTorg/lending-requirements.txt .
COPY --from=builder /var/www/VibeTorg/manager-requirements.txt .

RUN pip install --no-cache /wheels/*

RUN chown -R django:django $APP_HOME
USER django

###########
# lending #
###########

FROM base as lending

WORKDIR $APP_HOME/lending

COPY lending $APP_HOME/lending

USER root

RUN chown -R django:django $APP_HOME/lending

USER django

###########
# manager #
###########

FROM base as manager

WORKDIR $APP_HOME/manager

COPY manager $APP_HOME/manager

USER root

RUN chown -R django:django $APP_HOME/manager

USER django