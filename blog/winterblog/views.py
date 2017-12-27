from __future__ import unicode_literals
from django.http import Http404
from django.shortcuts import render,get_object_or_404,redirect
from django.urls import reverse
from django.views.generic import View
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse, HttpResponseRedirect,HttpRequest
from .forms import SignUpForm,LoginForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
def index(request):
    return render(request,'winterblog/index.html')
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'winterblog/signup.html', {'form': form})
def blogger(request):
    pass
def blog(request):
    pass
def comment(request):
    pass
def login2(request):
    if request.method=='POST':
        form=LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('winterblog/index.html')
    else:
        form = LoginForm()
    return render(request, 'winterblog/login.html', {'form': form})
def logout2(request):
    logout(request)
    return redirect('winterblog/index.html')