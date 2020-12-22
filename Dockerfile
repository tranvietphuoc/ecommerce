FROM python:3.8.2

RUN pip install flask flask_mail flask_login flask_admin flask_babel flask_script flask_migrate flask_sqlalchemy wtforms flask_wtf

RUN mkdir /app

ADD . /app

WORKDIR /app

RUN run python run.sh
