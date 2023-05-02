from django.urls import include, path
from rest_framework import routers

from api.views import (CommentViewSet, TitleViewSet,
                       GenreViewSet, CategoryViewSet,
                       ReviewViewSet)
from users.views import UserViewSet, signup, get_token


app_name = 'api'

router_v1 = routers.DefaultRouter()

router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register('categories', CategoryViewSet,
                   basename='categories')
router_v1.register(r'titles/(?P<title_id>\d+)/reviews',
                   ReviewViewSet, basename='reviews')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments')
router_v1.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('v1/auth/signup/',
         signup),
    path('v1/auth/token/',
         get_token),
    path('v1/', include(router_v1.urls)),
]
