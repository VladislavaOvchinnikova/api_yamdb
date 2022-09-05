from django.urls import include, path
from rest_framework import routers

from .views import (APISignUp, CategoryViewSet, CommentViewSet,
                    CustomTokenObtainPairView, GenreViewSet, ReviewViewSet,
                    TitleViewSet, UserViewSet)

router_v1 = routers.DefaultRouter()
router_v1.register(
    r'titles/(?P<titles_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router_v1.register(
    r'titles/(?P<titles_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register('users', UserViewSet, basename='users')
router_v1.register('categories', CategoryViewSet, basename='categories')

urlpatterns = [
    path(
        'v1/auth/token/',
        CustomTokenObtainPairView.as_view(),
        name='token_custom'
    ),
    path('v1/auth/signup/', APISignUp.as_view(), name='signup'),
    path('v1/', include(router_v1.urls)),
]
