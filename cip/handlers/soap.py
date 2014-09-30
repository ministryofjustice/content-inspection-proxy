import os
from lxml import etree

import cip
from cip.handler import BaseHandler


class SoapValidationException(Exception):
    pass


class RequestTooLargeException(Exception):
    pass


class SoapHandler(BaseHandler):

    def __init__(self, **kwargs):
        super(SoapHandler, self).__init__(**kwargs)

        self.root_dir = os.path.dirname(cip.__file__)
        soap_xsd_path = os.path.join(self.root_dir, '..',
                                     self.config['soap_xsd'])
        self.xsd_path = os.path.join(self.root_dir, '..', self.config['xsd'])
        custom_xsd = os.path.join(self.root_dir, '..', 'config',
                                  'nomis_test1.xsd')

        try:
            xml_config = self.config['xml_config']
            out = custom_xsd
            self.inject_schema(xml_config, custom_xsd)
        except KeyError:
            out = self.xsd_path
            if os.path.exists(custom_xsd):
                os.unlink(custom_xsd)

        soap_xsd_parsed = etree.parse(soap_xsd_path)
        nomis_url = 'http://services.pvb.nomis.syscon.net/'
        xsd_import = etree.Element('{http://www.w3.org/2001/XMLSchema}import',
                                   namespace=nomis_url,
                                   schemaLocation=out)
        soap_xsd_parsed.getroot().insert(0, xsd_import)
        self.schema = etree.XMLSchema(soap_xsd_parsed)

    def inject_schema(self, xml_config, out):
        moj_path = os.path.join(self.root_dir, '..', xml_config['custom_def'])
        moj_import = etree.Element('{http://www.w3.org/2001/XMLSchema}import',
                                   namespace='moj',
                                   schemaLocation=moj_path)
        nomis_xsd_parsed = etree.parse(self.xsd_path)

        # replace xs:string with moj:LimitedString
        namespaces = {'xs': 'http://www.w3.org/2001/XMLSchema'}
        if 'transformations' in xml_config:
            for src, dst in xml_config['transformations'].items():
                xpath_query = '//xs:element[@type="{}"]'.format(src)
                for elm in nomis_xsd_parsed.findall(
                        xpath_query, namespaces=namespaces):
                    elm.set('type', dst)

        # lxml doesn't provide a way to change the namespace map
        # so we need to create a new root...

        nomis = nomis_xsd_parsed.getroot()
        nsmap = nomis.nsmap
        nsmap['moj'] = 'moj'
        new_root = etree.Element(nomis.tag, nsmap=nsmap)
        for key in nomis.keys():
            new_root.set(key, nomis.get(key))
        new_root[:] = nomis[:]
        new_root.insert(0, moj_import)
        with open(out, 'w') as xml_out:
            xml_out.write(etree.tostring(new_root, pretty_print=True,
                                         xml_declaration=True))

    # def __call__(self, request, path=None):
    #     """
    #     enforces post method
    #     :param request:
    #     :param path:
    #     :return: None
    #     """
    #     if request.method.lower() != 'post':
    #         raise SoapValidationException(
    #             "method ({}) is not allowed".format(request.method.lower()))
    #     return self.post(request, path)

    def base_method(self, request, path=None, method=None):
        methods = {'get': self.get,
                   'post': self.post}
        method = methods.get(method, path)
        if not method:
            raise SoapValidationException(
                "method ({}) is not allowed".format(request.method.lower()))
        return method(request, path=path)

    def post(self, request, path=None):
        request_size = self.config.get('request_size', 8192)

        if len(request.data) > request_size:
            raise RequestTooLargeException

        parser = etree.XMLParser(resolve_entities=False, no_network=True)
        soap_request = etree.fromstring(request.data, parser=parser)
        self.schema.assertValid(soap_request)

    def handle_wsdl_request(self):
        wsdl_path = os.path.join(self.root_dir, '..', self.config['wsdl'])
        x = etree.parse(wsdl_path)
        r = x.getroot()

        # TODO: Fix this mess.

        # hack #1: Set the schema location
        try:
            filter(lambda x:x.tag == '{http://schemas.xmlsoap.org/wsdl/}types',
                   r.getchildren())[0].getchildren()[0].getchildren()[0].set(
                'schemaLocation', '{}?xsd=1'.format(self.config['service_url']))
        except:
            self.log.debug('Failed to set xsd location in wsdl')

        # hack #2: Set the service location
        try:
            filter(lambda x:x.tag=='{http://schemas.xmlsoap.org/wsdl/}service',
                   r.getchildren())[0].getchildren()[0].getchildren()[0].set(
                'location', self.config['service_url'])
        except:
            self.log.debug('Failed to set service url')
        return (etree.tostring(r, pretty_print=True, xml_declaration=True),
                200, {'Content-Type': 'application/xml'})

    def get(self, request, path=None):
        if 'wsdl' in request.args:
            return self.handle_wsdl_request()
        elif 'xsd' in request.args:
            with open(self.xsd_path) as xsd:
                data = xsd.read()
                return (data, 200, {'Content-Type': 'application/xml'})
        else:
            return(request.args, 404, {})


class SoapHandlerMock(SoapHandler):
    def post(self, request, path=None):
        super(SoapHandlerMock, self).post(request, path)
        return ("requested:{}".format(path), 200, {})