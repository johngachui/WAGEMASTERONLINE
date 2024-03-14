from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from datetime import date
from django.utils import timezone
from datetime import timedelta

class User(AbstractUser):
    ADMINISTRATOR = 1
    CLIENT = 2
    SUPERVISOR = 3
    EMPLOYEE = 4

    USER_TYPE_CHOICES = (
        (ADMINISTRATOR, 'Administrator'),
        (CLIENT, 'Client'),
        (SUPERVISOR, 'Supervisor'),
        (EMPLOYEE, 'Employee'),
    )

    user_type = models.IntegerField(choices=USER_TYPE_CHOICES, default=EMPLOYEE)

class ClientGroup(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'client_group'  

class ExtendedGroup(models.Model):
    group = models.OneToOneField(Group, on_delete=models.CASCADE)
    user_type = models.IntegerField(choices=User.USER_TYPE_CHOICES)
    default = models.BooleanField(default=False)
    client_groups = models.ManyToManyField(ClientGroup, blank=True)

    def __str__(self):
        return self.group.name
        
class OneTimePassword(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    used = models.BooleanField(default=False)

    @property
    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=1440)  # OTP expires after 1 day
  
class Client(models.Model):
    ClientIdentity = models.AutoField(primary_key=True)
    ClientName = models.CharField(max_length=255)
    ClientEmail = models.EmailField()
    ClientTel = models.CharField(max_length=20)
    ClientContactPerson = models.CharField(max_length=255)
    users = models.ManyToManyField(User, related_name='clients')
    client_group = models.ForeignKey(ClientGroup, on_delete=models.PROTECT, null=True, blank=True)
    class Meta:
        db_table = 'client'
        

class Company(models.Model):
    CompanyIdentity = models.AutoField(primary_key=True, db_column='CompanyIdentity', 
                                       auto_created=True, blank=False, null=False)
    CompanyName = models.TextField(max_length=255)
    CompanyEmail = models.EmailField()
    CompanyTel = models.TextField(max_length=255)
    CompanyContactPerson = models.TextField()
    CompanyKey = models.TextField(default ="n/a")
    needs_sync = models.BooleanField(default=True)
    ClientIdentity = models.ForeignKey(Client, on_delete=models.CASCADE,
                                       related_name='company', db_column='ClientIdentity')
    class Meta:
        db_table = 'company'
        

class Subscription(models.Model):
    SubscriptionID =  models.AutoField(primary_key=True, db_column='SubscriptionID', 
                                       auto_created=True, blank=False, null=False)
    
    CompanyIdentity = models.ForeignKey(Company, on_delete=models.CASCADE,
                                       related_name='subscription', db_column='CompanyIdentity')
    SubscriptionStartDate = models.DateField(default=date(2022, 1, 1))
    SubscriptionEndDate = models.DateField(default=date(2022, 1, 1))
    SubscriptionActionDate = models.DateField(default=date(2022, 1, 1))
    Maximum_Employees = models.IntegerField(default=10)
    SubscriptionStatus = models.TextField(default ="Pending")
    CompanyKey = models.TextField(default ="n/a")
    class Meta:
        db_table = 'subscription'
        
class Division(models.Model):
    DivisionIdentity = models.AutoField(primary_key=True, db_column='DivisionIdentity', 
                                       auto_created=True, blank=False, null=False)
    CompanyIdentity = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        to_field='CompanyIdentity'
    )
    DivisionName = models.CharField(max_length=255)
    CompanyKey = models.TextField(default ="n/a")
    DivisionKey = models.TextField(default ="n/a")
    class Meta:
        db_table = 'division'

class Employee(models.Model):
    StaffIdentity = models.AutoField(primary_key=True, db_column='StaffIdentity', 
                                       auto_created=True, blank=False, null=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee_profile')
    CompanyIdentity = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        to_field='CompanyIdentity'
    )
    DivisionIdentity = models.ForeignKey(
        Division,
        on_delete=models.CASCADE,
        to_field='DivisionIdentity'
    )
    StaffNo = models.CharField(max_length=255)  
    StaffName = models.CharField(max_length=255)
    StaffIDNo = models.CharField(max_length=255)
    Email = models.EmailField()
    Employed = models.BooleanField()
    EmployeeKey = models.TextField(default ="n/a")
    needs_sync = models.BooleanField(default=True)
    class Meta:
        db_table = 'employee'

class Supervisor(models.Model):
    SupervisorIdentity = models.AutoField(primary_key=True, db_column='SupervisorIdentity', 
                                          auto_created=True, blank=False, null=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='supervisor_profile')
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='supervisors'
    )
    SupervisorName = models.CharField(max_length=255)
    Email = models.EmailField()
    SupervisorTel = models.TextField(max_length=255)
    employees = models.ManyToManyField('Employee', related_name='supervisors')

    class Meta:
        db_table = 'supervisor'



class LeaveBalance(models.Model):
    StaffIdentity = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        to_field='StaffIdentity'
    )
    AnnualBfwd = models.DecimalField(max_digits=10, decimal_places=2)
    AnnualCfwd = models.DecimalField(max_digits=10, decimal_places=2)
    Earned = models.DecimalField(max_digits=10, decimal_places=2)
    Taken = models.DecimalField(max_digits=10, decimal_places=2)
    Sold = models.DecimalField(max_digits=10, decimal_places=2)
    Adjustment = models.DecimalField(max_digits=10, decimal_places=2)
    Absence = models.DecimalField(max_digits=10, decimal_places=2)
    OffsBfwd = models.DecimalField(max_digits=10, decimal_places=2)
    OffsCfwd = models.DecimalField(max_digits=10, decimal_places=2)
    MaternityBfwd = models.DecimalField(max_digits=10, decimal_places=2)
    MaternityCfwd = models.DecimalField(max_digits=10, decimal_places=2)
    SickFull = models.DecimalField(max_digits=10, decimal_places=2)
    SickHalf = models.DecimalField(max_digits=10, decimal_places=2)
    EmployeeKey = models.TextField(default ="n/a")
    needs_sync = models.BooleanField(default=True)
    class Meta:
        db_table = 'leavebalance'

class ProcessedLeave(models.Model):
    WagemasterLeaveID = models.IntegerField()
    StaffIdentity = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        to_field='StaffIdentity'
    )
    LeaveType= models.TextField()
    StartDate = models.DateField()
    StopDate = models.DateField()
    Approved = models.BooleanField()
    NotApproved= models.BooleanField()
    Taken = models.BooleanField()
    EmployeeKey = models.TextField(default ="n/a")
    needs_sync = models.BooleanField(default=True)
    class Meta:
        db_table = 'processedleave'

class LeaveApplication(models.Model):
    LeaveApplicationIdentity = models.IntegerField()
    StaffIdentity = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        to_field='StaffIdentity'
    )
    LeaveType= models.TextField()
    StartDate = models.DateField()
    StopDate = models.DateField()
    EmployeeKey = models.TextField(default ="n/a")
    needs_sync = models.BooleanField(default=True)
    class Meta:
        db_table = 'leaveapplication'

class SyncTable(models.Model):
    table_name = models.CharField(max_length=255, unique=True)
    last_synced = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.table_name


