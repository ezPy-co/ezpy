from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'/create_env', 'installer_config.views.create_env', name='create_env')
)
