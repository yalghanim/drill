from rest_framework import serializers
from homebrew.models import Brew

class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brew
        fields = ['title', 'author', 'slug', 'number','publish',]

class PostDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brew
        fields = ['id', 'author', 'title', 'slug', 'number','publish','draft', 'email']

class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brew
        fields = ['title', 'number','email', 'publish','draft']
