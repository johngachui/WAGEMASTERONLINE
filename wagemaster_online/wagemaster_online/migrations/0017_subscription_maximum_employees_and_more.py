# Generated by Django 4.2.2 on 2023-07-01 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wagemaster_online', '0016_remove_subscription_subscriptionkey'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='Maximum_Employees',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='subscription',
            name='SubscriptionActive',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='subscription',
            name='SubscriptionDatePaid',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='subscription',
            name='SubscriptionEndDate',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='subscription',
            name='SubscriptionKey',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='subscription',
            name='SubscriptionStartDate',
            field=models.DateField(blank=True, null=True),
        ),
    ]
