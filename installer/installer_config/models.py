from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class UserChoice(models.Model):
    PRIORITY = (
        (1, 'High'),
        (2, 'Normal'),
        (3, 'Low'),
    )

    DISPLAY_CATEGORY = (
        ('core', 'Core Dependencies'),
        ('env', 'Virtual Environment'),
        ('git', 'Git'),
        ('prompt', 'Terminal Prompt'),
        ('subl', 'Sublime'),
        ('pkg', 'Pip Packages'),
        ('other', 'Other'),
    )

    name = models.CharField(max_length=63)
    description = models.CharField(max_length=255, blank=True)
    category = models.CharField(max_length=7, choices=DISPLAY_CATEGORY)
    priority = models.IntegerField(choices=PRIORITY)

    def __str__(self):
        return str(self.name)

    class Meta:
        ordering = ['category']


@python_2_unicode_compatible
class Step(models.Model):
    STEP_TYPE_CHOICES = (
        ('dl', 'Download'),
        ('pip', 'Install with Pip'),
        ('edprof', 'Edit a profile'),
        ('edfile', 'Edit a file'),
        ('env', 'Set environment variable'),
        ('exec', 'Run a shell command'),
    )

    step_type = models.CharField(max_length=63, choices=STEP_TYPE_CHOICES)
    url = models.CharField(max_length=63, blank=True, null=True)
    args = models.CharField(max_length=255, blank=True, null=True)
    dependency = models.CharField(max_length=63, blank=True, null=True)
    user_choice = models.ForeignKey(UserChoice, related_name='step')

    def __str__(self):
        return str(self.step_type) + " " + str(self.args)


@python_2_unicode_compatible
class EnvironmentProfile(models.Model):
    """Unique environment profile created by a user"""
    user = models.ForeignKey(User, related_name='profile')
    description = models.CharField(max_length=63)
    choices = models.ManyToManyField(UserChoice,
                                     related_name='profiles',
                                     blank=True,
                                     null=True)
    
    def __str__(self):
        return str(self.description)
