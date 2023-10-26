#!/bin/bash

# Collect static files
echo "<<<<<<<<<< Collect static files >>>>>>>>>>"
#python manage.py collectstatic --noinput
python manage.py collectstatic --noinput --settings=project.settings.production

# Apply database migrations
echo "----------- Apply database migrations ----------"
python manage.py makemigrations --settings=project.settings.production
python manage.py migrate --settings=project.settings.production
# Start server
echo "------- Starting server ------------"
gunicorn project.wsgi --bind 0.0.0.0:8000 --workers 3 
