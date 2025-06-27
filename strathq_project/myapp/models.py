from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.

class Profile(models.Model):
    """
    Extends Django's built-in User model to add a role.
    This single model replaces the need for separate Student, Staff, and Admin models.
    """
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('staff', 'Staff'),
        ('admin', 'Admin'),
    )
    # Creates a one-to-one link with a User. If a User is deleted, their Profile is also deleted.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')

    def __str__(self):
        # The User model already has username, email, first_name, last_name.
        return f'{self.user.username} - {self.get_role_display()}'


class Service(models.Model):
    # Let Django handle the primary key automatically.
    name = models.CharField(max_length=100)
    # A service can be managed by a staff member.
    # limit_choices_to ensures you can only select users with the 'staff' role.
    managed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'profile__role': 'staff'})

    def __str__(self):
        return self.name


class Queue(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('left', 'Left'),
    )
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    # A single foreign key to the User model is much cleaner.
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    joined_at = models.DateTimeField(auto_now_add=True) # Automatically set when the queue is created.
    served_at = models.DateTimeField(null=True, blank=True) # Can be set when the student is served.

    def __str__(self):
        return f"{self.service.name} - {self.student.username} ({self.get_status_display()})"


class Notification(models.Model):
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    sent_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"To: {self.recipient.username} - {self.message[:30]}..."
