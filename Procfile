web: gunicorn main:server --log-file=-
worker: celery -A app.inv.tasks worker --loglevel=info
