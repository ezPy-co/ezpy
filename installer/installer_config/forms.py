from django import forms
from django.forms.models import ModelForm
from installer_config.models import EnvironmentProfile, Package, TerminalPrompt
 

class EnvironmentForm(ModelForm):
    packages = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                              queryset=Package.objects.all())

    class Meta:
        model = EnvironmentProfile
        exclude = ('user',)
