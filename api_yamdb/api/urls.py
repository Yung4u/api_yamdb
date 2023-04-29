from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router_v1 = DefaultRouter()

router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register('categories', CategoryViewSet,
                   basename='categories')

urlpatterns = [
    path('v1/users', views.UserViewSet.as_view({'get': 'list',
                                                    'post': 'create',
                                                    'patch': 'me'})),
    path('v1/users/me', views.UserViewSet.as_view({'get': 'get_me',
                                                       'patch': 'patch_me'})),
    path('v1/users/<str:username>', views.UserViewSet.as_view(
        {'get': 'retrieve',
         'patch': 'update',
         'del': 'destroy'})),
    path('v1/auth/signup',
         views.SignupViewSet.as_view({'post': 'create'})),
    path('v1/auth/token',
         views.TokenViewSet.as_view({'post': 'create'})),
    path('v1/', include(router_v1.urls)),
]
