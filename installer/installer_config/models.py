from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible


# @python_2_unicode_compatible
# class Package(models.Model):
#     """Python Package Manager for pip requirements.txt"""
#     display_name = models.CharField(max_length=63)
#     install_name = models.CharField(max_length=63)
#     version = models.FloatField(null=True, blank=True)
#     website = models.URLField()
#     description = models.TextField()

#     class Meta:
#         verbose_name = "pip package"

#     def __str__(self):
#         return str(self.display_name)


# @python_2_unicode_compatible
# class TerminalPrompt(models.Model):
#     """Terminal prompt customization"""
#     display_name = models.CharField(max_length=63)
#     install_name = models.TextField()
#     description = models.TextField()

#     def __str__(self):
#         return str(self.display_name)


@python_2_unicode_compatible
class UserChoice(models.Model):
    description = models.CharField(max_length=63)


@python_2_unicode_compatible
class Step(models.Model):
    STEP_TYPE_CHOICES = (
        ('dl', 'Download'),
        ('pip', 'Install with Pip'),
        ('edprof', 'Edit a profile'),
        ('edfile', 'Edit a file'),
        ('env', 'Set environment variable'),
        ('exec', 'Run a shell command')
        )

    step_type = models.CharField(max_length=63, choices=STEP_TYPE_CHOICES)
    url = models.CharField(max_length=63, blank=True, null=True)
    args = models.CharField(max_length=63, blank=True, null=True)
    dependency = models.CharField(max_length=63, blank=True, null=True)
    user_choice = models.ForeignKey(UserChoice, related_name='step')


@python_2_unicode_compatible
class EnvironmentProfile(models.Model):
    """Unique environment profile created by a user"""
    user = models.ForeignKey(User, related_name='profile')
    description = models.CharField(max_length=63)
    choices = models.ManyToManyField(UserChoice,
                                     related_name='profiles',
                                     blank=True,
                                     null=True)
    # prompt = models.ForeignKey(TerminalPrompt, related_name='profile', blank=True, null=True)
    # git_completion = models.BooleanField(default=True)

    def __str__(self):
        return str(self.description)
