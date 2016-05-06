from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.views.generic import DetailView, UpdateView

from .forms import CaracolienForm
from .models import Caracolien


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User

    def get_object(self, queryset=None):
        return self.request.user


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ('username', 'email', 'first_name', 'last_name')
    success_url = reverse_lazy('profil')

    def get_object(self, queryset=None):
        return self.request.user


class PasswordUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = PasswordChangeForm
    success_url = reverse_lazy('profil')

    def get_object(self, queryset=None):
        return self.request.user


class CaracolienUpdateView(LoginRequiredMixin, UpdateView):
    model = Caracolien
    form_class = CaracolienForm
    success_url = reverse_lazy('profil')
    # fields = ('phone_number', 'address')

    def get_object(self, queryset=None):
        return self.request.user.caracolien
