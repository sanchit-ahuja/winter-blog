
from __future__ import unicode_literals
from django.http import Http404
from django.shortcuts import render,get_object_or_404,redirect
from django.urls import reverse
from .models import Blog,Blogger,Comment
from django.contrib.auth.models import User
from django.views.generic import View
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse, HttpResponseRedirect,HttpRequest
from .forms import SignUpForm,LoginForm,CommentForm,BlogForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import user_passes_test
import xlwt
# Visible View for the home page
def index(request):
    return render(request,'winterblog/index.html')


# Dual View (Hidden and Visible) for signing up
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/blog')
    else:
        form = SignUpForm()
    return render(request, 'winterblog/signup.html', {'form': form})


# Dual View for logging in
def login2(request):
    if request.method=='POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_password)
            print("User: {}".format(user))
            if user:
                login(request, user)
                return redirect('winterblog:index')
            else:
                return HttpResponse("Wrong Login Creds")
    else:
        form = LoginForm()
    return render(request, 'winterblog/login.html', {'form': form})


# Hidden View for logging out
def logout2(request):
    logout(request)
    return redirect('winterblog:login')


@login_required
def blogger_list(request):
    user_list=User.objects.all()
    return render(request,'winterblog/blogger_list.html',{'user_list':user_list})

@login_required
def blogger_detail(request, blogger_id):
    user=get_object_or_404(User, pk=blogger_id)
    blogs = Blog.objects.all().filter(id=blogger_id)
    return render(request,'winterblog/blogger_detail.html',{'blogs':blogs,'user':user})

@login_required
def blog_list(request):
    blog_list=Blog.objects.all()
    return render(request,'winterblog/blog_list.html',{'blog_list':blog_list})


@login_required
def blog_detail(request,blog_id):
    blog=get_object_or_404(Blog,pk=blog_id)
    comments=Comment.objects.all()
    return render(request,'winterblog/blog_detail.html',{'blog':blog, 'comments':comments})


@login_required
def blog_create(request):
    blog=Blog.objects.all()
    form=BlogForm(request.POST)
    if request.method=="GET":
        return render(request,'winterblog/blog_create.html',{'form':form})
    if request.method=="POST":
        if form.is_valid():
            blog=form.save(commit=False)
            blog.save()
            return redirect('winterblog:blog_list')
        else:
            form=BlogForm()
            return redirect('winterblog:blog_create')


@login_required
def comment(request,blog_id):
    blog=get_object_or_404(Blog,pk=blog_id)
    comments=Comment.objects.all().filter(id=blog_id)
    form=CommentForm(request.POST)
    if request.method == "GET":
        return render(request,'winterblog/comment.html',{'form':form})
    if request.method =='POST':
        if form.is_valid():
            comment=form.save(commit=False)
            comment.save()
            return redirect('winterblog:blog_detail',blog_id)
        else:
            form=CommentForm()
            comment=Comment.objects.filter(blog=blog)
            return redirect('winterblog:comment',blog_id)


#delete asking for two arguments
def delete(request,blog_id):
    blog=get_object_or_404(Blog,pk=blog_id)
    comment=get_object_or_404(Comment,pk=blog_id)
    if comment.user==request.user:
        comment.is_removed=True
        comment.save()
    return redirect('winterblog:blog_detail',blog_id)



@user_passes_test(lambda x:x.is_superuser)
def admin_tools_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="users.xls"'

    wb = xlwt.Workbook()
    ws = wb.add_sheet('Users')
    row_num = 0


    columns = ['Username', 'First name', 'Last name', 'Email address','password' ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num],)

    rows = User.objects.all().values_list('username', 'first_name', 'last_name', 'email','password')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], )

    wb.save(response)
    return response




    

    