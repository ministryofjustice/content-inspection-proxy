FROM python:2.7
ADD . /cip
RUN useradd cip -g daemon -d /cip
RUN chown -R cip:daemon /cip
WORKDIR /cip/cip
RUN pip install -r /cip/requirements.txt
USER cip
EXPOSE 5000
ENTRYPOINT gunicorn -w 4 -b 0.0.0.0:5000 -k gevent --pythonpath /cip/ 'cip.wsgi:app'
