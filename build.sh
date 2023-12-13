#!/usr/bin/env bash
# exit on error
set -o errexit

#Esto lo añadimos nosotros en lugar del servicio Poetry propuesto por Render.
pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate
