from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.shortcuts import render, redirect
from .models import User, Client

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['company_name', 'company_email', 'tel', 'contact_person']

def create_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            client.user = request.user  # Associate the client with the current user
            client.save()
            return redirect('administrator_dashboard')
    else:
        form = ClientForm()
    return render(request, 'create_client.html', {'form': form})
