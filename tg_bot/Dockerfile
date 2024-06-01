FROM python:3.11.0-alpine
LABEL authors="0gl04q"

WORKDIR /var/www/tg_bot

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . ./

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN chmod +x ./bot.py

CMD python bot.py
