from django.shortcuts import render
from django.views.generic import CreateView
from installer_config.models import EnvironmentProfile
from installer_config.forms import CreateEnvironmentForm


class CreateEnvironmentProfile(CreateView):
    model = EnvironmentProfile
    template_name = 'create_env_profile.html'
    form_class = CreateEnvironmentForm