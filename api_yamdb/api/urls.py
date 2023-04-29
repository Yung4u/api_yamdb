from django.urls import include, path
from rest_framework import routers
from api.views import (CommentViewSet, TitleViewSet,
                       GenreViewSet, CategoryViewSet,
                       ReviewViewSet, UserViewSet,
                       SignupViewSet, TokenViewSet)


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


urlpatterns = [
    path('v1/users/', UserViewSet.as_view({'get': 'list',
                                          'post': 'create',
                                          'patch': 'me'})),
    path('v1/users/me/', UserViewSet.as_view({'get': 'get_me',
                                             'patch': 'patch_me'})),
    path('v1/users/<str:username>/', UserViewSet.as_view(
        {'get': 'retrieve',
         'patch': 'update',
         'del': 'destroy'})),
    path('v1/auth/signup/',
         SignupViewSet.as_view({'post': 'create'})),
    path('v1/auth/token/',
         TokenViewSet.as_view({'post': 'create'})),
    path('v1/', include(router_v1.urls)),
]
