from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import Caracolien


class CaracolienForm(ModelForm):
    class Meta:
        model = Caracolien
        fields = ('phone_number', 'address')

    def clean_phone_number(self):
        phone = self.cleaned_data['phone_number']
        phone = phone.replace(' ', '').replace('.', '')
        if phone.startswith('0'):
            phone = '+33%s' % phone[1:]
        return phone


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
