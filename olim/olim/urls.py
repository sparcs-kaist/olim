from django.conf.urls import patterns, include, url
from django.http import HttpResponseRedirect
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', lambda request: HttpResponseRedirect('/root')),
    url(r'^root', 'olim.apps.storage.views.index'),
    url(r'^account/', include('olim.apps.account.urls')),
    url(r'^login/$', 'olim.apps.account.views.login_user'),
    url(r'^logout/$', 'olim.apps.account.views.logout_user'),

    # Auth path
    url(r'^nlogin/$', 'olim.apps.account.views.need_login'),

    # Filesys path
    url(r'^filesys/getdata/$', 'olim.apps.storage.views.get_url_data'),
    url(r'^files/', 'olim.apps.storage.views.get_file_data'),

    # Media path
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root':settings.MEDIA_ROOT}),

    # Admin Page
    url(r'^admin/', include(admin.site.urls)),
)
