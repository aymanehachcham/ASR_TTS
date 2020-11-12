FROM ubuntu:18.04

MAINTAINER Ahmed Barbouche <ahmed.barbouche1@gmail.com>

# Ignore APT warnings about not having a TTY
ENV DEBIAN_FRONTEND noninteractive
ENV DOCKER_DEV true

# install Dependecies
RUN \
apt-get update -qq && \
apt-get install -y \
build-essential \
apt-utils &&\
apt-get install -y \
aptdaemon \
ed git \
libcairo-dev \
libedit-dev \
libapparmor1 \
libpq-dev \
libedit2 \
libssl1.0.0 \
libcurl4-gnutls-dev \
libssl-dev \
curl \
sudo \
wget &&\
apt-get install -y \
libzbar-dev \
imagemagick \
zip \
unzip \
xvfb &&\
rm -rf /var/lib/apt/lists/*

# install Python libraries
RUN \
apt-get update -qq && \
apt-get install -y \
python3 python3-pip python3.6-venv python3-dev  libssl-dev &&\
pip3 --no-cache-dir install virtualenv --upgrade && \
#easy_install distribute && \
rm -rf /var/lib/apt/lists/*

RUN apt-get update && \
    apt-get install binutils libproj-dev gdal-bin libgeoip1 postgis python-gdal -y &&\
    rm -rf /var/lib/apt/lists/*

RUN apt-get update -y && apt-get install -y --no-install-recommends build-essential gcc \
                                        libsndfile1 \
                                        ffmpeg \
                                        libsndfile1-dev \
                                        llvm-7 \
                                        libblas-dev \
                                        liblapack-dev \
                                        libatlas-base-dev \
                                        gfortran


#RUN gunicorn -b :5000 --access-logfile - --error-logfile - app:app

ENV SHELL /bin/bash

RUN useradd -m docker

RUN echo "docker ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

COPY docker-entrypoint.sh /

RUN chmod 777 /docker-entrypoint.sh

#USER docker

RUN mkdir -p /home/docker/app/

WORKDIR /home/docker/app

ENTRYPOINT ["/docker-entrypoint.sh"]

