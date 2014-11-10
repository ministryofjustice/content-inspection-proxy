import unittest
import time
from cip.application import app_maker
from cip.tests.soap_requests import *


class CIPTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app_maker("../config/test.yaml").test_client()

    def test404(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 404)

    def _testPathMapping(self, path, expected_mapped_path):
        response = self.app.get(path)
        self.assertEqual(response.status_code, 200)
        path_passed = response.data.split(':')[1]
        self.assertEqual(path_passed, expected_mapped_path)

    def testURLPassThroughMock(self):
        self._testPathMapping('/mock', '/ws')
        self._testPathMapping('/mock/foo', '/ws/foo')
        self._testPathMapping('/mock/', '/ws')  # flask way

    def testURLPassThrough(self):
        time.sleep(0.1)
        self._testPathMapping('/test', '/ws')
        self._testPathMapping('/test/', '/ws')  # flask way
        self._testPathMapping('/test/foo', '/ws/foo')

        self._testPathMapping('/slash', '/ws/')
        self._testPathMapping('/slash/', '/ws/')  # flask way
        self._testPathMapping('/slash/foo', '/ws/foo')

    def testPost(self):
        response = self.app.post('/mock', data=soap_bookVisit_fixed)
        self.assertEqual(response.status_code, 200)
        path_passed = response.data.split(':')[1]
        self.assertEqual(path_passed, '/ws')

    def testSoap(self):
        response = self.app.post('/soap', data=soap_bookVisit_fixed)
        self.assertEqual(response.status_code, 200)

    def test_production_logging(self):
        response = self.app.post('/soap', data='<broken>stuff</broken>')
        self.assertEqual(response.status_code, 500)
        #TODO: complete me...

    def test_long_string(self):
        response = self.app.post('/more_soap', data=soap_bookVisit_long)
        self.assertEqual(response.status_code, 500)

    def test_request_size(self):
        response = self.app.post('/little_soap', data=soap_bookVisit_fixed)
        self.assertEqual(response.status_code, 500)

    def test_inline_entity_expansion(self):
        response = self.app.post('/soap', data=soap_bookVisit_expansion)
        self.assertEqual(response.status_code, 500)

if __name__ == '__main__':
    unittest.main()
