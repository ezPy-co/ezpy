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
    else:
        # If the whole directory has been scanned with
        # no result...
        print 'File or directory not found'
        return None

{% for choice in choices %}
{% spaceless %}
# For choice {{choice.name}}
{% for step in choice.step.all %}
{% spaceless %}
{% if step.step_type == 'dl' %}
# Download and run {{step}}
print "Downloading from {{step.url}}"
response = urllib2.urlopen('{{step.url}}')
file_name = os.path.basename('{{step.url}}')
with open(file_name, 'w') as f:
    f.write(response.read())
if os.path.splitext(file_name)[1] == '.py':
    call(['python', file_name])
else:
{% if choice.category == 'git' %}
# Unpack git for execution
{% endif %}
    run_file = './'+file_name
    print "Running file_name"
    call([run_file])
{% endif %}

{% if step.step_type == 'edprof' %}
# Edit a profile
profile_name = os.path.expanduser('~/')+'.profile'
with open(profile_name, 'a') as f:
    f.write("\n"+"{{step.args}}")
print "Added '{{step.args}}' to file at profile_name"
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
call(['pip', 'install', "{{step.args}}"])
{% endif %}

{% if step.step_type == 'exec' %}
command_line = "{{step.args}}".split(',')
print "Executing " + ' '.join(command_line)
call(command_line)
{% endif %}
{% endspaceless %}
{% endfor %}

{% endspaceless %}
{% endfor %}