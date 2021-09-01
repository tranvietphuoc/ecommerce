FROM python:3.9-alpine

RUN mkdir /app

ADD . /app

WORKDIR /app

RUN pip install -r requirements.txt

CMD ["sh", "run.sh"]

VOLUME /app

