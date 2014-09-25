FROM python:2.7
ADD . /srv
WORKDIR /srv/cip
RUN pip install -r /srv/requirements.txt
EXPOSE 5000
ENTRYPOINT gunicorn -w 4 -b 0.0.0.0:5000 -k gevent --pythonpath /srv/ 'cip.wsgi:app'
