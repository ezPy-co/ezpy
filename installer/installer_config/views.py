from django.shortcuts import render
from django.shortcuts import render_to_response
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from installer_config.models import EnvironmentProfile, UserChoice, Step
from installer_config.forms import EnvironmentForm
from django.core.urlresolvers import reverse


class CreateEnvironmentProfile(CreateView):
    model = EnvironmentProfile
    context_object_name = 'profile'
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

    def get_queryset(self):
        qs = super(UpdateEnvironmentProfile, self).get_queryset()
        return qs.filter(user=self.request.user)


class DeleteEnvironmentProfile(DeleteView):
    model = EnvironmentProfile
    success_url = '/profile'


class ViewEnvironmentProfile(DetailView):
    model = EnvironmentProfile
    context_object_name = 'profile'
    template_name = 'env_profile.html'

    def get_context_data(self, **kwargs):
        context = super(ViewEnvironmentProfile, self).get_context_data()
        categories = ['core', 'env', 'git', 'prompt', 'subl', 'pkg', 'other']

        # all = context.profile.choices.all
        for categ in categories:
            count = context['profile'].choices.filter(category=categ).count()
            print categ + "  " + str(count)
            if count:
                context[categ] = True
            else:
                context[categ] = False
        return context

    # def get_context_data(self):
    #     context = super(ViewEnvironmentProfile, self).get_context_data()
    #     categorized = {}
    #     for choice in self.object.choices.all():
    #         categorized.setdefault(choice.category, []).append(choice)
    #     context.update({'categorized_choices': categorized})
    #     return context


def download_profile_view(request, **kwargs):
    environment = EnvironmentProfile.objects.get(pk=kwargs['pk'])
    choices = UserChoice.objects.filter(profiles=environment)

    response = render_to_response('installer_template.py', {'choices': choices},
                                  content_type='application')
    response['Content-Disposition'] = 'attachment; filename=ezpy__{env_name}.py'.format(
        env_name=environment.description.replace(' ', '_'), user=environment.user.username)
    return response
