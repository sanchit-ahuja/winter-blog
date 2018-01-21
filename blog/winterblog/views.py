
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
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle,Paragraph
from reportlab.lib.pagesizes import A4, cm 
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
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
def blogger_detail(request, user_id):
    user=get_object_or_404(User, pk=user_id)
    blogs = user.blog_set.all()
    print(blogs)
    return render(request,'winterblog/blogger_detail.html',{'blogs':blogs,'user':user})

@login_required
def blog_list(request):
    blog_list=Blog.objects.all()
    return render(request,'winterblog/blog_list.html',{'blog_list':blog_list})


@login_required
def blog_detail(request,blog_id):
    blog=get_object_or_404(Blog,pk=blog_id)
    comments=blog.comment_set.all()
    user = blog.user
    return render(request,'winterblog/blog_detail.html',{'blog':blog, 'comments':comments, 'user':blog.user})


@login_required
def blog_create(request):
    blog=Blog.objects.all()
    form=BlogForm(request.POST)
    if request.method=="GET":
        return render(request,'winterblog/blog_create.html',{'form':form})
    if request.method=="POST":
        if form.is_valid():
            blog=form.save(commit=False)
            blog.user=request.user
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
        context = {'blog_id':blog_id, 'form':form}
        return render(request,'winterblog/comment.html',context)
    if request.method =='POST':
        if form.is_valid():
            comment=form.save(commit=False)
            blog.user=request.user
            comment.user=request.user
            comment.blog = Blog.objects.get(pk=request.POST["blog_id"])
            comment.save()
            return redirect('winterblog:blog_detail',blog_id)
        else:
            form=CommentForm()
            comment=Comment.objects.filter(blog=blog)
            return redirect('winterblog:comment',blog_id)


def delete(request,typ,id):
    if typ == 'blog':
        blog = Blog.objects.get(id=id)
        blog.delete()
        return redirect('winterblog:blogger_detail',request.user.id)
    else:
        comment = Comment.objects.get(id=id)
        comment.delete()
        return redirect('winterblog:blog_detail',comment.blog.id)


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


def admin_tools_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment;   filename="users.pdf" '  
    buffer=BytesIO()
    p=canvas.Canvas(buffer,pagesize=A4)
    width, height = A4
    styles = getSampleStyleSheet()
    styleN = styles["BodyText"]
    styleN.alignment = TA_LEFT
    styleBH = styles["Normal"]
    styleBH.alignment = TA_CENTER
    user_data=User.objects.all().values_list('username','email')
    username=Paragraph("'<b>Username</b>'",styleBH)
    email=Paragraph("'<b>Email Id</b>'",styleBH)
    data=[[username,email]]
    for i in user_data:
        username=str(i.username).encode('utf-8')
        email=str(i.email).encode('utf-8')
        user=Paragraph(username,styleN)
        mail=Paragraph(email,styleN)
        data+=[user,mail]
    table=Table(data,colWidths=[4*cm,4*cm,4*cm,4*cm])
    p.showpage()
    p.save()
    pdf=buffer.getvalue()
    return response
    
def follow(request,user_id):
    blogger = Blogger.objects.get(user=request.user)
    userFolllow = get_object_or_404(Blogger, user_id=user_id)
    if request.method == 'POST':
        userFollow.follows.add(blogger)
    return redirect('winterblog:blogger_detail',user_id)

    