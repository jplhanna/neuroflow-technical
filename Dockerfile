From Python:3.6

ENV PYTHONBUFFERED 1

RUN mkdir /mood_service

WORKDIR /mood_service

ADD . /mood_service/

RUN pip install -r requirements.txt