FROM python:3.11-slim-buster
ENV PYTHONUNBUFFERED=1

ARG LOCAL_DEV_MODE=FALSE

WORKDIR /code

COPY ./create_tls_certs.sh /code/create_tls_certs.sh

RUN if [ "$LOCAL_DEV_MODE" = "TRUE" ] ; then ./create_tls_certs.sh ; fi

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

COPY server.py server.py

COPY ./static/ /code/static

RUN pytest

CMD ["python" ,"server.py"]
