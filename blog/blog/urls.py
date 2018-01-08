
from django.conf.urls import url,include
from django.contrib import admin

from django.conf.urls import include, url
from django.contrib import admin

urlpatterns=[
    url(r'blog/',include('winterblog.urls')),
    url(r'admin/',include(admin.site.urls)),
]
