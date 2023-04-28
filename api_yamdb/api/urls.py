from django.urls import path

from . import views

urlpatterns = [
    path('api/v1/users', views.UserViewSet.as_view({'get': 'list',
                                                    'post': 'create',
                                                    'patch': 'me'})),
    path('api/v1/users/me', views.UserViewSet.as_view({'get': 'get_me',
                                                       'patch': 'patch_me'})),
    path('api/v1/users/<str:username>', views.UserViewSet.as_view(
        {'get': 'retrieve',
         'patch': 'update',
         'del': 'destroy'})),
    path('api/v1/auth/signup',
         views.SignupViewSet.as_view({'post': 'create'})),
    path('api/v1/auth/token',
         views.TokenViewSet.as_view({'post': 'create'})),
]
