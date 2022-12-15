# app/Dockerfile

FROM reqs:latest

EXPOSE 8501

WORKDIR /app


COPY main.py /app/main.py




ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]