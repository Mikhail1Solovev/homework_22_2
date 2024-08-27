from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from .models import Product
from django.core.cache import cache


def get_cached_categories():
    categories = cache.get('categories')
    if not categories:
        categories = list(Category.objects.all())
        cache.set('categories', categories, 60 * 15)
    return categories

@method_decorator(cache_page(60 * 15), name='dispatch')
class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'products/product_detail.html'


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    fields = ['title', 'description', 'category']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


@method_decorator(cache_page(60 * 15), name='dispatch')
class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'products/product_list.html'


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    fields = ['title', 'description', 'category']
    template_name = 'products/product_form.html'

    def test_func(self):
        product = self.get_object()
        return self.request.user == product.owner or self.request.user.has_perm('products.change_product')

    def handle_no_permission(self):
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = 'products/product_confirm_delete.html'
    success_url = '/products/'

    def test_func(self):
        product = self.get_object()
        return self.request.user == product.owner or self.request.user.has_perm('products.delete_product')

    def handle_no_permission(self):
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied
