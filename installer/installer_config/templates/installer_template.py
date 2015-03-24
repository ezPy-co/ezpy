#!usr/bin/env python
from subprocess import call

{% for choice in choices %}

# For a straight pip install with no setup
    {% for step in choice.step.all %}

    # Download file
    {% if step.step_type == 'dl' %}
    print step + "\n"
    print 'download\n'
    {% endif %}

    # Pre execution setup
    {% if step.step_type == 'edprof' %}
    print 'profile change\n'
    {% endif %}

    # Execute file
    {% if step.step_type == 'edfile' %}
    # call(['pip', 'install', option.package_name])
    print 'file change\n'
    {% endif %}
    {% if step.step_type == 'env' %}
    # Need to know download file name and type...
    print 'set a thing\n'
    {% endif %}

    # Post execution setup
    {% if step.step_type == 'pip' %}
    print 'pip\n'
    {% endif %}

    {% endfor %}

{% endfor %}