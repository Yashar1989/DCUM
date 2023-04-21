from django.urls import path
from .views import (
    CustomLoginView,
    ProfileView,
    UserRegisterView,
    VerifyRegisterCode,
    logout_view,
    ProfileUpdateView,
    PasswordChange
)
from django.contrib.auth.views import PasswordResetView

app_name = 'account'

urlpatterns = [
    path('', CustomLoginView.as_view(), name='index'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/edit', ProfileUpdateView.as_view(), name='profile-edit'),
    path('logout/', logout_view, name='logout'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('verify/', VerifyRegisterCode.as_view(), name='verify'),
    path('change_password/', PasswordChange.as_view(), name='password-change'),

]
