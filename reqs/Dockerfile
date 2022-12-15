# app/Dockerfile

FROM python:3.9-slim

EXPOSE 8501

WORKDIR /app
COPY requirements.txt /app/requirements.txt

RUN pip3 install -r requirements.txt
