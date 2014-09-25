# import socket
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
def post_stat(key, value, type):
    # try:
    #     s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #     s.connect(('127.0.0.1', 8125))
    #     s.send('{}:{}|{}\n'.format(key, value, type))
    #     s.close()
    # except Exception:
    #     pass
    pass