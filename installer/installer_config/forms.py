from django import forms
from django.forms.models import ModelForm
from installer_config.models import EnvironmentProfile, UserChoice
 

class EnvironmentForm(ModelForm):
    packages = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                              queryset=UserChoice.objects.all())

    class Meta:
        model = EnvironmentProfile
        exclude = ('user',)
