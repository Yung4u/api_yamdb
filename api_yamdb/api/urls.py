from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import TitleViewSet, GenreViewSet, CategoryViewSet


router_v1 = DefaultRouter()

router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register('categories', CategoryViewSet,
                   basename='categories')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
]
