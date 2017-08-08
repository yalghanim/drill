from django.conf.urls import url
from . import views
from django.conf import settings 
from django.conf.urls.static import static 

urlpatterns = [
    url(r'^home/', views.home, name="home"),
    url(r'^fourth/', views.fourth, name="fourth"),
    url(r'^day/', views.day, name="day"),
    url(r'^task/', views.task, name="task"),
    url(r'^all/$', views.allobj, name="allobj"),
    url(r'^intlink/(?P<post_slug>[-\w]+)/$', views.intlink, name="intlink"),
    url(r'^create/', views.create, name="create"),
    url(r'^update/(?P<post_slug>[-\w]+)/$', views.update, name="update"),
    url(r'^delete/(?P<post_slug>[-\w]+)/$', views.delete, name="delete"),
    url(r'^ajax_like/(?P<post_id>\d+)/$', views.ajax_like, name="like_button"),
    url(r'^signup/$', views.usersignup, name="signup"),
    url(r'^login/$', views.userlogin, name="login"),
    url(r'^logout/$', views.userlogout, name="logout"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)