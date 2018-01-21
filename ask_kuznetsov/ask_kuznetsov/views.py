from django.shortcuts import render_to_response, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import get_object_or_404
from django.contrib import auth

from django.contrib.auth.models import User


def index_view(request, *args, **kwargs):
    return render_to_response('index.html', kwargs)

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