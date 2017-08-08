from django.conf.urls import url
from api.views import *

urlpatterns = [
    url(r'^all/$', PostListAPIView.as_view(), name="all"),
    url(r'^delete/(?P<post_slug>[-\w]+)/$', PostDeleteAPIView.as_view(), name="delete"),
    url(r'^create/$', PostCreateAPIView.as_view(), name="create"),
    url(r'^update/(?P<post_slug>[-\w]+)/$', PostUpdateAPIView.as_view(), name="update"),
]