from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, DeleteView
from installer_config.models import EnvironmentProfile, UserChoice, Step
from installer_config.forms import EnvironmentForm


class CreateEnvironmentProfile(CreateView):
    model = EnvironmentProfile
    template_name = 'env_profile_form.html'
    form_class = EnvironmentForm
    success_url = '/profile'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreateEnvironmentProfile, self).form_valid(form)


class UpdateEnvironmentProfile(UpdateView):
    model = EnvironmentProfile
    context_object_name = 'profile'
    template_name = 'env_profile_form.html'
    form_class = EnvironmentForm
    success_url = '/profile'


class DeleteEnvironmentProfile(DeleteView):
    model = EnvironmentProfile
    success_url = '/profile'


def download_profile_view(request, **kwargs):
    choices = UserChoice.objects.filter(profiles=kwargs['pk']).all()
    return render(request, 'installer_template.py', {'choices': choices})
