#!usr/bin/env python
from subprocess import call
import urllib2
import os
import sys

def scan(a_name):
    """
    Return the full file path to a file, including file_name.

    If the file is not found, print 'File or directory not found'
    to the console and return None.
    """
    extension = os.splitext(a_name)[1]
    if 'Windows' in os.environ.get('OS'):
        # Assumes the drive letter is C
        walker = os.walk('C:/')
    else:
        walker = os.walk('/')
        if extension:
            # Search for a file
            for directory, sub_dir, files in walker:
                if a_name in files:
                    return directory + a_name
        else:
            # Search for a directory
            for directory, sub_dir, files in walker:
                if a_name in directory:
                    return directory
    # If the whole directory has been scanned with
    # no result...
    print 'File or directory not found'
    return None

def execute(command_line):
    command_line = command_line
    if 'win' not in sys.platform:
        command_line.insert(0, 'sudo')
    call(command_line)

{% for choice in choices %}
{% spaceless %}
# For choice {{choice.name}}
{% for step in choice.step.all %}
{% spaceless %}

{% if step.step_type == 'dl' %}

# Download and run {{step}}
url = '{{step.url}}'
not_linux = True
{% if choice.category != 'git' %}
# Detect OS and change url accordingly...
if 'win' in sys.platform:
    # The url for git will be the url used for the windows exe
    print 'Windows detected'
elif 'darwin' in sys.platform:
    print 'Mac detected'
    url = None
elif 'linux' in sys.platform:
    print 'Linux detected'
    not_linux = False
else:
    print 'WARNING: Failed to determine OS'
{% endif %}

if not_linux and url:
    print "Downloading from {}".format(url)
    response = urllib2.urlopen(url)
    file_name = os.path.basename(url)

    with open(file_name, 'w') as f:
        f.write(response.read())

    if os.path.splitext(file_name)[1] == '.py':
        execute([sys.executable, file_name])
        raw_input('Enter anything to continue when finished installing git.')
    else:
        print "Running file_name"
        execute(['./'+file_name])
elif url is None:
    call(['sudo', 'xcode-select', '--install'])
    raw_input('Enter anything to continue when finished installing xcode and git.')
else:
    # This will prompt user for sudo password
    call(['sudo', 'apt-get', 'install', 'git'])
{% endif %}

{% if step.step_type == 'edprof' %}
# Edit a profile
profile_name = os.path.expanduser('~/')+'.profile'
print "Adding '{{step.args}}' to file at profile_name"
with open(profile_name, 'a') as f:
    # Assumes the .profile should be in the home directory
    f.write("\n"+"{{step.args|safe}}")
{% endif %}

{% if step.step_type == 'edfile' %}
# Edit a file, {{step.args}}
with open(step.file_location)
# call(['pip', 'install', option.package_name])
print 'file change\n'
{% endif %}

{% if step.step_type == 'env' %}
# Add a key, value pair for a subsequent call([])
key, val = "{{step.args}}".split(',')
os.putenv(key, val)
{% endif %}

{% if step.step_type == 'pip' %}
# Pip install, assuming the exact name of the package as used for 'pip install [package]'
# is given in the args field for a step
execute(['pip', 'install', "{{step.args}}"])
{% endif %}

{% if step.step_type == 'exec' %}
command_line = "{{step.args}}".split(',')
print "Executing " + ' '.join(command_line)
execute(command_line)
{% endif %}

{% endspaceless %}
{% endfor %}

{% endspaceless %}
{% endfor %}