import os
import manifest
import unittest
from manifest.tasks import convert_bash_colors

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
        self.assertEqual(result, "this is a string")

if __name__ == '__main__':
    unittest.main()
