from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (
    AuthView,
    profile_view,
    profile_edit_view,
    CustomPasswordChangeView,
)

urlpatterns = [
  
    path('auth/', AuthView.as_view(), name='auth'),

    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),

    path('profile/',      profile_view,      name='profile'),
    path('profile/edit/', profile_edit_view, name='profile-edit'),
    path('profile/password/', CustomPasswordChangeView.as_view(), name='password-change'),
]
