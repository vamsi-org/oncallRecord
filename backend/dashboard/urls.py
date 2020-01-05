from django.urls import path, include
from .views import dashboard, OnCallDetail, CallDetail, Search

urlpatterns = [
    path('', dashboard, name="dashboard"),
    path('view_record/<int:pk>', OnCallDetail.as_view(), name='oncall_view'),
    path('view_call/<int:pk>/', CallDetail.as_view(), name='view_call'),
    path('search/', Search.as_view(), name='search'),
]