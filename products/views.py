from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from .models import Product

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    fields = ['title', 'description', 'category']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'products/product_list.html'


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'products/product_detail.html'


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
