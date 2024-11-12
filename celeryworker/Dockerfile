FROM python:3.12-alpine

# prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE 1
# ensure Python output is sent directly to the terminal without buffering
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
WORKDIR /app
EXPOSE 8000

RUN pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt && \
    adduser \
        --disabled-password \
        --no-create-home \
        celery-user && \
    chown -R celery-user:celery-user /app


USER celery-user
