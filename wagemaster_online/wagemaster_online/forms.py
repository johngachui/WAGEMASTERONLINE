from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User, Client, Company, Subscription,ClientGroup,ExtendedGroup,Supervisor
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
    user_type = forms.ChoiceField(choices=User.USER_TYPE_CHOICES, required=True)
    default = forms.BooleanField(required=False)

    client_groups = forms.ModelMultipleChoiceField(
        queryset=ClientGroup.objects.none(),  # Initially set to none
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    
    class Meta:
        model = Group
        fields = ['name', 'permissions', 'user_type', 'default']

    def __init__(self, *args, **kwargs):
        group_instance = kwargs.pop('instance', None)
        super(GroupCreationForm, self).__init__(*args, **kwargs)

        self.fields['permissions'].queryset = Permission.objects.all().order_by('id')
        # Always add client_groups field, but conditionally populate it
        self.fields['client_groups'].queryset = ClientGroup.objects.all().order_by('id')

        extended_group = None
        if group_instance:
            self.instance = group_instance
            self.fields['name'].initial = group_instance.name
            self.fields['permissions'].initial = group_instance.permissions.all()

            try:
                extended_group = ExtendedGroup.objects.get(group=group_instance)
                self.fields['user_type'].initial = extended_group.user_type
                self.fields['default'].initial = extended_group.default
                # Conditionally populate client_groups based on user type
                if extended_group.user_type == User.ADMINISTRATOR:
                    self.fields['client_groups'].initial = extended_group.client_groups.all()
            except ExtendedGroup.DoesNotExist:
                pass
        # Additional logic for new form (not an instance)
        if not group_instance:
            # Set default behavior for client_groups when creating a new group
            # For example, if you want to show all client groups for a new 'Administrator' type group
            user_type = self.data.get('user_type', User.ADMINISTRATOR)  # Default to Administrator
            if user_type == User.ADMINISTRATOR:
                self.fields['client_groups'].queryset = ClientGroup.objects.all().order_by('id')
        
    def save(self, commit=True):
        group = super().save(commit=False)
        if commit:
            group.save()
            self.save_m2m()

        user_type_value = int(self.cleaned_data['user_type'])

        # Get or create ExtendedGroup instance with user_type set
        extended_group, created = ExtendedGroup.objects.get_or_create(
            group=group,
            defaults={'user_type': user_type_value, 'default': self.cleaned_data['default']}
        )

        # Update the ExtendedGroup instance if it already exists
        if not created:
            extended_group.user_type = user_type_value
            extended_group.default = self.cleaned_data['default']
            extended_group.save()

        if 'client_groups' in self.cleaned_data:
            extended_group.client_groups.set(self.cleaned_data['client_groups'])

        return group


    def clean_name(self):
        name = self.cleaned_data['name']
        if self.instance and self.instance.pk and self.instance.name == name:
            return name
        if Group.objects.filter(name=name).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Group with this Name already exists.")
        return name
   
    
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
        fields = ['CompanyName', 'CompanyEmail', 'CompanyTel', 'CompanyContactPerson', 'ClientIdentity', 'CompanyKey']
        widgets = {'ClientIdentity': forms.HiddenInput()}

class SupervisorForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Assuming you want to disable the client field to prevent users from manually changing it
        self.fields['client'].disabled = True

    class Meta:
        model = Supervisor
        fields = ['SupervisorName', 'Email', 'SupervisorTel', 'client']
        widgets = {'client': forms.HiddenInput()}


class SubscriptionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['CompanyIdentity'].disabled = True

    class Meta:
        model = Subscription
        fields = ['SubscriptionID', 'SubscriptionStartDate', 'SubscriptionEndDate', 'SubscriptionStatus','SubscriptionActionDate','Maximum_Employees', 'CompanyIdentity']
        widgets = {'CompanyIdentity': forms.HiddenInput()}
       

