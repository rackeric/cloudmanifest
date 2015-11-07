from firebase import FirebaseApplication, FirebaseAuthentication
#from firebase import Firebase
import firebase
from celery.decorators import task
from ansible import utils
import ansible.runner, json, os
from flask.views import MethodView


# firebase can not use several special characters for key names
# https://www.firebase.com/docs/creating-references.html
def sanitize_keys(mydict):
    return dict((k.replace('.', '_'),sanitize_keys(v) if hasattr(v,'keys') else v) for k,v in mydict.items())


class AnsibleJeneric(MethodView):
    #@task()
    #decorators = [task]
    def get(self, user_id, project_id, job_id):
        #result = run_task.delay(user_id, project_id, job_id)
        result = run_task(user_id, project_id, job_id)
        return "sent"

@task()
def run_task(user_id, project_id, job_id):

    # firebase authentication
    SECRET = os.environ['SECRET']
    authentication = FirebaseAuthentication(SECRET, True, True)

    # set the specific job from firebase with user
    user = 'simplelogin:' + str(user_id)
    URL = 'https://deploynebula.firebaseio.com/users/' + user + '/projects/' + project_id + '/external_data/'
    #myExternalData = FirebaseApplication(URL)
    myExternalData = FirebaseApplication(URL, authentication)

    # update status to RUNNING in firebase
    myExternalData.patch(job_id, json.loads('{"status":"RUNNING"}'))

    # finally, get the actual job and set ansible options
    job = myExternalData.get(URL, job_id)

    # set vars from job data in firebase
    myHostList = job['host_list']
    myModuleName = job['module_name']
    if 'module_args' in job.keys():
        myModuleArgs = job['module_args']
    else:
        myModuleArgs = ''
    myPattern = job['pattern']
    myRemoteUser = job['remote_user']
    myRemotePass = job['remote_pass']
    myProjectID = job['project_id']

    # set and get Ansible Project Inventory
    URL = 'https://deploynebula.firebaseio.com/users/' + user + '/projects/' + myProjectID
    job = myExternalData.get(URL, 'inventory')

    # creating Ansible Inventory based on host_list
    myInventory = ansible.inventory.Inventory(myHostList)

        # set Host objects in Inventory object based on hosts_lists
        # NEED: to set other host options
        # BUG: hostnames with periods (.) do not work
    for key, host in job.iteritems():
        if host['name'] in myHostList:
            tmpHost = myInventory.get_host(host['name'])
            tmpHost.set_variable("ansible_ssh_host", host['ansible_ssh_host'])
            tmpHost.set_variable("ansible_ssh_user", host['ansible_ssh_user'])
            if host.has_key('ansible_ssh_pass'):
                tmpHost.set_variable("ansible_ssh_pass", host['ansible_ssh_pass'])
            # Group Stuffs
            if myInventory.get_group(host['group']) is None:
                # set up new group
                tmpGroup = ansible.inventory.Group(host['group'])
                tmpGroup.add_host(myInventory.get_host(host['name']))
                myInventory.add_group(tmpGroup)
            else:
                # just add to existing group
                tmpGroup = myInventory.get_group(host['group'])
                tmpGroup.add_host(myInventory.get_host(host['name']))

    # get ssh key file
    URL = 'https://deploynebula.firebaseio.com/users/' + user + '/projects/' + project_id
    ssh_key = myExternalData.get(URL, '/ssh_key')

    tmpKey = open("/tmp/" + project_id + '_key', "w")
    tmpKey.write(ssh_key)
        # close file
    tmpKey.close()
    os.chmod("/tmp/" + project_id + '_key', 0600)

        # run ansible module
    if ssh_key is not None:
        results = ansible.runner.Runner(
        pattern=myPattern,
           	forks=10,
     	module_name=myModuleName,
        module_args=myModuleArgs,
    	    #remote_user=myRemoteUser,
    	    #remote_pass=myRemotePass,
            private_key_file='/tmp/' + project_id + '_key',
    	inventory=myInventory,
        ).run()
    else:
        results = ansible.runner.Runner(
        pattern=myPattern,
       	    forks=10,
     	    module_name=myModuleName,
    	    module_args=myModuleArgs,
    	    #remote_user=myRemoteUser,
    	    #remote_pass=myRemotePass,
    	    inventory=myInventory
        ).run()


    # set status to COMPLETE
    myExternalData.patch(job_id, {"status":"COMPLETE"})

    # jsonify the results
    json_results = ansible.utils.jsonify(results)

        #
        # HELP! can't get a proper json object to pass, but below string works
        #
    myExternalData.post(job_id + '/returns/', sanitize_keys(results))
    os.remove('/tmp/' + project_id + '_key')

    return results
