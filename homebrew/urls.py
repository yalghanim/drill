from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^home/', views.home, name="home"),
    url(r'^fourth/', views.fourth, name="fourth"),
    url(r'^day/', views.day, name="day"),
    url(r'^task/', views.task, name="task"),
    url(r'^all/$', views.allobj, name="allobj"),
    url(r'^intlink/(?P<slug>[-\w]+)/$', views.intlink, name="intlink"),
    url(r'^create/', views.create, name="create"),
    url(r'^update/(?P<slug>[-\w]+)/$', views.update, name="update"),
    url(r'^delete/(?P<slug>[-\w]+)/$', views.delete, name="delete"),

]
