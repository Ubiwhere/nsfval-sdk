import unittest
import os
from nsfval.sdk import validator


class UnitValidateTests(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(UnitValidateTests, self).__init__(*args, **kwargs)
        self.resource_path = os.path.join(os.path.dirname(__file__), 'resources')

    def test_validate_ns_pass(self):

        result = validator.validate_ns('osm', 's', os.path.join(self.resource_path, 'osm/nsd/cirros_nsd.yaml'))
        self.assertEquals(result['error_count'], result['warning_count'], 0)

        addt_files = [os.path.join(self.resource_path, 'osm/vnfd/cirros_vnfd.yaml'),
                      os.path.join(self.resource_path, 'osm/vnfd/ref11_vnfd.yaml')]
        result = validator.validate_ns('osm', 'sit', os.path.join(self.resource_path, 'osm/nsd/cirros_nsd.yaml',),
                                       addt_files=addt_files)
        self.assertEquals(result['error_count'], result['warning_count'], 0)

    def test_validate_ns_fail(self):
        result = validator.validate_ns('osm', 'sit', os.path.join(self.resource_path, 'osm/nsd/cirros_nsd.yaml'))
        self.assertEquals(result['error_count'], 1)

    def test_to_fail(self):
        # addt_files = [os.path.join(self.resource_path, 'osm/vnfd/cirros_vnfd.yaml')]
        # result = nsfval.validate_ns('osm', 'sit', os.path.join(self.resource_path, 'osm/nsd/cirros_nsd.yaml', ),
        #                             addt_files=addt_files)
        # self.assertEquals(result['error_count'], result['warning_count'], 0)

        result = validator.validate_ns('osm', 'sit', os.path.join(self.resource_path, 'osm/nsd/cirros_nsd.yaml'))
        self.assertEquals(result['error_count'], 1)

        result = validator.validate_ns('osm', 's', os.path.join(self.resource_path, 'osm/nsd/cirros_nsd.yaml'))
        self.assertEquals(result['error_count'], 0)

        result = validator.validate_ns('osm', 'sit', os.path.join(self.resource_path, 'osm/nsd/cirros_nsd.yaml'))
        self.assertEquals(result['error_count'], 1)
