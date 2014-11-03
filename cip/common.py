import socket
import time
from flask import current_app

xml_error = '''
<?xml version='1.0' encoding='UTF-8'?>
<S:Envelope xmlns:S="http://schemas.xmlsoap.org/soap/envelope/">
    <S:Body>
        <S:Fault xmlns:ns4="http://www.w3.org/2003/05/soap-envelope">
            <faultcode>S:Server</faultcode>
            <faultstring>{}</faultstring>
        </S:Fault>
    </S:Body>
</S:Envelope>'''


# TODO: make this configurable
# Commented out for now since this functionality has been put on hold
def post_stat(key, value, stat_type):
    config = current_app.config
    logger = current_app.logger
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((config['collectd_host'], int(config['collectd_port'])))
        s.send('{}:{}|{}\n'.format(key, value, stat_type))
        s.close()
    except Exception:
        # metrics although serious are not worthy of dropping the request
        # Just log it and set an alert on the fact that we somehow
        # failed miserably.
        logger.exception('Error while sending stats.')


# default is microseconds
def get_duration(req_start_dt, multiplier=1000000):
    end_dt = time.time()
    return int((end_dt - req_start_dt) * multiplier)
