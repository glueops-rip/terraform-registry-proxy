FROM python:3.9-slim-buster

RUN apt update -y && apt upgrade -y
# RUN apt install -y libnss3-tools curl

# RUN curl -JLO "https://dl.filippo.io/mkcert/latest?for=linux/amd64" && chmod +x mkcert-v*-linux-amd64 && cp mkcert-v*-linux-amd64 /usr/local/bin/mkcert

WORKDIR /code



COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

COPY server.py server.py


CMD ["python" ,"prod_server.py"]
