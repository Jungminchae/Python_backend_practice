FROM python:3.8-slim-buster

# USEFUL TO GET LOGS
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY . /app

CMD python manage.py runserver 0.0.0.0:8000