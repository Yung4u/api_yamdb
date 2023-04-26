from django.urls import path
from . import views

urlpatterns = [
    path('api/v1/users', views.UserViewSet.as_view({'get': 'list',
                                                    'post': 'create'})),
    path('api/v1/users/<str:username>', views.UserViewSet.as_view(
        {'get': 'retrieve',
         'patch': 'update',
         'del': 'destroy'})),
]
