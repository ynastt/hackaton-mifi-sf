FROM python:3.11

WORKDIR /app
ENV PYTHONPATH=/app

COPY . /app
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt
