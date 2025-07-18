# Generated by Django 4.2 on 2025-07-04 11:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('myapp', '0003_queueentry'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='is_online',
        ),
        migrations.AddField(
            model_name='profile',
            name='online_status',
            field=models.CharField(choices=[('online', 'Online'), ('unavailable', 'Unavailable')], default='unavailable', max_length=15),
        ),
        migrations.AddField(
            model_name='queue',
            name='assigned_staff',
            field=models.ForeignKey(blank=True, limit_choices_to={'profile__role': 'staff'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assigned_tickets', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='queue',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='queue_tickets', to=settings.AUTH_USER_MODEL),
        ),
        migrations.RemoveField(
            model_name='service',
            name='staff_members',
        ),
        migrations.DeleteModel(
            name='QueueEntry',
        ),
        migrations.AddField(
            model_name='service',
            name='staff_members',
            field=models.ManyToManyField(limit_choices_to={'profile__role': 'staff'}, related_name='services_offered', to=settings.AUTH_USER_MODEL),
        ),
    ]
