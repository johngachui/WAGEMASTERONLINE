from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_administrator = models.BooleanField(default=False)

    # Add any additional fields or methods as needed

    def is_admin(self):
        return self.is_administrator

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='client')
    ClientIdentity = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=255)
    tel = models.CharField(max_length=20)
    contact_person = models.CharField(max_length=255)
    class Meta:
        db_table = 'client'
        
class Company(models.Model):
    CompanyIdentity = models.AutoField(primary_key=True, db_column='CompanyIdentity', 
                                       auto_created=True, blank=False, null=False)
    CompanyName = models.TextField()
    CompanyEmail = models.TextField()
    CompanyTel = models.TextField()
    CompanyContactPerson = models.TextField()
    ClientIdentity = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='company')
    class Meta:
        db_table = 'company'

class Subscription(models.Model):
    SubscriptionID =  models.AutoField(primary_key=True, db_column='SubscriptionID', 
                                       auto_created=True, blank=False, null=False)
    CompanyIdentity = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        to_field='CompanyIdentity'
    )
    SubscriptionKey = models.TextField()
    SubscriptionStartDate = models.DateField()
    SubscriptionEndDate = models.DateField()
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
    DivisionName = models.TextField()
    class Meta:
        db_table = 'division'

class Employee(models.Model):
    StaffIdentity = models.AutoField(primary_key=True, db_column='StaffIdentity', 
                                       auto_created=True, blank=False, null=False)
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
    StaffNo = models.TextField()   
    StaffName = models.TextField()
    StaffIDNo = models.TextField()
    Email = models.TextField()
    Employed = models.BooleanField()
    class Meta:
        db_table = 'employee'

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
    class Meta:
        db_table = 'leaveapplication'



