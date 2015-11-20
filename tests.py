import os
import manifest
import unittest
from manifest.tasks import convert_bash_colors
from manifest.tasks import sanitize_keys
from manifest.tasks import populate_playbooks
from manifest.tasks import run_ansible_jeneric
from mock import patch
from firebase import FirebaseApplication
from firebase import FirebaseAuthentication
from git import Repo
import glob
import shutil
from mock import MagicMock
import json


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

    def test_populate_playbooks(self):
        with patch.object(FirebaseApplication, 'get', return_value='playbook') as mock_FirebaseApplication:
            with patch.object(Repo, 'clone_from', return_value='something') as mock_Repo:
                with patch.object(glob, 'glob', return_value='play.yml') as mock_glob:
                    with patch.object(shutil, 'rmtree', return_value='nothing') as mock_shutil:
                        with patch.object(FirebaseApplication, 'post', return_value='nothing') as mock_FirebaseApplication_post:
                            mock_FirebaseAuthentication = FirebaseAuthentication("secret", True, True)
                            mock_FirebaseAuthentication.__main__ = MagicMock(return_value="myauth")
                            populate_playbooks(11, 'proj123', 'playbook123')

        user = 'simplelogin:11'
        project_id = 'proj123'
        URL = 'https://deploynebula.firebaseio.com/users/' + user + '/projects/' + project_id + '/rolesgit/'

        #assert mock_FirebaseAuthentication.__main__.called
        #mock_FirebaseApplication.assert_called_with(URL, FirebaseAuthentication("SECRET", True, True))
        assert mock_FirebaseApplication.called

        git_url = "play.yml"
        git_dir = '/tmp/' + project_id + 'playbook'
        mock_Repo.assert_called_once_with("playbook", git_dir)

        mock_glob.assert_called_once_with(git_dir + '/*.y*ml')

        mock_shutil.assert_called_once_with(git_dir)

        #mock_FirebaseApplication_post.assert_called_with("playbook123" + '/playbooks', {'name': "play.yml"})
        assert mock_FirebaseApplication_post.called

    def test_run_ansible_jeneric(self):
        extData = {"host_list" : [ "test1", "cloudserver1", "host1" ],
                   "module_name" : "ping",
                   "pattern" : "all",
                   "module_args" : "",
                   "project_id" : "proj123",
                   "remote_pass" : "lkjlkj",
                   "remote_user" : "root",
                   # inventory options
                   "name": "server1",
                   "group": "group1",
                   "ansible_ssh_host": "host1",
                   "ansible_ssh_user": "root"}
        with patch.object(FirebaseApplication, 'get', return_value=extData) as mock_FirebaseApplication:
            with patch.object(FirebaseApplication, 'patch', return_value=None) as mock_FirebaseApplication_post:
                mock_FirebaseAuthentication = FirebaseAuthentication("secret", True, True)
                mock_FirebaseAuthentication.__main__ = MagicMock(return_value="myauth")
                run_ansible_jeneric(11, 'proj123', 'job123')

        user = 'simplelogin:11'
        project_id = 'proj123'
        URL = 'https://deploynebula.firebaseio.com/users/' + user + '/projects/' + project_id + '/rolesgit/'

        assert mock_FirebaseApplication.called
        assert mock_FirebaseApplication_post.called



if __name__ == '__main__':
    unittest.main()
