FROM python:latest

WORKDIR /project

ADD requirements.txt requirements.txt

RUN pip install -r requirements.txt

EXPOSE 5000
RUN adduser --disabled-password --gecos '' app  
