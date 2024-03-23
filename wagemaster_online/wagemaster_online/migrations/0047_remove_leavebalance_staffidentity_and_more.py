# Generated by Django 4.2.11 on 2024-03-22 21:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagemaster_online', '0046_remove_supervisor_client_supervisor_clientidentity_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='leavebalance',
            name='StaffIdentity',
        ),
        migrations.RemoveField(
            model_name='leavebalance',
            name='id',
        ),
        migrations.AddField(
            model_name='leavebalance',
            name='employee',
            field=models.OneToOneField(db_column='StaffIdentity', default=1, on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='leave_balance', serialize=False, to='wagemaster_online.employee'),
            preserve_default=False,
        ),
    ]
