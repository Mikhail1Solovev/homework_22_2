from django.contrib import admin
from django.urls import path, include
from users.views import HomePageView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('', HomePageView.as_view(), name='home'),
]
