from django.conf.urls import patterns, include, url
from django.contrib import admin
from installer_config.views import CreateEnvironmentProfile

urlpatterns = patterns('',
    url(r'create_env/', CreateEnvironmentProfile.as_view(), name='CreateEnv')
)
