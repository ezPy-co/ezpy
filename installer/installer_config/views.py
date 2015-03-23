from django.shortcuts import render
from django.views.generic import CreateView
from installer_config.models import EnvironmentProfile
from installer_config.forms import CreateEnvironmentForm


class CreateEnvironmentProfile(CreateView):
    model = EnvironmentProfile
    template_name = 'create_env_profile.html'
    form_class = CreateEnvironmentForm
    success_url= '/'


    def form_valid(self, form):
        # import pdb; pdb.set_trace()
        form.instance.user = self.request.user
        return super(CreateEnvironmentProfile, self).form_valid(form)

