FROM python:3.9.5-buster
ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN mkdir -p /code
WORKDIR /code

ADD Pipfile /code/
ADD Pipfile.lock /code/

RUN pip install --upgrade pip
RUN pip install pipenv
RUN pipenv install --system --deploy

ADD . /code/
