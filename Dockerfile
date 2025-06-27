# Use official Python image
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY requirements/base.txt .
RUN pip install --upgrade pip && pip install -r base.txt

COPY . .
