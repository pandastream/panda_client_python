import unittest
from nose.tools import *
import panda

class PropertiesTest(unittest.TestCase):
    def setUp(self):
        self.i = panda.Panda(cloud_id='my-cloud-id', access_key='my-access-key', secret_key='my-secret-key')

    def test_cloud_id(self):
        eq_(self.i.cloud_id, 'my-cloud-id')

    def test_access_key(self):
        eq_(self.i.access_key, 'my-access-key')

    def test_secret_key(self):
        eq_(self.i.secret_key, 'my-secret-key')

    def test_api_host(self):
        eq_(self.i.api_host, 'api.pandastream.com')

    def test_api_port(self):
        eq_(self.i.api_port, 80)
