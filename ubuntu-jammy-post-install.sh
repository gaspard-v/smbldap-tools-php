#!/bin/bash

set -euo pipefail

sudo apt update
sudo apt install -y software-properties-common
sudo add-apt-repository -y ppa:ondrej/php
sudo apt update
sudo apt install -y \
php8.3 \
php8.3-fpm \
php8.3-cli \
php8.3-ldap \
php8.3-mbstring \
php8.3-oauth \
php8.3-xml \
php8.3-xdebug \
php8.3-curl