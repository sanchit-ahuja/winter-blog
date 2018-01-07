from django.conf.urls import url,include

from . import views
app_name='winterblog'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    #url(r'^blogger/(?P<blogger_id>\d+)$',views.blogger,name='blogger'),
    url(r'^blogs/$',views.blog_list,name='blog_list'),
    url(r'^blog/(?P<blog_id>\d+)/$',views.blog_detail,name='blog_detail'),
    url(r'^signup/$',views.signup,name='signup'),
    url(r'^login/$',views.login2,name='login'),
    url(r'^logout/$',views.logout2,name='logout'),
    url(r'^blog/(?P<blog_id>\d+)/comment/$',views.comment,name='comment'),  
    url(r'^bloggers/$',views.blogger_list,name='blogger_list'),  
]