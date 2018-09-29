from django.contrib import admin
from django.conf.urls import url, include
import views
from django.contrib.auth.decorators import login_required
from .models import Question, Answer
from .models import LikeDislike
#from views import index_view
from django.views.generic import TemplateView

'''url(r'^question(\d+)/article/(?P<pk>\d+)/like/$',
        login_required(views.VotesView.as_view(model=Question, vote_type=LikeDislike.LIKE)),
        name='article_like'),
    url(r'^question(\d+)/article/(?P<pk>\d+)/dislike/$',
        login_required(views.VotesView.as_view(model=Question, vote_type=LikeDislike.DISLIKE)),
        name='article_dislike'),
'''

urlpatterns = [
    url(r'^article/(?P<pk>\d+)/like/$',
        login_required(views.VotesView.as_view(model=Question, vote_type=LikeDislike.LIKE)),
        name='article_like'),
    url(r'^article/(?P<pk>\d+)/dislike/$',
        login_required(views.VotesView.as_view(model=Question, vote_type=LikeDislike.DISLIKE)),
        name='article_dislike'),


    url(r'^question(\d+)/answer/(?P<pk>\d+)/like/$',
        login_required(views.VotesView.as_view(model=Answer, vote_type=LikeDislike.LIKE)),
        name='answer_like'),
    url(r'^question(\d+)/answer/(?P<pk>\d+)/dislike/$',
        login_required(views.VotesView.as_view(model=Answer, vote_type=LikeDislike.DISLIKE)),
        name='answer_dislike'),
    url(r'^$', views.index_view, name='index'),
    url(r'^index', views.index_view, name='index'),
    url(r'^question(?P<article_id>\d+)/', views.answer_view, name='answer'),
    url(r'^login', views.login_view, name='login'),
    url(r'^signup', views.signup_view, name='signup'),
    url(r'^logout/', views.logout_view, name='logout'),
    url(r'^hot/', views.index_view, name='hot'),
    url(r'^ask', views.ask_view, name='ask'),
    url(r'^settings', views.settings_view, name='settings'),
    url(r'^hot_index', views.hot_index_view, name='hot_index'),
    url(r'^search/$', views.search_view, name='search'),
    url(r'^tags/$', views.tags_view, name='tags'),
    url(r'^admin/', admin.site.urls),
]

handler404 = views.e_handler404
handler500 = views.e_handler500