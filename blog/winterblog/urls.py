from django.conf.urls import url,include

from . import views
app_name='winterblog'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^blogger/(?P<blogger_id>\d+)$',views.blogger,name='blogger'),
    url(r'^blog/(?P<blog_id>\d+)$',views.blog,name='blog'),
    url(r'^blog/(?P<blog_id>\d+)/comment$',views.comment,name='comment'),
    url(r'^signup/$',views.signup,name='signup'),
    url(r'^login/$',views.login2,name='login'),
    url(r'^logout/$',views.logout2,name='logout')
    
]