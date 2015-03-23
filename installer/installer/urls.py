from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$', 'installer.views.index', name='index'),
    url(r'^profile/', include('installer_profile.urls', namespace='profile')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^', include('installer_config.urls', namespace='installer_config'))
)
