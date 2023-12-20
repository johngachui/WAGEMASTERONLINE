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

    def __init__(self, *args, **kwargs):
        group_instance = kwargs.pop('instance', None)
        print("Before super call, instance:", group_instance)
        print("kwargs before super call:", kwargs)

        super(GroupCreationForm, self).__init__(*args, **kwargs)
        print("After super call, self.instance:", self.instance)
        self.fields['permissions'].queryset = Permission.objects.all().order_by('id')
        #print(self.fields['permissions'].queryset)  # Debugging line

        if group_instance:
            self.fields['name'].initial = group_instance.name
            self.fields['permissions'].initial = group_instance.permissions.all()
            try:
                extended_group = ExtendedGroup.objects.get(group=group_instance)
                self.fields['user_type'].initial = extended_group.user_type
                self.fields['default'].initial = extended_group.default
            except ExtendedGroup.DoesNotExist:
                pass

=======
>>>>>>> eb0c99c6c5db06fd174f363996c128d8b733a7ea
    def save(self, commit=True):
        # Save the Group instance
        group = super().save(commit=False)
        if commit:
            group.save()
            self.save_m2m()  # Save many-to-many data for the form.

        print("user_type from form:", self.cleaned_data['user_type'])
        user_type_value = int(self.cleaned_data['user_type'])

        # Check if an ExtendedGroup instance already exists
        try:
            extended_group = ExtendedGroup.objects.get(group=group)
            extended_group.user_type = user_type_value
            extended_group.default = self.cleaned_data['default']
            if commit:
                extended_group.save()
        except ExtendedGroup.DoesNotExist:
            # Create a new ExtendedGroup instance if it does not exist
            ExtendedGroup.objects.create(
                group=group,
                user_type=user_type_value,
                default=self.cleaned_data['default']
            )

        return group
    
    def clean_name(self):
        name = self.cleaned_data['name']
        # Check if the form is editing an existing instance and the name is unchanged
        print("self.instance:",self.instance,"self.instance.pk:",self.instance.pk,"self.instance.name:",self.instance.name,"name:",name)
        if self.instance and self.instance.pk and self.instance.name == name:
            return name
        # Check if the name already exists in other groups
        if Group.objects.filter(name=name).exclude(pk=self.instance.pk).exists():
            print("Group with this Name already exists.")
            raise forms.ValidationError("Group with this Name already exists.")
        return name

 
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
       

