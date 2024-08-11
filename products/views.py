from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from .models import Product

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    fields = ['name', 'description']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
