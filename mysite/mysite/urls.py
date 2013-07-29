# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from sample_board import views
from django.conf import settings


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^mysite/', include('mysite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.home), # 여기에서 home 컨트롤러를 호출하게 맵핑해준다.
    url(r'^show_write_form/$', views.show_write_form),
    url(r'^DoWriteBoard/$', views.DoWriteBoard),
    url(r'^listSpecificPageWork/$', views.listSpecificPageWork),
    url(r'^viewWork/$', views.viewWork),
    url(r'^listSearchedSpecificPageWork/$', views.listSearchedSpecificPageWork),
    url(r'^listSpecificPageWork_to_update/$', views.listSpecificPageWork_to_update),
    url(r'^updateBoard/$', views.updateBoard),
    url(r'^DeleteSpecificRow/$', views.DeleteSpecificRow),
    url(r'^searchWithSubject/$', views.searchWithSubject),
   # url(r'^', + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)),
    url(r'^upload/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^rowmodify/$', views.rowmodify),
)