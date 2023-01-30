FROM python:3.11.1-slim-buster

ARG api_port
ARG api_env
ARG redis_host
ARG redis_port

ENV EXPOSE_PORT=$api_port
ENV ENV=$api_env
ENV REDIS_HOST=$redis_host
ENV REDIS_PORT=$redis_port

#RUN apt-get update && apt-get install -y --no-install-recommends gcc build-essential curl

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

WORKDIR /

COPY . .

EXPOSE $EXPOSE_PORT
CMD uvicorn app:app --host 127.0.0.1 --port $EXPOSE_PORT