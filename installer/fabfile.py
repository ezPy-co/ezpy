from fabric.api import run, env, prompt, execute, sudo, open_shell, put
from fabric.contrib.project import rsync_project
from fabric.contrib.files import exists
import boto.ec2
import time
import os

env.aws_region = 'us-west-2'

env.hosts = ['localhost', ]
env.key_filename = '~/.ssh/pk-ins.pem'

env.myhost = 'ec2-54-149-69-177.us-west-2.compute.amazonaws.com'

# remote app directory
env.remote_directory = '~/installer'

# local app directory
env.local_directory = '~/projects/ezpy/'


def active():
    """Shows what instance is active"""
    if env.get('active_instance'):
        print "Active Instance: " + env.get('active_instance')
    else:
        print "No active instance"


def ssh_installer():
    ssh(host_=env.myhost)


def ssh(host_=None):
    """run an open shell"""
    run_command_on_selected_server(open_shell, host_=host_)


def host_type():
    run('uname -s')


def _deploy_app():
    """run this on server to uploading app to server"""
    rsync_project(env.remote_directory, env.local_directory,
                  exclude=['.git/', '*.pyc', 'tests.py', 'migrations/'])
    sudo('service installer_app restart')


def deploy_app(host_=None):
    """choose a in instance and upload app to server """
    run_command_on_selected_server(_deploy_app, host_=host_)


def deploy_installer(l_dir=env.local_directory):
    """Deploys package installer to our remote location
    Can set local location by using l_dir='<local path>'
    """
    env.local_directory = l_dir
    deploy_app(host_=env.myhost)



def _config_nginx():
    """configures nginx and return True if given path exists on host"""
    if exists('/etc/nginx/sites-available/', use_sudo=False, verbose=False):
        print "/etc/nginx/sites-available/ exists."
        put(os.path.join(env.local_directory, 'installer/simple_nginx_config'),
            '/etc/nginx/sites-available/default',
            use_sudo=True)
    else:
        print "Could't configure nginx because /etc/nginx/sites-available/ does not exist."


def config_nginx():
    """Configures nginx."""
    run_command_on_selected_server(_config_nginx)


def _restart_nginx():
    sudo('nginx -s reload')


def restart_nginx():
    """choose an instance and upload app to server"""
    run_command_on_selected_server(_restart_nginx)


def get_ec2_connection():
    """get an ec2 connection"""
    if 'ec2' not in env:
        conn = boto.ec2.connect_to_region(env.aws_region)
        if conn is not None:
            env.ec2 = conn
            print "Connected to EC2 region %s" % env.aws_region
        else:
            msg = "Unable to connect to EC2 region %s"
            raise IOError(msg % env.aws_region)
    return env.ec2


def list_aws_instances(verbose=False, state='all'):
    """list instances (-v), optionally filtering for a particular state."""
    conn = get_ec2_connection()

    reservations = conn.get_all_reservations()
    instances = []
    for res in reservations:
        for instance in res.instances:
            if state == 'all' or instance.state == state:
                instance = {
                    'id': instance.id,
                    'type': instance.instance_type,
                    'image': instance.image_id,
                    'state': instance.state,
                    'instance': instance,
                }
                instances.append(instance)
    env.instances = instances
    if verbose:
        import pprint
        pprint.pprint(env.instances)


def stop_instance():
    """terminate an instance"""
    select_instance()
    env.active_instance.stop()


def terminate_instance():
    select_instance(state='all')
    env.active_instance.terminate()


def select_instance(state='running'):
    """give an interactive choice of running instances"""
    if env.get('active_instance', False):
        return

    list_aws_instances(state=state)

    prompt_text = "Please select from the following instances:\n"
    instance_template = " %(ct)d: %(state)s instance %(id)s\n"
    for idx, instance in enumerate(env.instances):
        ct = idx + 1
        args = {'ct': ct}
        args.update(instance)
        prompt_text += instance_template % args
    prompt_text += "Choose an instance: "

    def validation(input):
        choice = int(input)
        if not choice in range(1, len(env.instances) + 1):
            raise ValueError("%d is not a valid instance" % choice)
        return choice

    choice = prompt(prompt_text, validate=validation)
    env.active_instance = env.instances[choice - 1]['instance']
    print env.active_instance


def run_command_on_selected_server(command, host_=None):
    """run a given command (passed by name as an argument) on the server we select"""
    print host_
    if not host_:
        select_instance()
        selected_hosts = [
            'ubuntu@' + env.active_instance.public_dns_name
        ]
    else:
        selected_hosts = [
            'ubuntu@' + str(env.myhost)
        ]
    execute(command, hosts=selected_hosts)


def _install_gunicorn():
    sudo('pip install gunicorn')
    sudo('gunicorn ')


def install_gunicorn():
    run_command_on_selected_server(_install_gunicorn)


def _install_nginx():
    sudo('apt-get update')
    sudo('apt-get install nginx')
    sudo('/etc/init.d/nginx start')


def install_nginx():
    run_command_on_selected_server(_install_nginx)


def provision_instance(wait_for_running=False, timeout=60, interval=2):
    """provision a new instance and set it running"""
    wait_val = int(interval)
    timeout_val = int(timeout)
    conn = get_ec2_connection()
    instance_type = 't1.micro'
    key_name = 'pk-ins'
    security_group = 'package_install'
    image_id = 'ami-d0d8b8e0'

    reservations = conn.run_instances(
        image_id,
        key_name=key_name,
        instance_type=instance_type,
        security_groups=[security_group, ]
    )
    new_instances = [i for i in reservations.instances if i.state == u'pending']
    running_instance = []
    if wait_for_running:
        waited = 0
        while new_instances and (waited < timeout_val):
            time.sleep(wait_val)
            waited += int(wait_val)
            for instance in new_instances:
                state = instance.state
                print "Instance %s is %s" % (instance.id, state)
                if state == "running":
                    running_instance.append(
                        new_instances.pop(new_instances.index(i))
                    )
                instance.update()