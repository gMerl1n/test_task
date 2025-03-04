FROM python:3.11-slim

WORKDIR /usr/local/task_service/


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN apt-get update
RUN apt-get install -y python3-dev gcc libc-dev libffi-dev
RUN apt-get -y install libpq-dev gcc

COPY requirements.txt /usr/local/task_service/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/local/task_service/

RUN chmod a+x /usr/local/task_service/start.sh

ENV PYTHONPATH "${PYTHONPATH}:/usr/local/task_service/"