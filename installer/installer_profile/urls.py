from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
                       url('^$', 'installer_profile.views.profile',
                           name='profile')
)
