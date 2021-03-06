from django import forms
from django.forms.models import ModelForm, ModelMultipleChoiceField
from django.utils.html import format_html
from installer_config.models import EnvironmentProfile, UserChoice


class CustomMultipleChoiceField(ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return format_html(u'<b>{}</b><br /><small class="indent">{}</small>',
                           obj.name,
                           obj.description
                           )


class EnvironmentForm(ModelForm):
    choices = CustomMultipleChoiceField(widget=forms.CheckboxSelectMultiple(),
        queryset=UserChoice.objects.all().order_by('category', 'priority',
        ),
        error_messages={'required': 'Choose options below.'}
    )

    class Meta:
        model = EnvironmentProfile
        exclude = ('user', 'steps', )
