from django.shortcuts import render
from django.shortcuts import render_to_response
from django.views.generic import CreateView, UpdateView, DeleteView
from installer_config.models import EnvironmentProfile, UserChoice, Step
from installer_config.forms import EnvironmentForm
from django.core.urlresolvers import reverse


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
    response = render_to_response('installer_template.py', {'choices': choices},
                                  content_type='application')
    response['Content-Disposition'] = 'attachment; filename=something.py'
    return response
