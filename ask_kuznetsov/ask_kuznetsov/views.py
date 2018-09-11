from django.shortcuts import render_to_response, redirect, render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import get_object_or_404
from django.contrib import auth

from ask_kuznetsov.models import *

from django.contrib.auth.models import User

def index_view(request, *args, **kwargs):
    articles = Question.objects.all()
    return pagination(request, 'index.html', articles,'articles', 10, *args, **kwargs)

def signup_view(request, *args, **kwargs):
    return render_to_response('signup.html', kwargs)

def ask_view(request, *args, **kwargs):
    return render_to_response('ask.html', kwargs)

def answer_view(request, *args, **kwargs):
    return render_to_response('answer.html', kwargs)

def login_view(request, *args, **kwargs):
    return render_to_response('login.html', kwargs)

def settings_view(request, *args, **kwargs):
    return render_to_response('settings.html', kwargs)

def tag_view(request, *args, **kwargs):
    return render_to_response('tag.html', kwargs)

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

    return render(request,html_page, kwargs)

