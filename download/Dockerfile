FROM python:3.10.9-slim-bullseye


ENV IMG_VOL /mnt/negatives/

WORKDIR /app

COPY requirements.txt /app/requirements.txt
COPY app.py /app/app.py

RUN pip3 install -r requirements.txt

ENTRYPOINT ["gunicorn", "app:app", "-w", "2", "--threads", "2", "-b", "0.0.0.0:8000"]