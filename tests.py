import os
import manifest
import unittest
from manifest.tasks import convert_bash_colors
from manifest.tasks import sanitize_keys
from manifest.tasks import populate_playbooks
from mock import MagicMock
from firebase import FirebaseApplication


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

    def test_convert_bash_colors(self):
        string = "this i[0;32ms a string"
        result = convert_bash_colors(string)
        # self.assertEqual(result, "this is a string")
        string = "this i[0;32ms a string"

    def test_sanitize_keys(self):
        myDict = {'192.168.1.1': "my server"}
        expect = {'192_168_1_1': "my server"}
        result = sanitize_keys(myDict)
        self.assertEqual(result, expect)

    def test_populate_playcooks(self):
        mock_Firebase = FirebaseApplication("myurl", FirebaseAuthentication("mysecretstring", True, True))
        mock_Firebase.get = MagicMock()

        # run the actual function
        populate_playbooks(11, 'proj123', 'playbook123')

        user = 'simplelogin:11'
        project_id = 'proj123'
        URL = 'https://deploynebula.firebaseio.com/users/' + user + '/projects/' + project_id + '/rolesgit/'
        mock_Firebase.get.assert_called_with(URL, playbook_id)


if __name__ == '__main__':
    unittest.main()
