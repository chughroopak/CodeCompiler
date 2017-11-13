from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from .views import *

urlpatterns = [
    url(r'^$', home),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'login'}, name='logout'),
    url(r'^htmlviewer$', codeplay),
    url(r'^userhome$', profile),
    url(r'^signup/$', signup, name='signup'),
    url(r'^base/$', base, name='base'),
    url(r'^compile/$', compileCode, name='compile'),
    # ex: /run/
    url(r'^run/$', runCode, name='run'),
    # ex: /code=ajSkHb/
    url(r'(?P<code_id>\w{0,50})/$', savedCodeView, name='saved-code'),
]
