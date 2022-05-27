from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import PostViewSet, CommentViewSet

router = DefaultRouter()
router.register('post', PostViewSet)
router.register('comment', CommentViewSet)


"""urlpatterns = [
    path('post/create/', PostCreateView.as_view())
]"""

urlpatterns = router.urls
