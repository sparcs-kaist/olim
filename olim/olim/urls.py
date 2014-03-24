from django.conf.urls import patterns, include, url
from django.http import *
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', lambda request: HttpResponseRedirect('/root')),
    url(r'^root/', 'olim.apps.storage.views.directory_index'),
    url(r'^files/', 'olim.apps.storage.views.file_index'),
    url(r'^account/', include('olim.apps.account.urls')),
    url(r'^login/', 'olim.apps.account.views.login_user'),
    url(r'^login/?next=(?P<next>)', 'olim.apps.account.views.login_user'),
    url(r'^logout/', 'olim.apps.account.views.logout_user'),
    url(r'^logout/?next=(?P<next>)', 'olim.apps.account.views.logout_user'),
    url(r'^filesys/getlist/$', 'olim.apps.storage.views.get_list_filesys'),

    # Media path
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root':settings.MEDIA_ROOT}),

    # Admin Page
    url(r'^admin/', include(admin.site.urls)),
)
