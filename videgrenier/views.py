from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DeleteView, DetailView, ListView, UpdateView

from caracole.forms import CaracolienForm, UserForm
from caracole.mixins import StaffRequiredMixin

from .forms import ReservationForm
from .models import Reservation


class ReservationListView(StaffRequiredMixin, ListView):
    model = Reservation


class ReservationModerateView(StaffRequiredMixin, UpdateView):
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
    def get_context_data(self, **kwargs):
        def get_infos(obj, field):
            return obj._meta.get_field(field).verbose_name, obj.__dict__[field]

        infos = [
            get_infos(self.object.caracolien.user, f) for f in ['last_name', 'first_name']
        ] + [
            get_infos(self.object.caracolien, f) for f in ['phone_number', 'address']
        ] + [
            get_infos(self.object, f) for f in ['birthdate', 'birthplace', 'id_num', 'id_date', 'id_org', 'plaque']
        ]
        return super().get_context_data(infos=infos, **kwargs)


@login_required
def reservation(request):
    ok = True
    try:
        reserv = request.user.caracolien.reservation
    except:
        reserv = None
    if request.method == 'POST':
        forms = [UserForm(request.POST, instance=request.user),
                 CaracolienForm(request.POST, instance=request.user.caracolien),
                 ReservationForm(request.POST, instance=reserv)]
        for form in forms:
            if form.is_valid():
                form.instance.caracolien = request.user.caracolien
                form.save()
            else:
                ok = False
        if ok:
            messages.success(request, 'Ces informations ont bien été enregistrées')
            return redirect('videgrenier:reservation-detail')
        else:
            messages.error(request, 'Certains champs présentent des erreurs')
    else:
        forms = [UserForm(instance=request.user),
                 CaracolienForm(instance=request.user.caracolien),
                 ReservationForm(instance=reserv)]
    return render(request, 'forms.html', {'forms': forms})
