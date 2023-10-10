from django.views.generic.edit import CreateView
from django.shortcuts import redirect
from .models import CustomUser
from django.views import View
from .forms import CustomUserCreationForm, CustomUserUpdateForm
from django.urls import reverse_lazy, reverse
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView, DeleteView
from config import settings
import secrets
from django.contrib.auth.models import Group


class RegisterView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'users/customuser_form.html'
    success_url = reverse_lazy('mailing_creation:home')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        token = secrets.token_urlsafe(nbytes=8)

        user.token = token
        activate_url = reverse_lazy('users:confirm_mail', kwargs={'token': user.token})
        send_mail(
            subject='Подтверждение почты',
            message=f'Для подтверждения регистрации перейдите по ссылке: http://localhost:8000/{activate_url}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False
        )
        user.save()

        return redirect('/')


class UserConfirmEmailView(View):
    def get(self, request, token):
        user = CustomUser.objects.get(token=token)
        user.groups.add(Group.objects.get(name='User'))
        user.is_active = True
        user.token = None
        user.save()
        return redirect('users:login')


class ProfileView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserUpdateForm
    template_name = 'users/profile_detail.html'
    success_url = reverse_lazy('blog:main_page')

class DeleteProfile(LoginRequiredMixin, DeleteView):
    model = CustomUser
    success_url = reverse_lazy('blog:main_page')


def send_new_password(request):
    new_password = secrets.token_hex(nbytes=8)
    send_mail(
        subject='Вы сменили пароль',
        message=f'Ваш новый пароль: {new_password}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[request.user.email]
    )
    request.user.set_password(new_password)
    request.user.save()
    return redirect(reverse('blog:main_page'))
