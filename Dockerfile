FROM python:3.11

WORKDIR /app
ENV PYTHONPATH=/app

COPY . /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt
