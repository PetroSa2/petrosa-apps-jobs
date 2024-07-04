# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY . .

RUN apt update && apt install -y git

RUN pip3 install -r requirements.txt

RUN pip3 install opentelemetry-distro opentelemetry-exporter-otlp
RUN opentelemetry-bootstrap -a install
