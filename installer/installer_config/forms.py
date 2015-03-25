from django import forms
from django.forms.models import ModelForm
from installer_config.models import EnvironmentProfile, UserChoice


class EnvironmentForm(ModelForm):
    choices = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(),
        queryset=UserChoice.objects.all().order_by('display_order'),
        help_text="Check all wanted options.")

    class Meta:
        model = EnvironmentProfile
        exclude = ('user', 'steps', )
