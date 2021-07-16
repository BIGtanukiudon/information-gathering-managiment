FROM python:3.8-slim as base
USER root

RUN apt-get update
RUN apt-get -y install locales && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
ENV TERM xterm

WORKDIR /home/app
COPY ./app /home/app

RUN pip install --upgrade pip
RUN pip install pipenv

# 開発用
FROM base as dev
RUN apt-get install -y git && pipenv install --dev

# 本番用
FROM base as prod
RUN pipenv install