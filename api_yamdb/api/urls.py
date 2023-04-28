from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from . import views

urlpatterns = [
    path('api/v1/users', views.UserViewSet.as_view({'get': 'list',
                                                    'post': 'create'})),
    path('api/v1/users/<str:username>', views.UserViewSet.as_view(
        {'get': 'retrieve',
         'patch': 'update',
         'del': 'destroy'})),
    path('api/v1/auth/signup', views.SignupViewSet.as_view({'post': 'create'})),
    path('api/v1/auth/token', views.TokenViewSet.as_view({'post': 'create'})),
]
