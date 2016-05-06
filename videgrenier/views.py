from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, DeleteView, DetailView, ListView, RedirectView, UpdateView

from caracole.mixins import StaffRequiredMixin

from .models import Reservation


class HomeView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_staff:
            return reverse('videgrenier:reservation-list')
        if not self.request.user.is_authenticated():
            return reverse('auth_login')
        if Reservation.objects.filter(caracolien__user=self.request.user).exists():
            return reverse('videgrenier:reservation-detail')
        return reverse('videgrenier:reservation-create')


class ReservationListView(StaffRequiredMixin, ListView):
    model = Reservation


class ReservationCreateView(LoginRequiredMixin, CreateView):
    model = Reservation
    fields = []
    success_url = reverse_lazy('videgrenier:home')

    def form_valid(self, form):
        form.instance.caracolien = self.request.user.caracolien
        return super().form_valid(form)


class ReservationUpdateView(StaffRequiredMixin, UpdateView):
    model = Reservation
    fields = []

    def get(self, request, accepte, *args, **kwargs):
        reservation = self.get_object()
        reservation.accepte = accepte == '1'
        reservation.save()
        return HttpResponseRedirect(reverse('videgrenier:reservation-list'))


class ReservationUserMixin(LoginRequiredMixin):
    def get_object(self, queryset=None):
        return get_object_or_404(Reservation, caracolien__user=self.request.user)


class ReservationDeleteView(ReservationUserMixin, DeleteView):
    pass


class ReservationDetailView(ReservationUserMixin, DetailView):
    pass
