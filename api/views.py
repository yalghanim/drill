from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView, DestroyAPIView, CreateAPIView, RetrieveUpdateAPIView
from homebrew.models import Brew
from .serializers import PostListSerializer, PostDetailSerializer, PostCreateSerializer

class PostListAPIView(ListAPIView):
    queryset = Brew.objects.all()
    serializer_class = PostListSerializer

class PostDetailAPIView(RetrieveAPIView):
    queryset = Brew.objects.all()
    serializer_class = PostDetailSerializer
    lookup_field = 'slug'
    lookup_url_kwarg = 'post_slug'

class PostDeleteAPIView(DestroyAPIView):
    queryset = Brew.objects.all()
    serializer_class = PostDetailSerializer
    lookup_field = 'slug'
    lookup_url_kwarg = 'post_slug'

class PostCreateAPIView(CreateAPIView):
    queryset = Brew.objects.all()
    serializer_class = PostCreateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class PostUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Brew.objects.all()
    serializer_class = PostCreateSerializer
    lookup_field = 'slug'
    lookup_url_kwarg = 'post_slug'

