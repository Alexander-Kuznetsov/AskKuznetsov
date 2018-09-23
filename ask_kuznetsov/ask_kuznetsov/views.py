from django.contrib.auth.models import User
from django.shortcuts import render_to_response, redirect, render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import get_object_or_404
from django.contrib import auth
from django.contrib.auth.decorators import login_required

from . import forms
from ask_kuznetsov.models import *


def index_view(request, *args, **kwargs):
    articles = Question.objects.all()
    return pagination(request, 'index.html', articles, 'articles', 10, *args, **kwargs)


def tag_john_view(request, *args, **kwargs):
    articles = []
    return pagination(request, 'tag.html', articles, 'articles', 10, *args, **kwargs)


def hot_index_view(request, *args, **kwargs):
    articles = Question.objects.best_questions()
    return pagination(request, 'hot_index.html', articles, 'articles', 10, *args, **kwargs)


def answer_view(request, article_id, *args, **kwargs):
    article = Question.objects.get(id=article_id)
    if request.POST:
        form = forms.AnswerAddForm(request.user, request.POST)
        if form.is_valid():
            return redirect(form.save(article).get_url())
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
    if request.POST:
        print('this post!')
        form = forms.SignInForm(request.POST)
        print('signin!')
        if form.is_valid():
            print('isvalid')
            auth.login(request, form.auth())
            return redirect('/')
    else:
        form = forms.SignInForm()
    return login_view_render(request, form=form, *args, **kwargs)


def signup_view_render(request, *args, **kwargs):
    return render(request, 'signup.html', kwargs)


def signup_view(request, *args, **kwargs):
    if request.POST:
        form = forms.RegistrationForm(request.POST)
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
    if request.POST:
        form = forms.ArticleAddForm(request.user, request.POST)
        if form.is_valid():
            return redirect(form.save().get_url())
    else:
        form = forms.ArticleAddForm()
    return ask_view_render(request, form=form, *args, **kwargs)


def settings_view(request, *args, **kwargs):
    return render(request, 'settings.html', kwargs)


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

    return render(request, html_page, kwargs)
