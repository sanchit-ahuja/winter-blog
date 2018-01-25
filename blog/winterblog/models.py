# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import date
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.urlresolvers import reverse



def markdown_to_html( markdownText, images ):    
    image_ref = ""

    for image in images:
        image_url = settings.MEDIA_URL + image.image.url
        image_ref = "%s\n[%s]: %s" % ( image_ref, image, image_url )

    md = "%s\n%s" % ( markdownText, image_ref )
    html = markdown.markdown( md )

    return html



class Blogger(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follower = models.ManyToManyField(User,related_name='following')
    def get_absolute_url(self):
        return reverse('blogger-detail',args=[str(self.id)])

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Blogger.objects.create(user=instance)

class Blog(models.Model):
    headline=models.CharField(max_length=100)
    pub_date=models.DateField(default=date.today)
    blog_text=models.TextField(max_length=1000)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    images = models.ImageField(upload_to='photo',null=True)
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

