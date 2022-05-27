from rest_framework import serializers

from .models import Post, Comment
from .validators import LessThanValidator, GreaterThanValidator


class PostSerializer(serializers.ModelSerializer):
    title = serializers.CharField(validators=[LessThanValidator(3), GreaterThanValidator(128)])
    body = serializers.CharField(validators=[LessThanValidator(3), GreaterThanValidator(4096)])
    author = serializers.ReadOnlyField(source='author.username')
    
    class Meta:
        model = Post
        fields = ['title', 'body', 'author']


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    post = serializers.ReadOnlyField(source='post.title')
    comment = serializers.CharField(validators=[LessThanValidator(3), GreaterThanValidator(4096)])
    
    class Meta:
        model = Comment
        fields = ['author', 'post', 'comment', 'related_to']

        
"""class PostCreateSerializer(serializers.ModelSerializer):
    title = serializers.CharField(validators=[LessThanValidator(3), GreaterThanValidator(128)])
    body = serializers.CharField(validators=[LessThanValidator(3), GreaterThanValidator(4096)])
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    
    class Meta:
        model = Post
        fields = ['title', 'body', 'author']"""
    
    


