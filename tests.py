import os
import manifest
import unittest
from manifest.tasks import convert_bash_colors
from manifest.tasks import sanitize_keys
from manifest.tasks import populate_playbooks
from manifest.tasks import run_ansible_jeneric
from manifest.tasks import run_ansible_playbook
from manifest.tasks import run_ansible_playbook_manual
from mock import patch
from firebase import FirebaseApplication
from firebase import FirebaseAuthentication
from git import Repo
import glob
import shutil
from mock import MagicMock
import json
import ansible.runner

class ManifestTestCase(unittest.TestCase):

    def setUp(self):
        self.app = manifest.app.test_client()

    def test_home_page(self):
        result = self.app.get('/')
        assert 'Manifest' in result.data
        self.assertEqual(result.status_code, 200)

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
        with patch.object(FirebaseApplication, 'get', return_value='playbook') as mock_FirebaseApplication_get:
            with patch.object(Repo, 'clone_from', return_value='something') as mock_Repo:
                with patch.object(os, 'chdir', return_value=None) as mock_chdir:
                    with patch.object(glob, 'glob', return_value='play.yml') as mock_glob:
                        with patch.object(shutil, 'rmtree', return_value='nothing') as mock_shutil:
                            with patch.object(FirebaseApplication, 'post', return_value='nothing') as mock_FirebaseApplication_post:
                                mock_FirebaseAuthentication = FirebaseAuthentication("secret", True, True)
                                mock_FirebaseAuthentication.__main__ = MagicMock(return_value="myauth")
                                populate_playbooks(11, 'proj123', 'playbook123')

        project_id = 'proj123'
        git_url = "play.yml"
        git_dir = '/tmp/' + project_id + 'playbook'
        assert mock_FirebaseApplication_get.called
        mock_Repo.assert_called_once_with("playbook", git_dir)
        mock_chdir.assert_called_once_with(git_dir)
        mock_glob.assert_called_once_with('*.y*ml')
        mock_shutil.assert_called_once_with(git_dir)
        assert mock_FirebaseApplication_post.called

    @patch.object(FirebaseApplication, 'get')
    def test_run_ansible_jeneric(self, mock_FirebaseApplication_get):
        extData = {
                   "host_list" : [ "test1", "cloudserver1", "host1" ],
                   "module_name" : "ping",
                   "pattern" : "all",
                   "module_args" : "",
                   "project_id" : "proj123",
                   "remote_pass" : "lkjlkj",
                   "remote_user" : "root"
                   }
        inventory = {
                     "key1" :
                        {
                         "name": "host1",
                         "group": "group1",
                         "ansible_ssh_host": "host1",
                         "ansible_ssh_user": "root"
                        }
                    }
        sshkey = None
        list_of_return_values = [extData, inventory, sshkey]

        mock_FirebaseApplication_get.side_effect = list_of_return_values

        with patch.object(FirebaseApplication, 'patch', return_value=None) as mock_FirebaseApplication_patch:
            with patch.object(FirebaseApplication, 'post', return_value=None) as mock_FirebaseApplication_post:
                with patch.object(ansible.runner.Runner, 'run', return_value=inventory) as mock_ansibleRunner:
                    mock_FirebaseAuthentication = FirebaseAuthentication("secret", True, True)
                    mock_FirebaseAuthentication.__main__ = MagicMock(return_value="myauth")
                    run_ansible_jeneric(11, 'proj123', 'job123')

        assert mock_FirebaseApplication_get.called
        assert mock_FirebaseApplication_patch.called
        assert mock_FirebaseApplication_post.called
        assert mock_ansibleRunner.called

    @patch.object(FirebaseApplication, 'get')
    def test_run_ansible_playbook(self, mock_FirebaseApplication):
        extData = {
                   "host_list" : [ "test1", "cloudserver1", "host1" ],
                   "module_name" : "ping",
                   "pattern" : "all",
                   "module_args" : "",
                   "project_id" : "proj123",
                   "remote_pass" : "lkjlkj",
                   "remote_user" : "root"
                  }
        inventory = {
                     "key1" :
                        {
                         "name": "host1",
                         "group": "group1",
                         "ansible_ssh_host": "host1",
                         "ansible_ssh_user": "root",
                         "ansible_ssh_pass": "lkjlkjljk"
                        }
                    }
        role = {
                "name": "role1",
                "playHosts": "all",
                "user_id": "simplelogin:11",
                "modules":
                    {
                    "module1":
                        {
                        "name": "install_vim",
                        "option": "yum",
                        "order": 1,
                        "user_id": "simplelogin:11",
                        "options": [{"comment": "this is a comment", "paramater": "name", "required": "yes", "value": "vim"}]
                        }
                    }
                }
        sshkey = None
        list_of_return_values = [extData, inventory, role, sshkey]

        mock_FirebaseApplication.side_effect = list_of_return_values

        with patch.object(FirebaseApplication, 'patch', return_value=None) as mock_FirebaseApplication_patch:
            with patch.object(FirebaseApplication, 'post', return_value=None) as mock_FirebaseApplication_post:
                with patch.object(ansible.runner.Runner, 'run', return_value=inventory) as mock_ansibleRunner:
                    mock_FirebaseAuthentication = FirebaseAuthentication("secret", True, True)
                    mock_FirebaseAuthentication.__main__ = MagicMock(return_value="myauth")
                    run_ansible_playbook(11, 'proj123', 'job123')

        assert mock_FirebaseApplication.called
        assert mock_FirebaseApplication_patch.called
        assert mock_FirebaseApplication_post.called
        assert mock_ansibleRunner.called


    @patch.object(FirebaseApplication, 'get')
    def test_run_ansible_playbook_manual(self, mock_FirebaseApplication):
        extData = {
                   "name" : "man1",
                   "playbook" : "---\n- name: install_vim\n  hosts: all\n  gather_facts: yes\n  remote_user: root\n  \n  \n  tasks:\n\n    - name: install_vim\n      yum: name=vim\n\n    - name: install_ansible\n      yum: name=ansible\n\n    - name: install_elinks\n      yum: name=elinks",
                   "type" : "manual",
                   "user_id" : "simplelogin:11"
                  }

        inventory = {
                     "key1" :
                        {
                         "name": "host1",
                         "group": "group1",
                         "ansible_ssh_host": "host1",
                         "ansible_ssh_user": "root",
                         "ansible_ssh_pass": "lkjlkjljk"
                        }
                    }
        playbook = "---\n- name: install_vim\n  hosts: all\n  gather_facts: yes\n  remote_user: root\n  \n  \n  tasks:\n\n    - name: install_vim\n      yum: name=vim\n\n    - name: install_ansible\n      yum: name=ansible\n\n    - name: install_elinks\n      yum: name=elinks"
        sshkey = None
        list_of_return_values = [extData, inventory, playbook, sshkey]

        mock_FirebaseApplication.side_effect = list_of_return_values

        with patch.object(FirebaseApplication, 'patch', return_value=None) as mock_FirebaseApplication_patch:
            with patch.object(FirebaseApplication, 'post', return_value=None) as mock_FirebaseApplication_post:
                with patch.object(ansible.runner.Runner, 'run', return_value=inventory) as mock_ansibleRunner:
                    mock_FirebaseAuthentication = FirebaseAuthentication("secret", True, True)
                    mock_FirebaseAuthentication.__main__ = MagicMock(return_value="myauth")
                    run_ansible_playbook_manual(11, 'proj123', 'job123')

        assert mock_FirebaseApplication.called
        assert mock_FirebaseApplication_patch.called
        assert mock_FirebaseApplication_post.called
        assert mock_ansibleRunner.called

if __name__ == '__main__':
    unittest.main()
