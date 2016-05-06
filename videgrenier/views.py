from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from caracole.mixins import StaffRequiredMixin

from .models import Reservation


class ReservationListView(StaffRequiredMixin, ListView):
    model = Reservation


class ReservationCreateView(LoginRequiredMixin, CreateView):
    model = Reservation
    fields = []

    def form_valid(self, form):
        form.instance.caracolien = self.request.user.caracolien
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        if Reservation.objects.filter(caracolien=self.request.user.caracolien).exists():
            return HttpResponseRedirect(reverse('videgrenier:reservation-detail'))
        return super().get(request, *args, **kwargs)


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
    success_url = reverse_lazy('videgrenier:home')


class ReservationDetailView(ReservationUserMixin, DetailView):
    pass
