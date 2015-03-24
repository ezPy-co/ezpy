#!usr/bin/env python
from subprocess import call

{% for choice in choices %}

# For a straight pip install with no setup
    {% for step in choice.step.all %}

    
    {% if step.step_type == 'dl' %}
    print {{step.url}}
    {% endif %}

    {% if step.step_type == 'edprof' %}
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