# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import Blogger,Blog,Comment
admin.site.register(Blog)
admin.site.register(Blogger)
admin.site.register(Comment)

#class BlogAdmin(admin.ModelAdmin):
    #list_display=('headline','pub_date','blogger')
#admin.site.register(BlogAdmin)