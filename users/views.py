from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from .forms import CustomUserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin

class RegisterView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')  # Redirect to login page upon successful registration
    template_name = 'users/register.html'

class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    
    def get_success_url(self):
        next_url = self.request.POST.get('next') or self.request.GET.get('next')  # Checks both POST and GET for 'next'
        if next_url:
            return next_url
        return super().get_success_url()

class ProfileView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'users/profile.html'

    