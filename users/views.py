from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, ListView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CustomUserCreationForm
from .models import Product
from django.views.generic import TemplateView

User = get_user_model()

class HomePageView(TemplateView):
    template_name = 'home.html'

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('email_verification_needed')
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False  # Пока не подтвержден
        user.save()
        self.send_verification_email(user)
        return super().form_valid(form)

    def send_verification_email(self, user):
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        verification_link = self.request.build_absolute_uri(
            reverse_lazy('verify_email', kwargs={'uidb64': uid, 'token': token})
        )
        send_mail(
            'Подтверждение регистрации',
            f'Перейдите по ссылке для подтверждения регистрации: {verification_link}',
            'no-reply@example.com',
            [user.email],
        )

def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True  # Активировать учетную запись
        user.save()
        return redirect('login')
    else:
        return render(request, 'registration/verification_failed.html')

class CustomLoginView(LoginView):
    def form_valid(self, form):
        if form.get_user().is_active:
            return super().form_valid(form)
        else:
            return redirect('email_verification_needed')

def reset_password(request):
    email = request.POST['email']
    try:
        user = User.objects.get(email=email)
        new_password = User.objects.make_random_password()
        user.set_password(new_password)
        user.save()
        send_mail(
            'Новый пароль',
            f'Ваш новый пароль: {new_password}',
            'no-reply@example.com',
            [email],
        )
    except User.DoesNotExist:
        pass
    return redirect('password_reset_done')

class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'products/product_list.html'

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    fields = ['name', 'description']
    template_name = 'products/product_form.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    fields = ['name', 'description']
    template_name = 'products/product_form.html'

class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'products/product_confirm_delete.html'
    success_url = reverse_lazy('product_list')
