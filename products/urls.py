from django.urls import path
from django.views.decorators.cache import cache_page
from .views import ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView, ProductDeleteView

urlpatterns = [
    path('', cache_page(60 * 15)(ProductListView.as_view()), name='product_list'),
    path('product/<int:pk>/', cache_page(60 * 15)(ProductDetailView.as_view()), name='product_detail'),
    path('product/new/', ProductCreateView.as_view(), name='product_create'),
    path('product/<int:pk>/edit/', ProductUpdateView.as_view(), name='product_update'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
]
