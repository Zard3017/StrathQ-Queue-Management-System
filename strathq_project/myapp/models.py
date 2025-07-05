from django.db import models

class Student(models.Model):
    student_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)  # In production, store hashed passwords

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.student_id})"


class Staff(models.Model):
    staff_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.staff_id})"


class Service(models.Model):
    DEPARTMENT_CHOICES = [
        ('SCES Helpdesk', 'SCES Helpdesk'),
        ('Administration', 'Administration'),
        ('Lecturer Consultation', 'Lecturer Consultation'),
        
    ]

    name = models.CharField(max_length=100)
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)
    staff_members = models.ManyToManyField(Staff, related_name='services_offered')

    def __str__(self):
        return f"{self.name} ({self.department})"



class Queue(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('left', 'Left'),
    )

    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='queue_tickets')
    assigned_staff = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tickets')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    joined_at = models.DateTimeField(auto_now_add=True)
    served_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.service.name} - {self.student.first_name} ({self.get_status_display()})"


class Notification(models.Model):
    recipient_student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)
    recipient_staff = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True, blank=True)
    message = models.CharField(max_length=255)
    sent_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        recipient = self.recipient_student or self.recipient_staff
        return f"To: {recipient} - {self.message[:30]}..."
