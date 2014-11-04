import os
from lxml import etree

import cip
from cip.handler import BaseHandler
from cip.lru import lru_cache


class SoapValidationException(Exception):
    pass


class RequestTooLargeException(Exception):
    pass


class EmptyRequestException(Exception):
    pass


class SoapHandler(BaseHandler):

    def __init__(self, **kwargs):
        super(SoapHandler, self).__init__(**kwargs)

        self.root_dir = os.path.join(os.path.dirname(cip.__file__), '..')

        soap_xsd_path = os.path.join(self.root_dir, self.config['soap_xsd'])
        self.xsd_path = os.path.join(self.root_dir, self.config['xsd'])

        soap_xsd_parsed = etree.parse(soap_xsd_path)
        nomis_url = 'http://services.pvb.nomis.syscon.net/'
        xsd_import = etree.Element('{http://www.w3.org/2001/XMLSchema}import',
                                   namespace=nomis_url,
                                   schemaLocation=self.xsd_path)
        soap_xsd_parsed.getroot().insert(0, xsd_import)
        self.schema = etree.XMLSchema(soap_xsd_parsed)

    def get(self, request, path=None, next_handler=None):
        """
        On get we terminate request by retuning wsdl, xsd or 404.
        :param request:
        :param path:
        :param next_handler:
        :return:
        """
        if 'wsdl' in request.args:
            return self.handle_wsdl_request()
        elif 'xsd' in request.args:
            with open(self.xsd_path) as xsd:
                data = xsd.read()
                return data, 200, {'Content-Type': 'application/xml'}
        else:
            return request.args, 404, {}

    def post(self, request, path=None, next_handler=None):
        request_size = self.config.get('request_size', 8192)

        if len(request.data) > request_size:
            raise RequestTooLargeException

        parser = etree.XMLParser(resolve_entities=False, no_network=True)
        if request.data:
            soap_request = etree.fromstring(request.data, parser=parser)
        else:
            raise EmptyRequestException
        # If the request contains invalid XML then the following will throw
        # an exception that will be handled by the pipeline handling code.
        self.schema.assertValid(soap_request)
        response = next_handler()
        #alter me
        return response

    #TODO: add invalidation after i.e. 15mins
    @lru_cache(maxsize=16)
    def handle_wsdl_request(self):
        if len(self.config['wsdl']) > 4 and self.config['wsdl'][0:4] == 'http':
            wsdl_path = self.config['wsdl']
        else:
            wsdl_path = os.path.join(self.root_dir, self.config['wsdl'])
        x = etree.parse(wsdl_path)
        r = x.getroot()

        # TODO: Fix this mess.

        # hack #1: Set the schema location
        try:
            filter(lambda x:x.tag == '{http://schemas.xmlsoap.org/wsdl/}types',
                   r.getchildren())[0].getchildren()[0].getchildren()[0].set(
                   'schemaLocation', '{}?xsd=1'.format(
                    self.config['service_url']))
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


class SoapHandlerMock(SoapHandler):
    def post(self, request, path=None, next_handler=None):
        super(SoapHandlerMock, self).post(request, path, next_handler=next_handler)
        return "requested:{}".format(path), 200, {}