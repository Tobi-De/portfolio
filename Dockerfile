FROM library/python:3.6.3-alpine

ENV PYTHONUNBUFFERED 1

RUN apk update && apk upgrade && apk add --no-cache make g++ bash git openssh postgresql-dev curl

# Create and set working directory
RUN mkdir -p /usr/src/app,
WORKDIR /usr/src/app
COPY . /usr/src/app

# Requirements are installed here to ensure they will be cached.
RUN pip install pip --upgrade
RUN pip install --no-cache-dir -r requirements/production.txt

# run script to run server
EXPOSE 80
CMD sh /usr/src/app/runserver.sh
