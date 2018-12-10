From python:3.6

ENV PYTHONBUFFERED 1

RUN pip install -r requirements.txt

RUN mkdir /mood_service

WORKDIR /mood_service

ADD . /mood_service/

