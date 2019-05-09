"""oncallRecord URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from record import views as record_views
from roster import views as roster_views
from django.contrib.auth import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', record_views.home_func, name='home'),
    path('profile/', roster_views.profile, name='profile'),
    path('logout/', user_views.LogoutView.as_view(template_name='record/logout.html'), name='logout'),
    path('login/', user_views.LoginView.as_view(template_name='record/login.html'), name='login'),
    path('view_record/<int:pk>', record_views.OnCallDetail.as_view(), name='oncall_view'),
    path('view_call/<int:pk>/', record_views.CallDetail.as_view(), name='view_call'),
    #path('roster/', roster.calendar, name='roster')
]
