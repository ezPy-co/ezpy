from django.shortcuts import render
from django.views.generic import CreateView
from installer_config.models import EnvironmentProfile


class CreateEnvironmentProfile(CreateView):
    model = EnvironmentProfile
    template_name = 'create_env_profile.html'
