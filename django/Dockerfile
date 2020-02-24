FROM python:3.8.1-buster

ENV PYTHONUNBUFFERED 1

RUN apt update && apt install -y build-essential

RUN mkdir /django
WORKDIR /django

ADD requirements.txt /django
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ADD . /django/