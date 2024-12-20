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
    apk add --update --no-cache postgresql17-client && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql17-dev musl-dev zlib zlib-dev linux-headers && \
    apk add --update --no-cache gdal proj geos binutils && \
    apk add --update --no-cache postgis && \
    ln -s /usr/lib/libgdal.so.36 /usr/lib/libgdal.so && \
    ln -s /usr/lib/libgeos_c.so.1 /usr/lib/libgeos_c.so && \
    ln -s /usr/lib/libproj.so.25 /usr/lib/libproj.so && \
    pip install -r /tmp/requirements.txt && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user && \
    chown -R django-user:django-user /app && \
    chmod -R +x /scripts

ENV PATH="/scripts:/py/bin:$PATH"

USER django-user

ENTRYPOINT ["entrypoint.sh"]