FROM python:3.10.9-slim-bullseye

EXPOSE 5000

WORKDIR /app
COPY requirements.txt /app/requirements.txt
COPY app.py /app/app.py
COPY gunicorn-starter.sh /app/guni.sh

RUN pip3 install -r requirements.txt

ENTRYPOINT ["gunicorn", "app:app", "-w", "2", "--threads", "2", "-b", "0.0.0.0:8000"]