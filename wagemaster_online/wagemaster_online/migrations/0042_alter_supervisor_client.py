# Generated by Django 4.2.2 on 2024-03-12 07:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagemaster_online', '0041_remove_supervisor_companyidentity_supervisor_client_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supervisor',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='supervisors', to='wagemaster_online.client'),
        ),
    ]
