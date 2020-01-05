from django.urls import path, include
from profile.api import ProfileList

urlpatterns = [
    path('list', ProfileList.as_view())
    
]

'''
    path('profile/', roster_views.profile, name='profile'),
    path('logout/', user_views.LogoutView.as_view(template_name='record/logout.html'), name='logout'),
    path('login/', user_views.LoginView.as_view(template_name='record/login.html'), name='login'),
    path('roster/', roster_views.roster, name='roster')'''