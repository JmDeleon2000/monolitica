# app/Dockerfile

#FROM tensorflow/tensorflow:latest
FROM python:3.10.9-slim-bullseye

EXPOSE 8501

WORKDIR /app
COPY requirements.txt /app/requirements.txt

RUN pip3 install -r requirements.txt
