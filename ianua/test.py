import os
import wsgi
import unittest
from subprocess32 import Popen, PIPE
import time
import sys
from ianua.application import app_maker
from ianua.tests.soap_requests import *

class IanuaTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app_maker("../config/test.yaml").test_client()
        self.mock_server = Popen([sys.executable, 'ianua/tests/mock_server.py'])
        #TODO any clue how to correctly wait for output? readline() blocks

    def tearDown(self):
        self.mock_server.terminate()

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
        print type(self.app.post)
        response = self.app.post('/mock', data=soap_bookVisit_fixed)
        self.assertEqual(response.status_code, 200)
        path_passed = response.data.split(':')[1]
        self.assertEqual(path_passed, '/ws')

    def testSoap(self):
        print type(self.app.post)
        response = self.app.post('/soap', data=soap_bookVisit_fixed)
        self.assertEqual(response.status_code, 200)
        path_passed = response.data.split(':')[1]
        self.assertEqual(path_passed, '/ws')


if __name__ == '__main__':
    unittest.main()
