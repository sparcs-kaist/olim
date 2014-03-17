from django.conf.urls import patterns, include, url
from django.http import *
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', include('olim.apps.storage.urls')),
    url(r'^account/', include('olim.apps.account.urls')),

    # Media path
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root':settings.MEDIA_ROOT}),

    # Admin Page
    url(r'^admin/', include(admin.site.urls)),
)
