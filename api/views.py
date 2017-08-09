from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from homebrew.models import Brew
from .serializers import PostListSerializer, PostDetailSerializer, PostCreateSerializer 
from .serializers import CommentListSerializer, CommentCreateSerializer, UserCreateSerializer
from .serializers import UserLoginSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from .permissions import King
from django.db.models import Q
from rest_framework.filters import SearchFilter, OrderingFilter
from django_comments.models import Comment
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.utils import timezone

class PostListAPIView(ListAPIView):
    queryset = Brew.objects.all()
    serializer_class = PostListSerializer
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'number', 'author__first_name']

    def get_queryset(self, *args, **kwargs):
        queryset_list = Brew.objects.all()
        query = self.request.GET.get("q")
        if query:
            queryset_list = queryset_list.filter(
                Q(title__icontains=query)|
                Q(content__icontains=query)|
                Q(author__first_name__icontains=query)|
                Q(author__last_name__icontains=query)
                ).distinct()
        return queryset_list

class PostDetailAPIView(RetrieveAPIView):
    queryset = Brew.objects.all()
    serializer_class = PostDetailSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'
    lookup_url_kwarg = 'post_slug'

class PostDeleteAPIView(DestroyAPIView):
    queryset = Brew.objects.all()
    serializer_class = PostDetailSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    lookup_field = 'slug'
    lookup_url_kwarg = 'post_slug'

class PostCreateAPIView(CreateAPIView):
    queryset = Brew.objects.all()
    serializer_class = PostCreateSerializer
    permission_classes = [IsAuthenticated, King]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class PostUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Brew.objects.all()
    serializer_class = PostCreateSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    lookup_field = 'slug'
    lookup_url_kwarg = 'post_slug'

class CommentListAPIView(ListAPIView):
    serializer_class = CommentListSerializer
    permission_classes = [AllowAny]

    def get_queryset(self, *args, **kwargs):
        queryset_list = Comment.objects.all()
        query = self.request.GET.get("q")
        if query:
            queryset_list = queryset_list.filter(
                Q(object_pk=query)|
                Q(user=query)
                ).distinct()
        return queryset_list

class CommentCreateAPIView(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(
                content_type=ContentType.objects.get_for_model(Post),
                site=Site.objects.get(id=1),
                user = self.request.user,
                user_name = self.request.user.username,
                submit_date = timezone.now()
            )

class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer

class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request, format=None):
        data = request.data
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data, status=HTTP_200_OK)
        return Response(serializer.errors, HTTP_400_BAD_REQUEST)
