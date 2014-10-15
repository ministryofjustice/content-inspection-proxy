FROM moj-base:latest
RUN rm -rf /etc/service/sshd /etc/my_init.d/00_regen_ssh_host_keys.sh
RUN apt-get update
RUN apt-get install -y libxml2-dev python-dev python-pip python-virtualenv libxslt1-dev zlib1g-dev
ADD . /cip
RUN useradd cip -g daemon -d /cip
RUN chown -R cip:daemon /cip
WORKDIR /cip/cip
RUN pip install -r /cip/requirements.txt
RUN mkdir -p /etc/service/gunicorn
ADD gunicorn.service /etc/service/gunicorn/run
EXPOSE 5000

