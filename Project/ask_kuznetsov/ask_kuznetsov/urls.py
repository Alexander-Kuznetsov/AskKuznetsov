from django.contrib import admin
from django.conf.urls import url, include
from views import *
from views import index_view
  
urlpatterns = [
    url(r'question/', include('questions.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^$', index_view, name='index'),
    url(r'^index', index_view, name='index'),
    url(r'^signup', signup_view, name='singup'),
    url(r'^ask', ask_view, name='ask'),
    url(r'^answer', answer_view, name='answer'),
    url(r'^login', login_view, name='login'),
    url(r'^settings', settings_view, name='settings'),
    url(r'^tag', tag_view, name='tag')
]
