from django.contrib import admin
from ask_kuznetsov.models import *

admin.site.register(Profile)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Tag)