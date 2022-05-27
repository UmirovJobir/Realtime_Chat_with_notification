from django.shortcuts import render
from rest_framework import mixins, generics, viewsets, permissions
from rest_framework.authentication import TokenAuthentication

from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer #PostCreateSerializer
from .permissions import ActionBasedPermission, AuthorAllStaffAllButEditOrReadOnly, IsOwnerOrReadOnly


class PostViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin,
                 mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (ActionBasedPermission,)
    action_permissions = {
        permissions.IsAuthenticated: ['create'],
        IsOwnerOrReadOnly: ['update', 'destroy', 'partial_update'],
        permissions.AllowAny: ['retrieve', 'list']
    }
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin,
                 mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (ActionBasedPermission,)
    action_permissions = {
        permissions.IsAuthenticated: ['create'],
        IsOwnerOrReadOnly: ['update', 'destroy', 'partial_update'],
        permissions.AllowAny: ['retrieve', 'list']
    }
    
    def perform_create(self, serializer):
        print('Request------------------ ', self.request.data)
        post = Post.objects.get(id=self.request.data['post'])
        related_to = self.request.data['related_to']
        if related_to is not None:
            try:
                related_to = Comment.objects.get(id=related_to)
            except:
                print('Related field not found')
        serializer.save(author=self.request.user, post=post)


"""class PostCreateView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer
    permission_classes= [permissions.IsAuthenticated]"""
