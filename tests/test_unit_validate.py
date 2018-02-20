import unittest
import os


class UnitValidateTests(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(UnitValidateTests, self).__init__(*args, **kwargs)
        self.resource_path = os.path.join(os.path.dirname(__file__), 'resources')

    def test_validate_ns_pass(self):
        from nsfval.sdk import sdk as nsfval
        result = nsfval.validate_ns('osm', 's', os.path.join(self.resource_path, 'osm/nsd/cirros_nsd.yaml'))
        self.assertEquals(result['error_count'], result['warning_count'], 0)
