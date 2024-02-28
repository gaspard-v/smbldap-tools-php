#!/bin/bash

sudo apt update
sudo apt install build-essential autoconf libtool bison re2c pkg-config git -y
sudo apt install -y \
libbz2-dev \
libcurl4-openssl-dev \
libffi-dev \
libzip-dev \
libpng-dev \
libjpeg-dev \
libwebp-dev \
libavif-dev \
libgmp-dev \
libldap2-dev \
libonig-dev \
libssl-dev \
libpq-dev \
libreadline-dev \
libsodium-dev \
libxml2-dev \
libzip-dev \
libsqlite3-dev

mkdir --verbose --parent "/tmp/php-build"
cd "/tmp/php-build"
git clone https://github.com/php/php-src.git --branch=master
cd "php-src"
./buildconf

./configure \
--prefix=/usr/local/php \
--enable-bcmath=shared \
--with-fpm-systemd \
--with-bz2=shared \
--with-curl=shared \
--enable-exif=shared \
--with-ffi=shared \
--enable-ftp=shared \
--enable-gd=shared \
--with-webp=shared \
--with-jpeg=shared \
--with-webp=shared \
--with-avif=shared \
--with-gmp=shared \
--enable-intl=shared \
--with-ldap=shared \
--enable-mbstring=shared \
--with-openssl \
--with-pdo-mysql=shared \
--with-pdo-pgsql=shared \
--with-readline=shared \
--enable-sockets=shared \
--with-sodium=share \
--enable-soap=shared \
--with-libxml=shared \
--with-zip=shared

./config.nice

make -j $(nproc)
