from django.urls import path, include
from .api import RegisterAPI, LoginAPI, ProfileViewSet
from knox import views as knox_views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'profile', ProfileViewSet, basename='Profile')

urlpatterns = [
    path('', include('knox.urls')),
    path('', include(router.urls)),
    path('register', RegisterAPI.as_view()),
    path('login', LoginAPI.as_view()),
    path('logout', knox_views.LogoutView.as_view(), name='knox-logout'),
]
