#Admin.py
from django.contrib import admin
from.models import Student, Staff, Service, Queue, Notification

admin.site.register(Student)
admin.site.register(Staff)
admin.site.register(Service)
admin.site.register(Queue)
admin.site.register(Notification)


# Register your models here.
