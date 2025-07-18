# Generated by Django 5.2.3 on 2025-07-05 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_remove_staff_is_available_service_department_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='department',
            field=models.CharField(choices=[('SCES Helpdesk', 'SCES Helpdesk'), ('Administration', 'Administration'), ('Lecturer Consultation', 'Lecturer Consultation')], default='SCES Helpdesk', max_length=50),
        ),
        migrations.AlterField(
            model_name='staff',
            name='status',
            field=models.CharField(choices=[('online', 'Online'), ('unavailable', 'Unavailable')], default='unavailable', max_length=20),
        ),
    ]
