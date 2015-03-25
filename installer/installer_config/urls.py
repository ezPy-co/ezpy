from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from installer_config.views import (CreateEnvironmentProfile,
                                    UpdateEnvironmentProfile,
                                    DeleteEnvironmentProfile,
                                    ViewEnvironmentProfile,
                                    download_profile_view)

urlpatterns = patterns(
    '',

    url(r'^create_env/$',
        login_required(CreateEnvironmentProfile.as_view()),
        name='CreateEnv'),

    url(r'^update_env/(?P<pk>\d+)/$',
        login_required(UpdateEnvironmentProfile.as_view()),
        name='UpdateEnv'),

    url(r'^delete_env/(?P<pk>\d+)/$',
        login_required(DeleteEnvironmentProfile.as_view()),
        name='DeleteEnv'),

    url(r'^download/(?P<pk>\d+)/$',
        download_profile_view,
        name='download_profile'),

    url(r'^env/(?P<pk>\d+)/$',
        login_required(ViewEnvironmentProfile.as_view()),
        name='ViewEnv'),
)
