# Generated by Django 4.2.2 on 2023-12-12 16:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagemaster_online', '0032_remove_client_clientuserid_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'client_group',
            },
        ),
        migrations.AddField(
            model_name='client',
            name='client_group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='wagemaster_online.clientgroup'),
        ),
    ]
