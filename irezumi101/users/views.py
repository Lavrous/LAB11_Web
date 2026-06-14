from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import LoginUserForm, RegisterUserForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from django.contrib.auth.views import PasswordChangeView
from .forms import ProfileUserForm, UserPasswordChangeForm
from django.contrib.auth import get_user_model

menu = [
    {'title': 'Главная', 'url_name': 'home'},
    {'title': 'О проекте', 'url_name': 'about'},
    {'title': 'Мастера', 'url_name': 'masters_home'},
]

class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {
        'title': "Вход в систему",
        'menu': menu,
    }

class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    extra_context = {
        'title': "Регистрация пользователя",
        'menu': menu,
    }
    success_url = reverse_lazy('users:login')

class ProfileUser(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'users/profile.html'
    extra_context = {
        'title': "Профиль пользователя",
        'menu': menu,
    }

    def get_success_url(self):
        return reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user

class UserPasswordChange(PasswordChangeView):
    form_class = UserPasswordChangeForm
    template_name = 'users/password_change_form.html'
    success_url = reverse_lazy('users:password_change_done')
    extra_context = {
        'title': "Изменение пароля",
        'menu': menu,
    }