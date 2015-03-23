from django.db import models
from django.contrib.auth.models import User


class Package(models.Model):
    """Python Package Manager for pip requirements.txt"""
    display_name = models.CharField(max_length=63)
    install_name = models.CharField(max_length=63)
    version = models.FloatField()
    website = models.URLField()
    description = models.TextField()

    class Meta:
        verbose_name = "pip package"


class TerminalPrompt(models.Model):
    """Terminal prompt customization"""
    display_name = models.CharField(max_length=63)
    install_name = models.TextField()
    description = models.TextField()


# class TerminalAddOns(models.Model):
    # """Add ons for terminal"""
    # Git completion
    # Virtual env
    # Virtual env wrapper

class EnvironmentProfile(models.Model):
    """Unique environment profile created by a user"""
    user = models.ForeignKey(User, related_name='profile')
    packages = models.ManyToManyField(Package,
                                      related_name='profiles',
                                      blank=True,
                                      null=True)
    prompt = models.ForeignKey(TerminalPrompt, related_name='profile')
