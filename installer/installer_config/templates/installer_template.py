#!usr/bin/env python
from subprocess import call

{% for option in environmental_profile %}

# For a straight pip install with no setup
    {% for step in option %}

    # Download file
    {% if step.type == 'download' %}
        print 'download'
    {% endif %}

    # Pre execution setup
    {% if step.type == 'preset' %}
        print 'preset'
    {% endif %}

    # Execute file
    {% if step.type == 'pip' %}
        # call(['pip', 'install', option.package_name])
        print 'pip'
    {% endif %}
    {% if step.type == 'execute': %}
        # Need to know download file name and type...
        print 'execute'
    {% endif %}

    # Post execution setup
    {% if step.type == 'postset' %}
        print 'postset '
    {% endif %}

    {% endfor %}

{% endfor %}