## Build

docker build "$(pwd)/reqs" -t reqs
docker build . -t labmono

## Run
docker run -dp 8501:8501 labmono