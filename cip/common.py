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
