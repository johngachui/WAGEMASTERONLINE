from django.shortcuts import render, redirect, get_object_or_404
from .models import Company , Subscription, Division, Employee, LeaveBalance, ProcessedLeave, LeaveApplication
from django.db import IntegrityError
import logging
from .models import User, Client, Company, Subscription
from django.contrib.auth import get_user_model
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.views import LoginView
from .forms import ClientForm, CompanyForm, SubscriptionForm
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.contrib import messages
import pdb
from django.http import JsonResponse

User = get_user_model()
logger = logging.getLogger(__name__)

def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['User']
        company_name = request.POST['ClientName']
        company_email = request.POST['ClientEmail']
        tel = request.POST['ClientTel']
        contact_person = request.POST['ClientContactPerson']

        # Send email to administrator
        administrator_email = 'admin@digitalframeworksltd.com'  # Replace with actual administrator email
        message = f"A new registration for online leave has been submitted:\n\n" \
                  f"Company Name: {company_name}\n" \
                  f"Username: {username}\n" \
                  f"Company Email: {company_email}\n" \
                  f"Telephone: {tel}\n" \
                  f"Contact Person: {contact_person}\n"
        
        try:
            send_mail(
                'New User Registration',
                message,
                'admin@digitalframeworksltd.com',
                [administrator_email],
                fail_silently=False,
            )
            messages.success(request, 'Registration successful. An email has been sent to the administrator for verification.')
        except BadHeaderError:
            messages.error(request, 'Failed to send registration email. Please try again later.')

        return redirect('home')

    return render(request, 'registration.html')

def create_client(request):
    #pdb.set_trace()
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            username = form.cleaned_data['username']  # Get the entered username
            
            try:
                # Check if a user with the same username already exists
                existing_user = User.objects.filter(username=username).exists()
                if existing_user:
                    messages.error(request, 'Username already exists. Please choose a different username.')
                    return redirect('administrator_dashboard')

                # Create a new user with the entered username
                user = User.objects.create_user(username=username)
                client.ClientUserID = user.id
                logger.debug(f"Username: {username}")
                logger.debug(f"User ID: {user.id}")
                logger.debug(f"Client: {client}")
                # Create a user profile with a one-time password
                one_time_password = generate_one_time_password()
                user.set_password(one_time_password)
                user.is_administrator = False
                

                try:
                    user.save()
                    logger.debug("User saved successfully")
                except Exception as e:
                    logger.exception(f"Error saving user: {e}")
                
                try:
                    client.save()
                    logger.debug("Client saved successfully")
                except Exception as e:
                    logger.exception(f"Error saving client: {e}")

                # Send the user details via email
                send_one_time_password_email(client.ClientEmail, one_time_password)

                return redirect('administrator_dashboard')
            except User.DoesNotExist:
                # Handle the case when the user does not exist
                messages.error(request, 'Invalid username. Please try again.')
                return redirect('administrator_dashboard')
    else:
        print(form.errors)  # Print form errors to the console for debugging purposes

        form = ClientForm()
    return render(request, 'create_client.html', {'form': form})

class UserLoginView(LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        user = self.request.user
        if user.is_authenticated and user.is_administrator:
            return '/admin/dashboard/'  # Redirect to the administrator dashboard
        else:
            return '/client/dashboard/'  # Redirect to the client dashboard

def client_list(request):
    clients = Client.objects.all()
    return render(request, 'client_list.html', {'clients': clients})

def client_update(request):
    selected_client_id = request.GET.get('selected_client')
    client = get_object_or_404(Client, ClientIdentity=selected_client_id)
    
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            # Redirect to a success page or perform any other desired action
    else:
        form = ClientForm(instance=client)

    context = {'form': form, 'selected_client_id': selected_client_id, 'client': client}
    return render(request, 'client_update.html', context)

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
    selected_client_id = request.GET.get('selected_client')
    print("Selected Client ID:", selected_client_id)
    clients = Client.objects.all()
    for client in clients:
        print(client.ClientIdentity)
    client = get_object_or_404(Client, ClientIdentity=selected_client_id)
    
    if request.method == 'POST':
        form = CompanyForm(request.POST, initial={'ClientIdentity': client})
        if form.is_valid():
            form.save()
            return redirect('administrator_dashboard')
    else:
        form = CompanyForm(initial={'ClientIdentity': client})
    
    return render(request, 'company_create.html', {'form': form, 'selected_client_id': selected_client_id, 'client': client})

def subscription_create(request):
    #pdb.set_trace()
    selected_company_id = request.GET.get('selected_company')
    company = get_object_or_404(Company, CompanyIdentity=selected_company_id)
    
    if request.method == 'POST':
        form = SubscriptionForm(request.POST, initial={'CompanyIdentity': company})
        if form.is_valid():
            form.save()
            return redirect('administrator_dashboard')
        else:
            print(form.errors)
    else:

        form = SubscriptionForm(initial={'CompanyIdentity': company})
        
    return render(request, 'subscription_create.html', {'form': form, 'selected_company_id': selected_company_id, 'company': company})

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
    
def administrator_dashboard(request):
    selected_client_id = request.GET.get('selected_client')
    selected_company_id = request.GET.get('selected_company')

    clients = Client.objects.all()
    companies = Company.objects.all()
    subscriptions = Subscription.objects.all()
    divisions = Division.objects.all()
    employees = Employee.objects.all()

    client_form = ClientForm()
    company_form = CompanyForm()
    subscription_form = SubscriptionForm()

    context = {
        'companies': companies,
        'clients': clients,
        'subscriptions': subscriptions,
        'divisions': divisions,
        'employees': employees,

        'client_form': client_form,
        'company_form': company_form,
        'subscription_form': subscription_form,
        
        'selected_client_id': selected_client_id,
        'selected_company_id': selected_company_id
    }
    return render(request, 'administrator_dashboard.html', context)

def dashboard(request):
    clients = Client.objects.all()
    initial_client_id = clients.first().ClientIdentity if clients else None
    return render(request, 'dashboard.html', {'clients': clients, 'initial_client_id': initial_client_id})


def fetch_companies(request):
    selected_client_id = request.GET.get('selected_client_id')
    print("Selected Client ID:", selected_client_id)
    companies = Company.objects.filter(ClientIdentity=selected_client_id)
    company_data = [{'name': company.CompanyName, 'id': company.CompanyIdentity} for company in companies]
    return JsonResponse(company_data, safe=False)

def fetch_subscriptions(request):
    selected_company_id = request.GET.get('selected_company_id')
    print("Selected Company ID:", selected_company_id)
    subscriptions = Subscription.objects.filter(CompanyIdentity=selected_company_id)
    subscription_data = [{'startdate': subscription.SubscriptionStartDate, 'stopdate': subscription.SubscriptionEndDate, 'isactive': subscription.SubscriptionActive, 'id': subscription.SubscriptionID } for subscription in subscriptions]
    return JsonResponse(subscription_data, safe=False)

def generate_one_time_password():
    return get_random_string(length=5, allowed_chars='1234567890')

def send_one_time_password_email(client_email, one_time_password):
    subject = 'Your One-Time Password'
    message = f'Your one-time password is: {one_time_password}'
    from_email = 'admin@digitalframeworksltd.com'  # Replace with your email address
    to_email = client_email
    send_mail(subject, message, from_email, [to_email])

def client_dashboard(request):
    user = request.user
    client = user.client  # Get the client associated with the user

    # Retrieve the client's companies and subscriptions
    companies = Company.objects.filter(ClientIdentity=client)
    subscriptions = Subscription.objects.filter(CompanyIdentity__ClientIdentity=client)

    context = {
        'client': client,
        'companies': companies,
        'subscriptions': subscriptions
    }

    return render(request, 'client_dashboard.html', context)

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