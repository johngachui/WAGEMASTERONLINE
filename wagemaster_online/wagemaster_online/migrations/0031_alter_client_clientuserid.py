# Generated by Django 4.2.2 on 2023-12-07 10:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagemaster_online', '0030_alter_onetimepassword_otp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='ClientUserID',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
