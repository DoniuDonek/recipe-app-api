FROM python:3.9-alpine3.13 

LABEL maintainer="londonappdeveloper.com" 
# powyżej nazwa 

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt 
COPY ./app /app
WORKDIR /app
EXPOSE 8000

ARG DEV=false
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    # instalowanie requirements w Docker image powyżej
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    # usuwamy powyżej tmp, bo już go nie potrzeba i nie zaśmieci obrazu
    adduser \
        --disabled-password \
        --no-create-home \
        django-user
    # dodaje nowego usera wewnątrz docker image

ENV PATH="/py/bin:$PATH"

USER django-user
# nie ma full przywilejów, co jest dobre w razie ataku