from django.shortcuts import render
from django.shortcuts import render_to_response
from django.views.generic import CreateView, UpdateView, DeleteView
from installer_config.models import EnvironmentProfile, UserChoice, Step
from installer_config.forms import EnvironmentForm
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

class CreateEnvironmentProfile(CreateView):
    model = EnvironmentProfile
    template_name = 'env_profile_form.html'
    form_class = EnvironmentForm
    success_url = '/profile'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreateEnvironmentProfile, self).form_valid(form)


    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = form_class(request.POST)
        if form.is_valid():
            config_profile = form.save(commit=False)
            config_profile.user = request.user
            config_profile.save()
            return HttpResponseRedirect(reverse('profile:profile'))
        return self.render_to_response({'form': form})

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
    return render_to_response('installer_template.py', {'choices': choices}, content_type='application')
