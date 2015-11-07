# CloudManifest

A web GUI for creating projects in Ansible and Saltstack, potentially Chef and Puppet in the future.

Now Built with:

- Flask
- AngularJS
- Firebase
- Bootstrap 3

Currently at https://cloudmanifest.com

## Other Stuff

You will need to export an environment variable named `SECRET` with the firebase api key.
```
$ export SECRET=<long api key from firebase>
```
When using ssh passwords host key checking will prevent you from connecting to hosts if they are not in your known_hosts file. You can get around this by either adding the host to the known_hosts file, using ssh keys or setting an enrivonrment variable `ANSIBLE_HOST_KEY_CHECKING=False`. 
```
$ export ANSIBLE_HOST_KEY_CHECKING=False
```
