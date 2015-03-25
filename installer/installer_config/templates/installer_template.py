#!usr/bin/env python
from subprocess import call
import urllib2
import os
import sys

def scan(file_name):
    """
    Return the full file path to a file, including file_name.

    If the file is not found, print 'File not found' to the console
    and return None.
    """
    if 'Windows' in os.environ.get('OS'):
        # Assumes the drive letter is C
        walker = os.walk('C:/')
    else:
        walker = os.walk('/')
    for directory, sub_dir, files in walker:
        if file_name in files:
            return directory + file_name
    else:
        # If the whole directory has been scanned with
        # no result...
        print 'File not found'
        return None

{% for choice in choices %}
{% spaceless %}
# For a straight pip install with no setup
{% for step in choice.step.all %}
{% spaceless %}
{% if step.step_type == 'dl' %}
# Download and run {{step}}
response = urllib2.urlopen('{{step.url}}')
file_name = os.path.basename('{{step.url}}')
with open(file_name, 'w') as f:
    f.write(response.read())
if os.path.splitext(file_name)[1] == '.py':
    call(['python', file_name])
else:
    run_file = './'+file_name
    call([run_file])
{% endif %}

{% if step.step_type == 'edprof' %}
profile_name = os.path.expanduser('~/')+'.profile'
with open(profile_name, 'a') as f:
    f.write("\n"+"{{step.args}}")


print 'profile change\n'
{% endif %}

{% if step.step_type == 'edfile' %}
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
call(['pip', 'install', "{{step.args}}"])
{% endif %}

{% if step.step_type == 'exec' %}
command_line = "{{step.args}}".split(',')
call(command_line)
{% endif %}
{% endspaceless %}
{% endfor %}

{% endspaceless %}
{% endfor %}