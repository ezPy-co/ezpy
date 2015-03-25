#!usr/bin/env python
from subprocess import call
import urllib2
import os

{% for choice in choices %}

# For a straight pip install with no setup
    {% for step in choice.step.all %}

    {% if step.step_type == 'dl' %}
        response = urllib2.urlopen({{step.url}})
        file_name = os.path.basename({{step.url}})
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
        f.write("\n"+{{step.args}})


    print 'profile change\n'
    {% endif %}

    {% if step.step_type == 'edfile' %}
    # call(['pip', 'install', option.package_name])
    print 'file change\n'
    {% endif %}

    {% if step.step_type == 'env' %}
    print 'set a thing\n'
    {% endif %}

    {% if step.step_type == 'pip' %}
    print 'pip\n'
    {% endif %}

    {% if step.step_type == 'exec' %}
    print {{step.args}}
    {% endif %}

    {% endfor %}

{% endfor %}