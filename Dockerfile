FROM library/python:3.6.3-alpine

ENV PYTHONUNBUFFERED 1

RUN apk update \
  # dependencies for building Python packages
  && apk install -y build-essential \
  # psycopg2 dependencies
  && apk install -y libpq-dev \
  # Translations dependencies
  && apk install -y gettext \
  # cleaning up unused files
  && apk purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

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
