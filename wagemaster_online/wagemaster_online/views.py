from django.shortcuts import render, redirect, get_object_or_404
from .models import Company , Subscription, Division, Employee, LeaveBalance, ProcessedLeave, LeaveApplication
from django.db import IntegrityError
import logging

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