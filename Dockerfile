FROM python:latest

WORKDIR /project

ADD requirements.txt requirements.txt

RUN pip install -r requirements.txt

RUN adduser --disabled-password --gecos '' app
