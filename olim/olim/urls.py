from django.conf.urls import patterns, include, url
from django.http import *
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', lambda request: HttpResponseRedirect('/root')),
    url(r'^root/', 'olim.apps.storage.views.filesys'),
    url(r'^account/', include('olim.apps.account.urls')),
    url(r'^login/', 'olim.apps.account.views.login_user'),
    url(r'^login/?next=(?P<next>)', 'olim.apps.account.views.login_user'),
    url(r'^logout/', 'olim.apps.account.views.logout_user'),
    url(r'^logout/?next=(?P<next>)', 'olim.apps.account.views.logout_user'),

    # Media path
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root':settings.MEDIA_ROOT}),

    # Admin Page
    url(r'^admin/', include(admin.site.urls)),
)
