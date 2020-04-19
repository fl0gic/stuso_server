FROM python:3.7-alpine

LABEL maintainer="Caden Kriese <caden2k3@gmail.com>"

COPY . .

RUN set -e; \
	apk add --no-cache --virtual .build-deps \
		gcc \
		libc-dev \
		linux-headers \
	; \
	pip3 install -r requirements/prod.txt; \
	pip3 install -r requirements.txt; \
	apk del .build-deps;

CMD uwsgi uwsgi.ini
