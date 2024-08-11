from django.urls import path
from .views import UserRegisterView, PasswordResetView, HomePageView, ProfileView, LogoutView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', HomePageView.as_view(), name='home'),
]
