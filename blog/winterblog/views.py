from __future__ import unicode_literals
from django.http import Http404
from django.shortcuts import render,get_object_or_404,redirect
from django.urls import reverse
from .models import Blog,Blogger,Comment
from django.views.generic import View
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse, HttpResponseRedirect,HttpRequest
from .forms import SignUpForm,LoginForm,CommentForm
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
@login_required
def blogger_list(request):
    pass
@login_required
def blog_list(request):
    blog_list=Blog.objects.order_by('pub_date')[:5]
    return render(request,'winterblog/blog_list.html',{'blog_list':blog_list})


@login_required
def blog_detail(request,blog_id):
    blog=get_object_or_404(Blog,pk=blog_id)
    return render(request,'winterblog/blog_detail.html',{'blog':blog})

    
@login_required
def comment(request,blog_id):
    if request.method=='POST':
        form=CommentForm(request.POST)
        if form.is_valid():
            comment_text=form.cleaned_data.get('comment_text')
            value=form.cleaned_data.get('value')
        form=CommentForm()
        b=request.POST['d']

        blog=Blog.objects.get(pk=b)
        comment=Comment.objects.filter(blog=blog)
    return render(request,'comment.html',{'comment':comment})
    #return HttpResponseRedirect("")
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