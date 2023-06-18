from django.shortcuts import render, redirect, get_object_or_404
from .models import Company , Subscription, Division, Employee, LeaveBalance, ProcessedLeave, LeaveApplication
from django.db import IntegrityError
import logging
from .models import User, Client
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail
from django.contrib.auth.views import LoginView

def home(request):
    return render(request, 'home.html')

from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .models import Client

def register(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)

            # Create a client object with the details
            client = Client(
                user=user,
                company_name=request.POST['company_name'],
                tel=request.POST['tel'],
                contact_person=request.POST['contact_person']
            )

            # Send email to administrator
            administrator_email = 'admin@example.com'  # Replace with actual administrator email
            message = f"A new user has registered:\n\n" \
                      f"Company Name: {client.company_name}\n" \
                      f"Telephone: {client.tel}\n" \
                      f"Contact Person: {client.contact_person}\n"
            send_mail(
                'New User Registration',
                message,
                'admin@example.com',
                [administrator_email],
                fail_silently=True,
            )

            return redirect('home')
    else:
        user_form = UserCreationForm()

    return render(request, 'registration.html', {'user_form': user_form})

class UserLoginView(LoginView):
    template_name = 'login.html'

def user_list(request):
    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})

def company_detail(request, company_id):
    company = get_object_or_404(Company, CompanyIdentity=company_id)
    return render(request, 'company_detail.html', {'company': company})

def company_list(request):
    companies = Company.objects.all()
    return render(request, 'company_list.html', {'companies': companies})

def company_create(request):
     if request.method == 'POST':
        try:
            companies = Company(CompanyName=request.POST.get('CompanyName'), 
                                CompanyEmail=request.POST.get('CompanyEmail'), 
                                CompanyTel=request.POST.get('CompanyTel'), 
                                CompanyContactPerson=request.POST.get('CompanyContactPerson'))
            companies.save()
            return redirect('company_list')
        except IntegrityError as e:
            logging.error(str(e))
     return render(request, 'company_create.html')


def company_update(request, company_id):
    company = get_object_or_404(Company, CompanyIdentity=company_id)
    if request.method == 'POST':
        company.CompanyName = request.POST.get('CompanyName')
        company.CompanyEmail = request.POST.get('CompanyEmail')
        company.CompanyTel = request.POST.get('CompanyTel')
        company.CompanyContactPerson = request.POST.get('CompanyContactPerson')
        company.save()
        return redirect('company_list')
    return render(request, 'company_update.html', {'company': company})

def company_delete(request, company_id):
    company = get_object_or_404(Company, CompanyIdentity=company_id)
    if request.method == 'POST':
        company.delete()
        return redirect('company_list')
    return render(request, 'company_delete.html', {'company': company})
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib import messages

from .models import Client, Company, Subscription

def administrator_dashboard(request):
    # Retrieve all clients, companies, and subscription records
    clients = Client.objects.all()
    companies = Company.objects.all()
    subscriptions = Subscription.objects.all()

    if request.method == 'POST':
        # Create a new client
        client_email = request.POST['client_email']
        client = Client.objects.create(client_email=client_email)
        # Generate a one-time password
        one_time_password = generate_one_time_password()
        # Create a user with the client email as username and one-time password
        user = User.objects.create_user(username=client_email, password=one_time_password)
        # Link the user to the client record
        client.user = user
        client.save()
        # Send the one-time password to the client's email
        send_one_time_password_email(client_email, one_time_password)
        messages.success(request, 'Client created successfully. One-time password has been sent to the client\'s email.')
        return redirect('administrator_dashboard')

    context = {
        'clients': clients,
        'companies': companies,
        'subscriptions': subscriptions,
    }
    return render(request, 'administrator_dashboard.html', context)

def generate_one_time_password():
    # Implement your logic to generate a one-time password
    # For example, you can use random number generation or any other method you prefer
    return '12345'

def send_one_time_password_email(client_email, one_time_password):
    subject = 'Your One-Time Password'
    message = f'Your one-time password is: {one_time_password}'
    from_email = 'your-email@example.com'  # Replace with your email address
    to_email = client_email
    send_mail(subject, message, from_email, [to_email])

def subscription_detail(request, subscription_id):
    subscription = Subscription.objects.get(SubscriptionIdentity=subscription_id)
    return render(request, 'subscription_detail.html', {'subscription': subscription})

def subscription_list(request):
    subscription = Subscription.objects.all()
    return render(request, 'subscription_list.html', {'subscription': subscription})

def division_detail(request, division_id):
    division = Division.objects.get(SubscriptionIdentity=division_id)
    return render(request, 'division_detail.html', {'division': division})

def division_list(request):
    division = Division.objects.all()
    return render(request, 'division_list.html', {'division': division})

def employee_detail(request, employee_id):
    employee = Employee.objects.get(StaffIdentity=employee_id)
    return render(request, 'employee_detail.html', {'employee': employee})

def employee_list(request):
    employee = Employee.objects.all()
    return render(request, 'employee_list.html', {'employee': employee})

def leavebalance_detail(request, employee_id):
    leavebalance = LeaveBalance.objects.get(StaffIdentity=employee_id)
    return render(request, 'leavebalance_detail.html', {'leavebalance': leavebalance})

def processedleave_list(request, employee_id):
    processedleave = ProcessedLeave.objects.all()
    return render(request, 'processedleave_list.html', {'processedleave': processedleave})

def leaveapplication_detail(request, application_id):
    leaveapplication = LeaveApplication.objects.get(LeaveApplicationIdentity=application_id)
    return render(request, 'leaveapplication_detail.html', {'leaveapplication': leaveapplication})

def leaveapplication_list(request, employee_id):
    leaveapplication = LeaveApplication.objects.all()
    return render(request, 'leaveapplication_list.html', {'leaveapplication': leaveapplication})