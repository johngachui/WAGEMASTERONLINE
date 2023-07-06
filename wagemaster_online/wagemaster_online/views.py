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
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.urls import reverse
from urllib.parse import urlencode

User = get_user_model()
logger = logging.getLogger(__name__)
#@method_decorator(csrf_exempt, name='dispatch')

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
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            username = form.cleaned_data['username']  # Get the entered username
            
            # Check if a user with the same username already exists
            existing_user = User.objects.filter(username=username).exists()
            if existing_user:
                messages.error(request, 'Username already exists. Please choose a different username.')
                return render(request, 'create_client.html', {'form': form}) # Redirect back to the same form

            # Create a new user with the entered username
            user = User.objects.create_user(username=username)
            
            # Assign the user instance to the ClientUserID field
            client.ClientUserID = user
            
            # Save the user and client objects
            user.save()
            client.save()
            created_client_id = client.pk
            #return redirect('administrator_dashboard')
            url = reverse('administrator_dashboard') + '?selected_client=' + str(created_client_id)
            return redirect(url)
    else:
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

    # Retrieve the associated user for the client
    user = client.ClientUserID
    
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            # Get the original username from the user instance
            original_username = user.username
            # Check if the username has changed
            new_username = form.cleaned_data['username']
            if original_username != new_username:
                # Check if the new username is already in use
                if User.objects.filter(username=new_username).exists():
                    # Provide feedback to the user
                    messages.error(request, "Username already in use. Please choose another one.")
                else:
                    # Update the username in the User model
                    user.username = new_username
                    user.save()
                    form.save()
                    #messages.success(request, "Client information successfully updated!")
                    return redirect('administrator_dashboard')
            else:
                form.save()
                messages.success(request, "Client information successfully updated!")
                return redirect('administrator_dashboard')
        
    else:
        # Populate the form with the client details and the original username
        form = ClientForm(instance=client, initial={'username': user.username})

    context = {'form': form, 'selected_client_id': selected_client_id, 'client': client, 'username': user.username}

    return render(request, 'client_update.html', context)

class ClientDeleteView(View):
    def post(self, request, *args, **kwargs):
        client_id = request.POST.get('client_id')
        client = get_object_or_404(Client, ClientIdentity=client_id)
        user = get_object_or_404(User, id=client.ClientUserID_id)
        client.delete()
        user.delete()
        return JsonResponse({'status': 'success'})
    
class CompanyDeleteView(View):
    def post(self, request, *args, **kwargs):
        company_id = request.POST.get('company_id')
        company = get_object_or_404(Company, CompanyIdentity=company_id)
        company.delete()
        return JsonResponse({'status': 'success'})    

class SubscriptionDeleteView(View):
    def post(self, request, *args, **kwargs):
        subscription_id = request.POST.get('subscription_id')
        subscription = get_object_or_404(Subscription, SubscriptionID=subscription_id)
        subscription.delete()
        return JsonResponse({'status': 'success'})    

def check_username_availability(request):
    username = request.GET.get('username')
    client_id = request.GET.get('client_id')

    if client_id:
        # Exclude the current client from the check
        exists = User.objects.exclude(client__ClientIdentity=client_id).filter(username=username).exists()
    else:
        # Check for any user with the given username
        exists = User.objects.filter(username=username).exists()

    return JsonResponse({'exists': exists})


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
    selected_company_id = request.GET.get('selected_company')
    selected_client_id = request.GET.get('selected_client')
    
    print("selected_company_id:", selected_company_id)
    clients = Client.objects.all()
    for client in clients:
        print(client.ClientIdentity)
    client = get_object_or_404(Client, ClientIdentity=selected_client_id)
    
    if request.method == 'POST':
        form = CompanyForm(request.POST, initial={'ClientIdentity': client})
        if form.is_valid():
            company = form.save()

            # Get the created company ID
            created_company_id = company.pk

            # Build the URL parameters for the administrator_dashboard
            params = {
                'selected_client': selected_client_id,
                'selected_company': created_company_id
            }

            # Construct the URL for the administrator_dashboard with the client and company IDs
            url = reverse('administrator_dashboard') + '?' + urlencode(params)

            # Redirect to the administrator_dashboard with the client and company IDs in the URL
            return redirect(url)
    else:
        form = CompanyForm(initial={'ClientIdentity': client})
    
    return render(request, 'company_create.html', {'form': form, 'selected_company_id': selected_company_id, 'selected_client_id': selected_client_id, 'client': client})

def company_update(request):
    selected_company_id = request.GET.get('selected_company')
    selected_client_id = request.GET.get('selected_client')
    # Get the company object based on the selected_company_id
    company = get_object_or_404(Company, CompanyIdentity=selected_company_id)
    client = get_object_or_404(Client, ClientIdentity=selected_client_id)
    # Handle form submission
    if request.method == 'POST':
        # Initialize the form with the submitted data and the existing company instance
        form = CompanyForm(request.POST, instance=company)
        if form.is_valid():
            # Save the updated company object
            company = form.save()

            # Get the created company ID
            updated_company_id = company.pk
            # Build the URL parameters for the administrator_dashboard
            params = {
                'selected_client': selected_client_id,
                'selected_company': updated_company_id
            }

            # Construct the URL for the administrator_dashboard with the client and company IDs
            url = reverse('administrator_dashboard') + '?' + urlencode(params)

            # Redirect to the administrator_dashboard with the client and company IDs in the URL
            return redirect(url)
    else:
        # Prepopulate the form with the existing company data
        form = CompanyForm(instance=company)
    
    return render(request, 'company_update.html', {'form': form, 'selected_company_id': selected_company_id, 'company': company, 'client': client})

def subscription_create(request):
    #pdb.set_trace()
    selected_company_id = request.GET.get('selected_company')
    selected_client_id = request.GET.get('selected_client')
    selected_subscription_id = request.GET.get('selected_subscription')
    company = get_object_or_404(Company, CompanyIdentity=selected_company_id)
    
    if request.method == 'POST':
        form = SubscriptionForm(request.POST, initial={'CompanyIdentity': company})
        if form.is_valid():
            subscription = form.save()

            # Get the created company ID
            created_subscription_id = subscription.pk

            # Build the URL parameters for the administrator_dashboard
            params = {
                'selected_client': selected_client_id,
                'selected_company': selected_company_id,
                'selected_subscription': created_subscription_id
            }

            # Construct the URL for the administrator_dashboard with the client and company IDs
            url = reverse('administrator_dashboard') + '?' + urlencode(params)
        else:
            print(form.errors)
    else:

        form = SubscriptionForm(initial={'CompanyIdentity': company})
        
    return render(request, 'subscription_create.html', {'form': form, 'selected_subscription_id':selected_subscription_id,'selected_client_id':selected_client_id,'selected_company_id': selected_company_id, 'company': company})

def subscription_update(request):
    selected_subscription_id = request.GET.get('selected_subscription')
    selected_company_id = request.GET.get('selected_company')
    selected_client_id = request.GET.get('selected_client')
    
    subscription = get_object_or_404(Subscription, SubscriptionID=selected_subscription_id)
    company = get_object_or_404(Company, CompanyIdentity=selected_company_id)
    
    if request.method == 'POST':
        form = SubscriptionForm(request.POST, instance=subscription)
        if form.is_valid():
            form.save()
            return redirect('administrator_dashboard')
        else:
            print(form.errors)
    else:
        form = SubscriptionForm(instance=subscription)

    context = {
        'form': form,
        'selected_subscription_id': selected_subscription_id,
        'selected_company_id': selected_company_id,
        'selected_client_id':selected_client_id,
        'subscription': subscription,
        'company': company
        }
    return render(request, 'subscription_update.html', context)

def company_delete(request, company_id):
    company = get_object_or_404(Company, CompanyIdentity=company_id)
    if request.method == 'POST':
        company.delete()
        return redirect('company_list')
    return render(request, 'company_delete.html', {'company': company})
    
def administrator_dashboard(request):
    selected_client_id = request.GET.get('selected_client')
    selected_company_id = request.GET.get('selected_company')
    selected_subscription_id =request.GET.get('selected_subscription')

    clients = Client.objects.all().order_by('ClientName')
    companies = Company.objects.all().order_by('CompanyName')
    subscriptions = Subscription.objects.all().order_by('SubscriptionStartDate')
    divisions = Division.objects.all().order_by('DivisionName')
    employees = Employee.objects.all().order_by('StaffName')

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
        'selected_company_id': selected_company_id,
        'selected_subscription_id':selected_subscription_id,

    }
    return render(request, 'administrator_dashboard.html', context)

def dashboard(request):
    clients = Client.objects.all()
    initial_client_id = clients.first().ClientIdentity if clients else None
    return render(request, 'dashboard.html', {'clients': clients, 'initial_client_id': initial_client_id})

def fetch_companies(request):
    selected_client_id = request.GET.get('selected_client_id')
    print("Selected Client ID:", selected_client_id)
    companies = Company.objects.filter(ClientIdentity=selected_client_id).order_by('CompanyName')
    company_data = [{'name': company.CompanyName, 'id': company.CompanyIdentity} for company in companies]
    return JsonResponse(company_data, safe=False)

def fetch_subscriptions(request):
    selected_company_id = request.GET.get('selected_company_id')
    print("Selected Company ID:", selected_company_id)
    subscriptions = Subscription.objects.filter(CompanyIdentity=selected_company_id).order_by('-SubscriptionStartDate')
    subscription_data = [{'startdate': subscription.SubscriptionStartDate, 'stopdate': subscription.SubscriptionEndDate, 'subscriptionstatus': subscription.SubscriptionStatus, 'id': subscription.SubscriptionID } for subscription in subscriptions]
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