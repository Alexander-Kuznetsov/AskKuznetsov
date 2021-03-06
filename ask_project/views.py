from django.contrib.auth.models import User
from django.shortcuts import render_to_response, redirect, render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import get_object_or_404
from django.contrib import auth
from django.contrib.auth.decorators import login_required
import simplejson as json
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.contenttypes.models import ContentType
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.template import RequestContext

from . import forms
from ask_project.models import *

from django.db.models import Count, Sum, F



def index_view(request, *args, **kwargs):
    articles = Question.objects.all()
    kwargs['tags'] = Tag.objects.get_count_iniq()
    kwargs['top_people'] = LikeDislike.objects.get_top_people()
    kwargs['author'] = Profile.objects
    return pagination(request, 'index.html', articles, 'articles', 10, *args, **kwargs)


def tags_view(request, *args, **kwargs):
    print(request.GET)
    return redirect('/')

def hot_index_view(request, *args, **kwargs):
    articles = Question.objects.hot_questions()
    kwargs['tags'] = Tag.objects.get_count_iniq()
    kwargs['top_people'] = LikeDislike.objects.get_top_people()
    return pagination(request, 'hot_index.html', articles, 'articles', 10, *args, **kwargs)


def search_view(request, *args, **kwargs):
    if request.method == 'GET':
        form = forms.SearchForm(request.GET)
        if form.is_valid():
            word = form.cleaned_data['search_word']
            print(word)
            articles = Question.objects.search_word(word)
            print(articles)
            if articles:
                kwargs['search_word'] = {'word': word, 'count': articles.count()}
                kwargs['tags'] = Tag.objects.get_count_iniq()
                kwargs['top_people'] = LikeDislike.objects.get_top_people()

                return pagination(request, 'search.html', articles, 'articles', 10, *args, **kwargs)
    #else:
    #    form = forms.SearchForm()

    return redirect('/')


def answer_view(request, article_id, *args, **kwargs):
    kwargs['tags'] = Tag.objects.get_count_iniq()
    kwargs['top_people'] = LikeDislike.objects.get_top_people()
    article = Question.objects.get(id=article_id)
    if request.POST:
        form = forms.AnswerAddForm(request.user, request.POST)
        user = Profile.objects.get(id=request.user.id)
        if form.is_valid():
            return redirect(form.save(article, user).get_url())
    else:
        form = forms.AnswerAddForm()
    answers = article.answer_set.all()
    return pagination(request, 'answer.html', answers, 'answers', 5, article=article, is_preview=False, form=form, *args, **kwargs)


def logout_view(request, *args, **kwargs):
    auth.logout(request)
    return redirect('/')


def login_view_render(request, *args, **kwargs):
    return render(request,'login.html', kwargs)


def login_view(request, *args, **kwargs):
    if request.user.is_authenticated():
        return redirect('/')

    kwargs['tags'] = Tag.objects.get_count_iniq()
    kwargs['top_people'] = LikeDislike.objects.get_top_people()
    if request.POST:
        form = forms.SignInForm(request.POST)
        if form.is_valid():
            user = form.auth()
            auth.login(request, user)
            #auth.authenticate(request, username=request.POST['username'], password=request.POST['username'])
            if user is not None:
                print('redirect')
                return redirect('/')
            print('sadasdadsaad')
            #    auth.login(request, user)
            #

            #auth.login(request, form.auth())
            #return redirect('/')

    else:
        form = forms.SignInForm()
    return login_view_render(request, form=form, *args, **kwargs)


def signup_view_render(request, *args, **kwargs):
    return render(request, 'signup.html', kwargs)


def signup_view(request, *args, **kwargs):
    if request.user.is_authenticated():
        return redirect('/')

    kwargs['tags'] = Tag.objects.get_count_iniq()
    kwargs['top_people'] = LikeDislike.objects.get_top_people()
    if request.POST:
        form = forms.RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            return redirect('/login/')
    else:
        form = forms.RegistrationForm()
    return signup_view_render(request, form=form, *args, **kwargs)


def ask_view_render(request, *args, **kwargs):
    return render(request, 'ask.html', kwargs)


@login_required
def ask_view(request, *args, **kwargs):
    kwargs['tags'] = Tag.objects.get_count_iniq()
    kwargs['top_people'] = LikeDislike.objects.get_top_people()
    if request.POST:
        form = forms.ArticleAddForm(request.user, request.POST)
        user = Profile.objects.get(id=request.user.id)
        if form.is_valid():
            return redirect(form.save(user).get_url())
    else:
        form = forms.ArticleAddForm()
    return ask_view_render(request, form=form, *args, **kwargs)

def settings_view_render(request, *args, **kwargs):
    return render(request, 'settings.html', kwargs)

@login_required
def settings_view(request, *args, **kwargs):
    kwargs['tags'] = Tag.objects.get_count_iniq()
    kwargs['top_people'] = LikeDislike.objects.get_top_people()

    if request.POST:
        form = forms.SettingsForm(request.user, request.POST)
        if form.is_valid():
            users = Profile.objects.get(id=request.user.id)
            #users.user.password = request.POST.get("password")
            #users.user.email = request.POST.get("email")
            #users.user.username = request.POST.get("login")
            #users.user.save()
            form.save(users.user)
            return redirect('/')
    else:
        form = forms.SettingsForm()
    return settings_view_render(request, form=form, *args, **kwargs)


def pagination(request, html_page, objects, object_name, objects_count, *args, **kwargs):
    paginator = Paginator(objects, objects_count)
    page = request.GET.get('page')

    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)

    kwargs[object_name] = objects
    kwargs['pagination_list'] = objects
    #print(kwargs)

    return render(request, html_page, kwargs)


class VotesView(View):
    model = None
    vote_type = None

    def post(self, request, pk):
        obj = self.model.objects.get(pk=pk)

        try:
            likedislike = LikeDislike.objects.get(content_type=ContentType.objects.get_for_model(obj), object_id=obj.id,
                                                  user=request.user)
            if likedislike.vote is not self.vote_type:
                likedislike.vote = self.vote_type
                likedislike.save(update_fields=['vote'])
                result = True
            else:
                likedislike.delete()
                result = False
        except LikeDislike.DoesNotExist:
            obj.votes.create(user=request.user, vote=self.vote_type)
            result = True

        return HttpResponse(
            json.dumps({
                "result": result,
                "like_count": obj.votes.likes().count(),
                "dislike_count": obj.votes.dislikes().count(),
                "sum_rating": obj.votes.sum_rating()
            }),
            content_type="application/json"
        )


def e_handler404(request):
    #context = RequestContext(request)
    response = render_to_response('error404.html')
    response.status_code = 404
    return response


def e_handler500(request):
    #context = RequestContext(request)
    response = render_to_response('error500.html')
    response.status_code = 500
    return response
'''
def pagination(request, objects, object_name, objects_count, *args, **kwargs):
    paginator = Paginator(objects, objects_count)
    page = request.GET.get('page')

    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)

    kwargs[object_name] = objects
    kwargs['pagination_list'] = objects

    return request, kwargs
'''


'''
@login_required()
def like(request):
    body = request.body.decode("utf-8")
    request.POST = json.loads(body)
    if request.POST['type'] == 'que':
        q = Question.objects.get(id=request.POST['qid'])
        p = Profile.objects.get(user_id=request.user.id)
        value = 1 if request.POST['type_like'] == 'like_question' else -1
        LikesQuestion.objects.add_or_update(owner=p, question=q, value=value)
        return HttpResponse(
            json.dumps({"qid": request.POST['qid'], 'like': value}),
            content_type="application/json"
        )
'''
'''
    else:
        if request.POST['type'] == 'ans':
            a = Answer.objects.get(id=request.POST['aid'])
            p = Profile.objects.get(user_id=request.user.id)
            value = 1 if request.POST['type_like'] == 'like_answer' else -1
            LikeToAnswer.objects.add_or_update(owner=p, answer=a, value=value)
            return HttpResponse(
                json.dumps({"aid": request.POST['aid'], 'like': value}),
                content_type="application/json"
            )
'''
