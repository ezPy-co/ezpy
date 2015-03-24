from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, DeleteView
from installer_config.models import EnvironmentProfile
from installer_config.forms import EnvironmentForm


class CreateEnvironmentProfile(CreateView):
    model = EnvironmentProfile
    template_name = 'env_profile_form.html'
    form_class = EnvironmentForm
    success_url = '/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreateEnvironmentProfile, self).form_valid(form)


class UpdateEnvironmentProfile(UpdateView):
    model = EnvironmentProfile
    template_name = 'env_profile_form.html'
    form_class = EnvironmentForm
    success_url = '/'


class DeleteEnvironmentProfile(DeleteView):
    model = EnvironmentProfile
    success_url = '/'
