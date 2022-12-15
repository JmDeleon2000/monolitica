## Run

docker build "$(pwd)/reqs" -t reqs
docker build . -t labmono | docker stop $(docker ps -q) | docker run -dp 8501:8501 labmono