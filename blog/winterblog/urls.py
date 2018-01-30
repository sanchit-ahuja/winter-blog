from django.conf.urls import url,include

from . import views
from django.conf.urls.static import static
from django.conf import settings
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
    url(r'^bloggers/(?P<user_id>\d+)$',views.blogger_detail,name='blogger_detail'),  
    url(r'^delete/(?P<typ>\w+)/(?P<id>\d+)$',views.delete,name='delete'),
    url(r'^blog_create/$',views.blog_create,name='blog_create'),
    url(r'^export/xls/$',views.admin_tools_xls,name='xls'),
    url(r'^export/pdf/$',views.admin_tools_pdf,name='pdf'),
    url(r'^follow/(?P<user_id>\d+)$',views.follow,name='follow'),
    url(r'^feed/(?P<user_id>\d+)$',views.feed,name='feed'),


]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)