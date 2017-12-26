from __future__ import unicode_literals
from django.http import Http404
from django.shortcuts import render,get_object_or_404,redirect
from django.urls import reverse
from django.views import generic
from django.views.generic import View
from django.utils import timezone
from django.contrib.auth import authenticate
from django.http import HttpResponse, HttpResponseRedirect,HttpRequest

def index(request):
    return render(request,'winterblog/index.html')