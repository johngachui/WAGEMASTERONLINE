# Generated by Django 4.2.2 on 2023-07-01 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wagemaster_online', '0023_alter_subscription_subscriptiondatepaid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='SubscriptionActive',
            field=models.BooleanField(),
        ),
    ]