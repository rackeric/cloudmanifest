import os
import manifest
import unittest

class ManifestTestCase(unittest.TestCase):

    def setUp(self):
        self.app = manifest.app.test_client()

    def test_home(self):
        request = self.app.get('/')
        assert 'Manifest' in rv.data
        self.assertEqual(result.status_code, 200)

if __name__ == '__main__':
    unittest.main()
