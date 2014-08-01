import os
from lxml import etree

import ianua
from ianua.handler import BaseHandler



class SoapValidationException(Exception):
    pass

class SoapHandler(BaseHandler):

    def __init__(self, **kwargs):
        super(SoapHandler, self).__init__(**kwargs)

        soap_xsd_path = os.path.join(os.path.dirname(ianua.__file__), '..', 'config/soap.xsd')
        soap_xsd_parsed = etree.parse(soap_xsd_path)

        xsd_path = os.path.join(os.path.dirname(ianua.__file__), '..', self.config['xsd'])
#        xsd_parsed = etree.parse(xsd_path)

        xsd_import = etree.Element('{http://www.w3.org/2001/XMLSchema}import',
            namespace="http://services.pvb.nomis.syscon.net/",
            schemaLocation=xsd_path)

        soap_xsd_parsed.getroot().insert(0, xsd_import)

        self.schema = etree.XMLSchema(soap_xsd_parsed)


        # soap_xsd_schema = etree.XMLSchema(soap_xsd_parsed)
        #
        # xsd_schema = etree.XMLSchema(xsd_parsed)
        #
        #
        # schema = etree.XMLSchema(file=xsd_path)
        # self.xml_parser = etree.XMLParser(schema=schema)

    def __call__(self, request, path=None):
        """
        enforces post method
        :param request:
        :param path:
        :return: None
        """
        req_method = request.method.lower()
        if req_method != 'post':
            raise SoapValidationException("method ({}) is not allowed".format(req_method))

        return self.post(request, path)

    def post(self, request, path):
        soap_request = etree.fromstring(request.data)
        self.schema.assertValid(soap_request)
