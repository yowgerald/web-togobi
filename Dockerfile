FROM python:3.8.3-alpine

ENV PROJECT=/var/www/python_django__togobi
# set work directory


RUN mkdir -p $PROJECT
RUN mkdir -p $PROJECT/static

# where the code lives
WORKDIR $PROJECT

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add postgresql-dev gcc python3-dev musl-dev \
    && apk del build-deps \
    && apk --no-cache add musl-dev linux-headers g++ \
    && apk add bash
# install dependencies
RUN pip install --upgrade pip
# copy project
COPY . $PROJECT
RUN pip install -r requirements.txt
RUN pip install django-settings-export