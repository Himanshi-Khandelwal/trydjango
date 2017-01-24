from django.conf.urls import url
from django.contrib import admin

from .views import (
	post_list,
	base,
	register_view,
	login_view,
	logout_view,
	post_create,
	post_detail,
	post_update,
	post_delete,
	)

urlpatterns = [
	url(r'^$', base , name='base'),
	url(r'^login/$', login_view, name='login'),
	url(r'^logout/$', logout_view, name='logout'),
	url(r'^register/$', register_view, name='register'),
	url(r'^post_list/$', post_list , name='list'),
    url(r'^create/$', post_create),
    url(r'^blog/(?P<id>\d+)/$', post_detail, name='detail'),
    url(r'^blog/(?P<id>\d+)/edit/$', post_update, name='update'),
    url(r'^blog/(?P<id>\d+)/delete/$', post_delete),
    #url(r'^posts/$', "<appname>.views.<function_name>"),
]
