# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import date
from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


class Blogger(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    following = models.ManyToManyField(User,related_name='following')

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('blogger-detail',args=[str(self.id)])


class Blog(models.Model):
    headline=models.CharField(max_length=100)
    pub_date=models.DateField(default=date.today)
    blog_text=models.TextField(max_length=1000)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    def get_absolute_url(self):
        return reverse('blog-detail',args=[str(self.id)])
    def __str__(self):
        return self.headline
    class Meta:
        ordering=('pub_date',)


class Comment(models.Model):
    comment_text=models.TextField(max_length=200,help_text='Enter comment for the blog',null=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    blog=models.ForeignKey(Blog,on_delete=models.CASCADE,null=True)
    pub_date=models.DateTimeField(auto_now_add=True,null=True)
