from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'question/', include('questions.urls')),

    url(r'^admin/', admin.site.urls),
]
