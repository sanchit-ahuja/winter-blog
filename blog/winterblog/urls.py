from django.conf.urls import url,include

from . import views
app_name='winterblog'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^blogs/$',views.blog_list,name='blog_list'),
    url(r'^blog/(?P<blog_id>\d+)/$',views.blog_detail,name='blog_detail'),
    url(r'^signup/$',views.signup,name='signup'),
    url(r'^login/$',views.login2,name='login'),
    url(r'^logout/$',views.logout2,name='logout'),
    url(r'^blog/(?P<blog_id>\d+)/comment/$',views.comment,name='comment'),  
    url(r'^bloggers/$',views.blogger_list,name='blogger_list'),
    url(r'^bloggers/(?P<blogger_id>\d+)$',views.blogger_detail,name='blogger_detail'),  
    url(r'^delete/$',views.delete,name='delete'),
    url(r'^blog_create/$',views.blog_create,name='blog_create'),
    url(r'^export/xls/$',views.admin_tools_xls,name='xls'),
    url(r'^export/pdf/$',views.admin_tools_pdf,name='pdf'),
    
]