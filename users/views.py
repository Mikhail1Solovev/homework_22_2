from django.contrib.auth import get_user_model
from django.views.generic import FormView, TemplateView, RedirectView
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from .forms import UserRegistrationForm, PasswordResetForm
from django.contrib.auth.forms import AuthenticationForm
import random
from django.core.mail import send_mail
from django.conf import settings

class HomePageView(FormView):
    template_name = 'home.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('profile')  # Перенаправление на страницу профиля после успешного входа

    def form_valid(self, form):
        email = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            messages.error(self.request, "Неверные учетные данные. Пожалуйста, попробуйте снова.")
            return self.form_invalid(form)

# Регистрация пользователя
class UserRegisterView(FormView):
    form_class = UserRegistrationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('home')  # Перенаправление на главную страницу после успешной регистрации

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)  # Автоматический вход в систему после регистрации
        return super().form_valid(form)

# Сброс пароля
class PasswordResetView(FormView):
    form_class = PasswordResetForm
    template_name = 'registration/password_reset_form.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        user = get_user_model().objects.get(email=email)
        new_password = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=8))
        user.set_password(new_password)
        user.save()

        send_mail(
            'Новый пароль',
            f'Ваш новый пароль: {new_password}',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
        )
        return super().form_valid(form)

# Страница профиля (пример)
class ProfileView(TemplateView):
    template_name = 'profile.html'

# Класс-представление для выхода из системы
class LogoutView(RedirectView):
    url = reverse_lazy('home')  # Перенаправление на главную страницу после выхода

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)
