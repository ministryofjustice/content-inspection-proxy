FROM    moj-base:latest

RUN     rm -rf /etc/service/sshd /etc/my_init.d/00_regen_ssh_host_keys.sh
RUN     apt-get update

RUN     apt-get install -y redis-server redis-tools
RUN     mkdir -p /etc/service/redis
ADD     redis.service /etc/service/redis/run

RUN     apt-get install -y libxml2-dev python-dev python-pip python-virtualenv libxslt1-dev zlib1g-dev
ADD     requirements.txt /cip/requirements.txt
RUN     pip install -r /cip/requirements.txt

ADD     . /cip
RUN     useradd cip -g daemon -d /cip
RUN     chown -R cip:daemon /cip
WORKDIR /cip/cip
RUN     mkdir -p /etc/service/gunicorn
ADD     gunicorn.service /etc/service/gunicorn/run

ADD     logstash-conf.sh /etc/logstash-conf.sh

ENV     PROJECT pvb-cip
ENV     APPVERSION 0.0.1
ENV     ENV dev

RUN     find /etc/service -name run -exec chmod +x \{\} \;

#TODO: make decent default so that it is silent for dev
#RUN     rm -Rf /etc/service/statsd
#RUN     rm -Rf /etc/service/logstash

EXPOSE  5000
