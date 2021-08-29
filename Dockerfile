FROM python:3.9-alpine

RUN mkdir /app

ADD . /app

COPY . ./app

WORKDIR /app

RUN pip install -r requirements.txt

RUN run python run.sh

