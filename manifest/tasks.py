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
        result = run_ansible_jeneric(user_id, project_id, job_id)
        return result


class AnsiblePlaybook(MethodView):
    def get(self, user_id, project_id, playbook_id):
        result = run_ansible_playbook(user_id, project_id, playbook_id)
        return result


#@task()
def run_ansible_jeneric(user_id, project_id, job_id):

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

    # run ansible module
    if ssh_key is not None:
        // set up ssh key in tmp
        tmpKey = open("/tmp/" + project_id + '_key', "w")
        tmpKey.write(ssh_key)
            # close file
        tmpKey.close()
        os.chmod("/tmp/" + project_id + '_key', 0600)

        // now the ansible runner
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


#@celery.task(serializer='json')
def run_ansible_playbook(user_id, project_id, playbook_id):

    # firebase authentication
    SECRET = os.environ['SECRET']
    authentication = FirebaseAuthentication(SECRET, True, True)

    # set the specific job from firebase with user
    user = 'simplelogin:' + str(user_id)
    URL = 'https://deploynebula.firebaseio.com/users/' + user + '/projects/' + project_id + '/roles/'
    myExternalData = FirebaseApplication(URL, authentication)

    # update status to RUNNING in firebase
    myExternalData.patch(playbook_id, {"status":"RUNNING"})

    # finally, get the actual job and set ansible options
    job = myExternalData.get(URL, playbook_id)


    ##
    ## Create full Ansible Inventory, playbook defines hosts to run on
    ##
    # set and get Ansible Project Inventory
    URL = 'https://deploynebula.firebaseio.com/users/' + user + '/projects/' + project_id
    inventory_list = myExternalData.get(URL, '/inventory')


    tmpHostList = []
    for key, host in inventory_list.iteritems():
        tmpHostList.append(host['name'])

    # creating Ansible Inventory based on host_list
    myInventory = ansible.inventory.Inventory(tmpHostList)

    # set Host objects in Inventory object based on hosts_lists
    # NEED: to set other host options
    # BUG: hostnames with periods (.) do not work
    for key, host in inventory_list.iteritems():
        tmpHost = myInventory.get_host(host['name'])
        tmpHost.set_variable("ansible_ssh_host", host['ansible_ssh_host'])
        tmpHost.set_variable("ansible_ssh_user", host['ansible_ssh_user'])
        if host.has_key('ansible_ssh_user'):
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


    ##
    ## Create temp playbook file
    ##
    URL = 'https://deploynebula.firebaseio.com/users/' + user + '/projects/' + project_id + '/roles/'
    playbook = myExternalData.get(URL, playbook_id)

    # order tasks in playbook base on order field in dict
    def func(key):
        return playbook['modules'][key]['order']
    sorted_tasks_keys = sorted(playbook['modules'].keys(), key=func)

    tmpPlay = open("/tmp/" + playbook_id + '.yml', "w")

    tmpPlay.write("---\n")
    tmpPlay.write("- name: %s\n" % playbook['name'])
    tmpPlay.write("  hosts: %s\n" % playbook['playHosts'])
    tmpPlay.write("  remote_user: %s\n" % playbook['playUsername'])
    tmpPlay.write("\n")
    # if has variables
    if playbook.has_key('variables'):
        tmpPlay.write("  vars:\n")
        for key, var in playbook['variables'].iteritems():
            tmpPlay.write("    %s: %s\n" % (var['name'], var['value']))
        tmpPlay.write("\n")
    # if has tasks
    if playbook.has_key('modules'):
        tmpPlay.write("  tasks:\n")
        # if has includes
        if playbook.has_key('includes'):
            for key, include in playbook['includes']:
                tmpPlay.write("    - include: %s" % include['name'])
        # now for the tasks
        for key in sorted_tasks_keys:
            tmpPlay.write("    - name: %s\n" % playbook['modules'][key]['name'])
            tmpPlay.write("      %s: " % playbook['modules'][key]['option'])
            for option in playbook['modules'][key]['options']:
                # for command and shell modules one-off crapness
                if option['paramater']:
                    tmpPlay.write("%s=%s " % (option['paramater'], option['value']))
                else:
                    tmpPlay.write("%s " % option['value'])
            tmpPlay.write("\n")
            # if has notify
            if option.has_key('notify'):
                tmpPlay.write("      notify:\n")
                tmpPlay.write("        - %s\n" % option['notify'])
            tmpPlay.write("\n")
    # if has handlers
    if playbook.has_key('handlers'):
        tmpPlay.write("  handlers:\n")
        for key, handler in playbook['handlers'].iteritems():
            tmpPlay.write("    - name: %s\n" % handler['name'])
            tmpPlay.write("      service: name=%s state=%s\n\n" % (handler['service_name'], handler['service_state']))

    # close file
    tmpPlay.close()

    # get ssh key file
    URL = 'https://deploynebula.firebaseio.com/users/' + user + '/projects/' + project_id
    ssh_key = myExternalData.get(URL, '/ssh_key')

    prev = sys.stdout
    prev2 = sys.stderr
    try:
        sys.stdout = StringIO()
        sys.stderr = StringIO()

        # Run Ansible PLaybook
        stats = ansible.callbacks.AggregateStats()
        playbook_cb = ansible.callbacks.PlaybookCallbacks(verbose=utils.VERBOSITY)
        runner_cb = ansible.callbacks.PlaybookRunnerCallbacks(stats, verbose=utils.VERBOSITY)

        if ssh_key is not None:
            # set up ssh key in tmp
            tmpKey = open("/tmp/" + playbook_id + '_key', "w")
            tmpKey.write(ssh_key)
            # close file
            tmpKey.close()
            os.chmod("/tmp/" + playbook_id + '_key', 0600)

            # now ansible playbook
            play = ansible.playbook.PlayBook(
                playbook='/tmp/' + playbook_id + '.yml',
                inventory=myInventory,
                runner_callbacks=runner_cb,
                stats=stats,
                callbacks=playbook_cb,
                private_key_file='/tmp/' + playbook_id + '_key',
                forks=10
            ).run()
        else:
            play = ansible.playbook.PlayBook(
                playbook='/tmp/' + playbook_id + '.yml',
                inventory=myInventory,
                runner_callbacks=runner_cb,
                stats=stats,
                callbacks=playbook_cb,
                forks=10
            ).run()

        myStdout = sys.stdout.getvalue()
        myStderr = sys.stderr.getvalue()
        #myExternalData.patch(playbook_id, {'stdout': myStdout})
        myExternalData.post(playbook_id + '/returns', {'stats': sanitize_keys(play), 'stdout': myStdout})
        #myExternalData.patch(playbook_id, {'stderr': myStderr})
    finally:
        sys.stdout = prev
        sys.stderr = prev2

    ##
    ## Post play results in to firebase
    ##
    ## WHERE?
    # update status to RUNNING in firebase
    myExternalData.patch(playbook_id, {"status":"COMPLETE"})
    #myExternalData.post(playbook_id + '/returns', play)

    # delete tmp playbook file
    os.remove('/tmp/' + playbook_id + '.yml')
    # delete tmp key file
    os.remove('/tmp/' + playbook_id + '_key')

    return play
