#!/bin/bash
if [ ! -e env ]
then
  python3 -m venv env --system-site-packages
fi
source env/bin/activate
pip3 install -r requirements.txt
python3 manage.py makemigrations --no-input
python3 manage.py migrate --no-input
python3 manage.py runscript scripts.init
chmod 777 -R media
if $DOCKER_DEV
then
  python3 manage.py runserver 0.0.0.0:8000 --noreload
  python3 manage.py collectstatic --noinput
else
  python3 manage.py collectstatic --noinput
  apache2ctl -D FOREGROUND
fi

