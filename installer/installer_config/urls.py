from django.conf.urls import patterns, include, url
from installer_config.views import (CreateEnvironmentProfile,
                                    UpdateEnvironmentProfile)

urlpatterns = patterns('',
    url(r'^create_env/$', CreateEnvironmentProfile.as_view(), name='CreateEnv'),
    url(r'^update_env/(?P<pk>\d+)/$', UpdateEnvironmentProfile.as_view(), name='UpdateEnv'),
)
