from django.conf.urls import patterns, url
from installer_config.views import (CreateEnvironmentProfile,
                                    UpdateEnvironmentProfile,
                                    DeleteEnvironmentProfile,
                                    download_profile_view)

urlpatterns = patterns(
    '',

    url(r'^create_env/$',
        CreateEnvironmentProfile.as_view(),
        name='CreateEnv'),

    url(r'^update_env/(?P<pk>\d+)/$',
        UpdateEnvironmentProfile.as_view(),
        name='UpdateEnv'),

    url(r'^delete_env/(?P<pk>\d+)/$',
        DeleteEnvironmentProfile.as_view(),
        name='DeleteEnv'),

    url(r'^download/(?P<pk>\d+)/$',
        download_profile_view,
        name='download_profile')
)
