# Generated by Django 4.2.2 on 2023-12-16 23:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('wagemaster_online', '0033_clientgroup_client_client_group'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExtendedGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_type', models.IntegerField(choices=[(1, 'Administrator'), (2, 'Client'), (3, 'Supervisor'), (4, 'Employee')])),
                ('default', models.BooleanField(default=False)),
                ('group', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='auth.group')),
            ],
        ),
    ]