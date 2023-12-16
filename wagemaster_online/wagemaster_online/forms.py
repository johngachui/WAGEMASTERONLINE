from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User, Client, Company, Subscription,ClientGroup,ExtendedGroup
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import Group, Permission

class GroupCreationForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    user_type = forms.ChoiceField(choices=User.USER_TYPE_CHOICES, required=True)  # Use User.USER_TYPE_CHOICES
    default = forms.BooleanField(required=False)

    class Meta:
        model = Group
        fields = ['name', 'permissions', 'user_type', 'default']

    def save(self, commit=True):
        # Save the Group instance
        group = super().save(commit=False)
        if commit:
            group.save()
            self.save_m2m()  # Save many-to-many data for the form.

        # Create or update the ExtendedGroup instance
        extended_group, created = ExtendedGroup.objects.get_or_create(group=group)
        extended_group.user_type = self.cleaned_data['user_type']
        extended_group.default = self.cleaned_data['default']
        if commit:
            extended_group.save()

        return group
    
    
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

class ClientForm(forms.ModelForm):
    users = forms.CharField(label='Username', required=True)

    class Meta:
        model = Client
        fields = ['ClientName', 'ClientEmail', 'ClientTel', 'ClientContactPerson', 'client_group', 'users']
    def clean_users(self):
        username = self.cleaned_data.get('users')
        # Check if the instance of the form already exists (i.e., updating a client)
        if self.instance and self.instance.pk:
            if not User.objects.filter(username=username).exists():
                raise forms.ValidationError("This username does not exist.")
        return username
    
    
class ClientGroupForm(forms.ModelForm):
    class Meta:
        model = ClientGroup
        fields = ['name']  # Include other fields if your model has more

        # Optionally, you can add widgets or other form options here
        # For example, to customize the input widget for 'name':
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Group Name'}),
        }
class CompanyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ClientIdentity'].disabled = True

    class Meta:
        model = Company
        fields = ['CompanyName', 'CompanyEmail', 'CompanyTel', 'CompanyContactPerson', 'ClientIdentity']
        widgets = {'ClientIdentity': forms.HiddenInput()}

class SubscriptionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['CompanyIdentity'].disabled = True

    class Meta:
        model = Subscription
        fields = ['SubscriptionID', 'SubscriptionStartDate', 'SubscriptionEndDate', 'SubscriptionStatus','SubscriptionActionDate','Maximum_Employees', 'SubscriptionKey', 'CompanyIdentity']
        widgets = {'CompanyIdentity': forms.HiddenInput()}
       

