# Generated by Django 4.2.2 on 2023-06-25 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wagemaster_online', '0010_subscription_maximum_employees_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='SubscriptionKey',
            field=models.TextField(null=True),
        ),
    ]
