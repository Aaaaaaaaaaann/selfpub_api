FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

ADD requirements.txt /app
RUN pip install -r requirements.txt

COPY . /app/
