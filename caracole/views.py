from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import password_change
from django.shortcuts import render

from .forms import CaracolienForm, UserForm


@login_required
def profil_password(request):
    return password_change(request, post_change_redirect='profil')


@login_required
def profil(request):
    ok = True
    if request.method == 'POST':
        forms = [UserForm(request.POST, instance=request.user),
                 CaracolienForm(request.POST, instance=request.user.caracolien)]
        for form in forms:
            if form.is_valid():
                form.save()
            else:
                ok = False
    if ok:
        if request.method == 'POST':
            messages.success(request, 'Ces informations ont bien été enregistrées')
        forms = [UserForm(instance=request.user),
                 CaracolienForm(instance=request.user.caracolien)]
    else:
        messages.error(request, 'Certains champs présentent des erreurs')
    return render(request, 'profil.html', {'forms': forms})
