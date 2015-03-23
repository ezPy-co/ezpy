from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'installer.views.index', name='index'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^profile/', include('installer_profile.urls', namespace='profile')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('installer_config.urls', namespace='installer_config'))
)
