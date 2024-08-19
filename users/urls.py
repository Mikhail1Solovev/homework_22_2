from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import EmailVerificationNeededView

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('register/', views.SignUpView.as_view(), name='register'),
    path('verify/<uidb64>/<token>/', views.verify_email, name='verify_email'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('products/create/', views.ProductCreateView.as_view(), name='product_create'),
    path('products/<pk>/update/', views.ProductUpdateView.as_view(), name='product_update'),
    path('products/<pk>/delete/', views.ProductDeleteView.as_view(), name='product_delete'),
    path('email_verification_needed/', EmailVerificationNeededView.as_view(), name='email_verification_needed'),
]
