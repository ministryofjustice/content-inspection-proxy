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

    def __call__(self, request, path=None):
        """
        enforces post method
        :param request:
        :param path:
        :return: None
        """
        if request.method.lower() != 'post':
            raise SoapValidationException(
                "method ({}) is not allowed".format(request.method.lower()))
        return self.post(request, path)

    def post(self, request, path=None):
        request_size = self.config.get('request_size', 8192)

        if len(request.data) > request_size:
            raise RequestTooLargeException

        parser = etree.XMLParser(resolve_entities=False, no_network=True)
        soap_request = etree.fromstring(request.data, parser=parser)
        self.schema.assertValid(soap_request)


class SoapHandlerMock(SoapHandler):
    def post(self, request, path=None):
        super(SoapHandlerMock, self).post(request, path)
        return "requested:{}".format(path)