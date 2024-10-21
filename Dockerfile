FROM python:3.10-slim-bullseye

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


WORKDIR /src

COPY ./requirements.txt /src/
RUN apt-get update -y && \
    apt-get install -y netcat && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

COPY ./entrypoint.sh /src/
RUN ["chmod", "+x",  "/src/entrypoint.sh"]

COPY . /src/

ENTRYPOINT ["sh", "-c" ,"/src/entrypoint.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
