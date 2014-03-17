from django.conf.urls import patterns, include, url
from olim.apps.storage import views

urlpatterns = patterns('',
    url(r'^$', views.listing),
)
