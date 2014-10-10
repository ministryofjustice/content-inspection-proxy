FROM moj-base:0.9.12
RUN apt-get update
RUN apt-get install -y libxml2-dev python-dev python-pip python-virtualenv libxslt1-dev zlib1g-dev
ADD . /cip
RUN useradd cip -g daemon -d /cip
RUN chown -R cip:daemon /cip
WORKDIR /cip/cip
RUN pip install -r /cip/requirements.txt
USER cip
EXPOSE 5000
ENTRYPOINT gunicorn -w 4 -b 0.0.0.0:5000 -k gevent --pythonpath /cip/ 'cip.wsgi:app'
