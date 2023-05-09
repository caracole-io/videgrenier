"""Vide Grenier views."""
import csv
from datetime import date
from typing import Any

from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

from ndh.utils import query_sum

from .forms import ReservationForm, UserForm
from .models import Reservation


class StaffRequiredMixin(UserPassesTestMixin):
    """Mixin to check that an user has staff access."""

    request: HttpRequest

    def test_func(self) -> bool:
        """Return the is_staff bool from the user model."""
        return bool(self.request.user.is_staff)


class ReservationListView(StaffRequiredMixin, ListView):
    """List all Reservation for staff."""

    model = Reservation

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        """Add the total number of emplacements requested to the context."""
        return super().get_context_data(
            total=query_sum(self.model.objects.all(), "emplacements"),
            **kwargs,
        )


class ReservationModerateView(StaffRequiredMixin, UpdateView):
    """Accept or deny a Reservation by Staff."""

    model = Reservation
    fields: list[str] = []

    def get(self, request, accepte, *args, **kwargs):
        """Set the accepted state on a Reservation by staff, and redirect to list."""
        reservation = self.get_object()
        reservation.accepte = accepte == 1
        reservation.save()
        return HttpResponseRedirect(reverse("videgrenier:reservation-list"))


class ReservationUserMixin(LoginRequiredMixin):
    """Mixin to check that an User has a Reservation."""

    request: HttpRequest

    def get_object(self, queryset=None) -> Reservation:
        """Get the Reservation for the current user, or 404."""
        return get_object_or_404(Reservation, user=self.request.user)


class ReservationDeleteView(ReservationUserMixin, DeleteView):
    """Let an User delete its Reservation."""

    success_url = reverse_lazy("videgrenier:home")


class ReservationDetailView(ReservationUserMixin, DetailView):
    """Show a Reservation details to its User."""

    object: Reservation  # noqa: A003

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        """Get infos for the User and its Reservation."""

        def get_infos(obj, field) -> tuple[str, Any]:
            """Helper function to get a field (verbose name & value) for an object."""
            return obj._meta.get_field(field).verbose_name, obj.__dict__[field]

        infos = [
            get_infos(self.object.user, f) for f in ["last_name", "first_name"]
        ] + [
            get_infos(self.object, f)
            for f in [
                "birthdate",
                "birthplace",
                "id_num",
                "id_date",
                "id_org",
                "plaque",
                "phone_number",
                "address",
            ]
        ]
        return super().get_context_data(infos=infos, **kwargs)


@login_required
def reservation(request: HttpRequest) -> HttpResponse:
    """Show the 2 forms for the User and Reservation data."""
    ok = True
    try:
        reserv: Reservation | None = request.user.reservation  # type: ignore
    except Exception:
        reserv = None
        if not (
            settings.DATES_VIDE_GRENIER["open"]
            <= date.today()
            <= settings.DATES_VIDE_GRENIER["close"]
        ):
            return redirect("videgrenier:fini")
    forms = [
        UserForm(request.POST or None, instance=request.user),  # type: ignore
        ReservationForm(request.POST or None, instance=reserv),
    ]
    if request.method == "POST":
        for form in forms:
            if form.is_valid():
                form.instance.user = request.user
                form.save()
            else:
                ok = False
        if ok:
            messages.success(request, "Ces informations ont bien été enregistrées")
            return redirect("videgrenier:reservation-detail")
        messages.error(request, "Certains champs présentent des erreurs")
    return render(request, "videgrenier/reservation_form.html", {"forms": forms})


@staff_member_required
def csview(request: HttpRequest) -> HttpResponse:
    """Let the staff download a csv with all Reservation data."""
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="videgrenier.csv"'

    writer = csv.writer(response)
    writer.writerow(
        [
            "Personne",
            "email",
            "Naissance",
            "Adresse",
            "Téléphone",
            "Pièce d`identité",
            "Immatriculation",
            "Emplacements",
            "Nature",
            "Accepté",
        ],
    )
    for reservation in Reservation.objects.all():
        writer.writerow(
            [
                f"{reservation.user.first_name} {reservation.user.last_name}",
                reservation.user.email,
                f"{reservation.birthdate} à {reservation.birthplace}",
                reservation.address,
                reservation.phone_number,
                f"n°{reservation.id_num} delivrée le {reservation.id_date} "
                f"par {reservation.id_org}",
                reservation.plaque,
                reservation.emplacements,
                reservation.nature,
                "Oui" if reservation.accepte else "Non",
            ],
        )
    return response


class FiniView(TemplateView):
    """View to show a static template when the vide grenier is not open."""

    def get_template_names(self) -> list[str]:
        """Get a list with the template name,
        if we are closed before or after a Vide Grenier."""
        return [
            "videgrenier/%s.html"
            % (
                "apres"
                if date.today() >= settings.DATES_VIDE_GRENIER["close"]
                else "avant"
            ),
        ]
