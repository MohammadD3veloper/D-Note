web: gunicorn root.wsgi --log-file -
celeryd: celery -A root worker -l INFO -c 4