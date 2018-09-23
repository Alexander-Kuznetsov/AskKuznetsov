from django.contrib import admin
from django.conf.urls import url, include
import views
#from views import index_view
  
'''
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
]'''

urlpatterns = [
    url(r'^$', views.index_view, name='index'),
    url(r'^index', views.index_view, name='index'),
    #rl(r'^tag/kuznetsov/', 'ask_buevich.views.tag_john_view', name='tag_john'),
    url(r'^question(?P<article_id>\d+)/', views.answer_view, name='answer'),
    url(r'^login', views.login_view, name='login'),
    url(r'^signup', views.signup_view, name='signup'),
    url(r'^logout/', views.logout_view, name='logout'),
    url(r'^hot/', views.index_view, name='hot'),
    url(r'^ask', views.ask_view, name='ask'),
    url(r'^settings', views.settings_view, name='settings'),
    url(r'^hot_index', views.hot_index_view, name='hot_index'),
    url(r'^admin/', admin.site.urls),
]
