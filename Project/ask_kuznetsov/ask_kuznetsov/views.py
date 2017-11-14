# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.views.generic import TemplateView

class AboutView(TemplateView):
    template_name = "about.html"
