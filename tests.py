import os
import manifest
import unittest
from manifest.tasks import convert_bash_colors
from manifest.tasks import sanitize_keys

class ManifestTestCase(unittest.TestCase):

    def setUp(self):
        self.app = manifest.app.test_client()

    def test_home_page(self):
        result = self.app.get('/')
        assert 'Manifest' in result.data
        self.assertEqual(result.status_code, 200)

    #def test_login_page(self):
    #    result = self.app.get('/#/login')
    #    self.assertEqual(result.status_code, 200)

    def test_remove_bash_colors(self):
        string = "this i[0;32ms a string"
        result = convert_bash_colors(string)
        assert '[0;32m' not in result
        string = "this i[0;32ms a string"

    def test_sanitize_keys(self):
        string = "192.168.1.1"
        result = sanitize_keys(string)
        self.assertEqual(result, "192_168_1_1")

if __name__ == '__main__':
    unittest.main()
