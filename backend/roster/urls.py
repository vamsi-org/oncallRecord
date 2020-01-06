from django.urls import path, include
from rest_framework.routers import DefaultRouter
from roster.api import OncallPeriodList, CallViewSet

router = DefaultRouter()
router.register(r'call', CallViewSet, basename='Call')

urlpatterns = [
    path('', include(router.urls)),
    path('calendar', OncallPeriodList.as_view())
]