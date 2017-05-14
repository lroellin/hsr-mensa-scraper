#!/bin/sh
set -e
set -x

git pull
killall -9 uwsgi || true
nohup uwsgi -s /srv/http/hsr-mensa-scraper/uwsgi.sock --chmod-socket=666 --manage-script-name --mount /=rest:application --plugin python3 &
service nginx restart