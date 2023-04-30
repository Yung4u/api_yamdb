from django.urls import include, path
from rest_framework import routers
from api.views import (CommentViewSet, TitleViewSet,
                       GenreViewSet, CategoryViewSet,
                       ReviewViewSet, UserViewSet,
                       signup, TokenViewSet,
                       get_profile,)


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
router_v1.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('v1/users/me/',
         get_profile),
    path('v1/auth/signup/',
         signup),
    path('v1/auth/token/',
         TokenViewSet.as_view({'post': 'create'})),
    path('v1/', include(router_v1.urls)),
]
