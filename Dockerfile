FROM python:3.10-slim-bullseye

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


WORKDIR /backend

COPY ./requirements.txt .

RUN apt-get update -y && \
    apt-get install -y netcat && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

COPY ./entrypoint.sh .
RUN ["chmod", "+x",  "/backend/entrypoint.sh"]

COPY . .

ENTRYPOINT ["sh", "-c" ,"/backend/entrypoint.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
