web: gunicorn root.wsgi --log-file -
celeryd: celery -A root.celery worker -E -B --loglevel=INFO