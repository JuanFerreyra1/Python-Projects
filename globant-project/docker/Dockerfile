# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

COPY requirements.txt /home/a446649/logs/docker/globant-project/requirements.txt

WORKDIR /home/a446649/logs/docker/globant-project

RUN apt-get update


RUN apt-get -y install  openjdk-11-jdk

RUN pip3 install -r requirements.txt

COPY . .
 

CMD [ "python3", "challenge.py"]

EXPOSE 3306
