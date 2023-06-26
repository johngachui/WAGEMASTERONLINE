from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User, Client, Company, Subscription
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import get_object_or_404


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

class ClientForm(forms.ModelForm):
    username = forms.CharField(label='Username')  # Add username field

    class Meta:
        model = Client
        fields = ['username', 'ClientName', 'ClientEmail', 'ClientTel', 'ClientContactPerson']

class CompanyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ClientIdentity'].disabled = True

    class Meta:
        model = Company
        fields = ['CompanyName', 'CompanyEmail', 'CompanyTel', 'CompanyContactPerson', 'ClientIdentity']
        widgets = {'ClientIdentity': forms.HiddenInput()}

class SubscriptionForm(forms.ModelForm):
    #SubscriptionActive = forms.BooleanField(
    #    widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    #)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['CompanyIdentity'].disabled = True

    class Meta:
        model = Subscription
        fields = ['SubscriptionStartDate', 'SubscriptionEndDate', 'SubscriptionDatePaid', 'SubscriptionActive', 'SubscriptionKey', 'CompanyIdentity']
        widgets = {'CompanyIdentity': forms.HiddenInput()}
       

