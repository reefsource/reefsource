FROM python:3.5

ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE reefsource.settings.docker
ENV DJANGO_DEBUG False

RUN apt-get -y install --no-install-recommends \
    libxml2-dev \
    libxslt-dev \
    binutils \
    libproj-dev \
    gdal-bin \

# Sane defaults for pip
ENV PIP_NO_CACHE_DIR off
ENV PIP_DISABLE_PIP_VERSION_CHECK on

ADD . /code
WORKDIR /code

RUN pip install -r requirements/local.txt