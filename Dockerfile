FROM python:3.12-alpine

# prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE 1
# ensure Python output is sent directly to the terminal without buffering
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./scripts /scripts
COPY . /app
WORKDIR /app
EXPOSE 8000

RUN pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user && \
    chown -R django-user:django-user /app && \
    chmod -R +x /scripts

ENV PATH="/scripts:/py/bin:$PATH"

USER django-user

ENTRYPOINT ["entrypoint.sh"]