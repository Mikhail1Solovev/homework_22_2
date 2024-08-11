from django import forms
from django.contrib.auth.forms import PasswordResetForm as DjangoPasswordResetForm
from .models import CustomUser

# Форма регистрации пользователя
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'avatar', 'phone_number', 'country']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # Установка хешированного пароля
        if commit:
            user.save()
        return user

# Форма сброса пароля
class PasswordResetForm(DjangoPasswordResetForm):
    email = forms.EmailField(label="Email", max_length=254)

    def clean_email(self):
        email = self.cleaned_data['email']
        if not CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с таким email не зарегистрирован.")
        return email
