# Generated by Django 4.2.2 on 2023-06-24 23:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagemaster_online', '0009_subscription_subscriptionactive_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='Maximum_Employees',
            field=models.IntegerField(default=10),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='CompanyIdentity',
            field=models.ForeignKey(db_column='CompanyIdentity', on_delete=django.db.models.deletion.CASCADE, related_name='subscription', to='wagemaster_online.company'),
        ),
    ]
