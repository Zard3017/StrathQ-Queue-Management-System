from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from .models import Service, Queue, Notification
from .models import Queue
from .models import Student, Staff



def signup(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')  # This is student_id or staff_id
        password = request.POST.get('password')
        role = request.POST.get('role')

        if role == 'student':
            if Student.objects.filter(student_id=username).exists():
                messages.error(request, "Student ID already registered.")
                return redirect('signup')
            Student.objects.create(
                student_id=username,
                first_name=first_name,
                last_name=last_name,
                password=password
            )

        elif role == 'staff':
            if Staff.objects.filter(staff_id=username).exists():
                messages.error(request, "Staff ID already registered.")
                return redirect('signup')
            Staff.objects.create(
                staff_id=username,
                first_name=first_name,
                last_name=last_name,
                password=password
            )

        else:
            messages.error(request, "Invalid role selected.")
            return redirect('signup')

        messages.success(request, "Account created successfully.")
        return redirect('login')

    return render(request, 'signup.html')

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .models import Student, Staff  # Import your role models if needed

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Check Student first
        try:
            student = Student.objects.get(student_id=username)
            if student.password == password:  # In production, hash and compare
                request.session['user_id'] = student.id
                request.session['role'] = 'student'
                return redirect('student')
        except Student.DoesNotExist:
            pass

        # Then check Staff
        try:
            staff = Staff.objects.get(staff_id=username)
            if staff.password == password:
                request.session['user_id'] = staff.id
                request.session['role'] = 'staff'
                return redirect('staff')
        except Staff.DoesNotExist:
            pass

        messages.error(request, 'Invalid credentials.')
        return redirect('login')

    return render(request, 'login.html')



def student(request):
    if request.session.get('role') != 'student':
        return redirect('login')

    student_id = request.session.get('user_id')
    student = get_object_or_404(Student, id=student_id)

    return render(request, 'student.html', {'student': student})


def get_queue_status(request):
    if request.session.get('role') != 'student':
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    student_id = request.session.get('user_id')
    student = get_object_or_404(Student, id=student_id)

    try:
        queue = Queue.objects.get(student=student, status='active')
    except Queue.DoesNotExist:
        return JsonResponse({'error': 'Not in queue'}, status=404)

    all_queues = Queue.objects.filter(service=queue.service, status='active').order_by('joined_at')
    position = list(all_queues).index(queue) + 1
    total = all_queues.count()

    estimated_wait = (position - 1) * 2

    return JsonResponse({
        'position': position,
        'total': total,
        'estimated_wait': f"{estimated_wait} minutes"
    })


def staff(request):
    if request.session.get('role') != 'staff':
        return redirect('login')

    staff_id = request.session.get('user_id')
    staff = get_object_or_404(Staff, id=staff_id)

    return render(request, 'staff.html', {'staff': staff})
  

def update_queue_status(request, queue_id, status):
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'staff':
        return redirect('login')
    queue = get_object_or_404(Queue, id=queue_id)
    if queue.service.managed_by != request.user:
        return redirect('staff')
    if status in ['completed', 'left']:
        queue.status = status
        queue.served_at = timezone.now()
        queue.save()
        messages.success(request, f'Queue status updated to {status}.')
    return redirect('staff')

def unauthorized(request):
    messages.error(request, 'You are not authorized to view this page.')
    return redirect('login')


def admin(request):
    if request.user.profile.role != 'admin':
        return redirect('login')
    return render(request, 'admin.html')

def logout_view(request):
    logout(request)
    return redirect('login')


def join_queue(request):
    departments = ['SCES Helpdesk', 'Administration', 'Lecturer Consultation']
    services_by_department = {
        dept: Service.objects.filter(department=dept).prefetch_related('staff_members') for dept in departments
    }
    return render(request, 'join_queue.html', {'services_by_department': services_by_department})

def my_queues(request):
    if request.session.get('role') != 'student':
        return redirect('login')

    student_id = request.session.get('user_id')
    student = get_object_or_404(Student, id=student_id)

    # Active queues for the student
    current_queues = Queue.objects.filter(student=student, status='active').order_by('joined_at')

    # Past queues (completed or left)
    past_queues = Queue.objects.filter(student=student).exclude(status='active').order_by('-joined_at')

    # Add dynamic fields to current_queues
    for queue in current_queues:
        all_in_queue = Queue.objects.filter(service=queue.service, status='active').order_by('joined_at')
        position = list(all_in_queue).index(queue) + 1
        queue.position = position
        queue.total = all_in_queue.count()
        queue.estimated_wait = (position - 1) * 2  # assuming 2 min per person

    return render(request, 'my_queues.html', {
        'current_queues': current_queues,
        'past_queues': past_queues,
    })


def get_staff_by_service(request, service_id):
    if request.method == 'GET':
        staff_list = Staff.objects.filter(service_id=service_id)
        data = []

        for staff in staff_list:
            data.append({
                'id': staff.id,
                'name': f"{staff.first_name} {staff.last_name}",
                'status': staff.status,  # assume 'online' or 'unavailable'
            })

        return JsonResponse({'staff': data})
def leave_queue(request, queue_id):
    if request.session.get('role') != 'student':
        return redirect('login')

    student_id = request.session.get('user_id')
    queue = get_object_or_404(Queue, id=queue_id, student_id=student_id, status='active')

    queue.status = 'left'
    queue.save()
    return redirect('my_queues')
def position_in_queue(self):
    if self.status != 'active':
        return None
    same_service_queues = Queue.objects.filter(service=self.service, status='active').order_by('joined_at')
    return list(same_service_queues).index(self) + 1
def toggle_availability(request):
    if request.session.get('role') != 'staff':
        return redirect('login')

    staff_id = request.session.get('user_id')
    staff = get_object_or_404(Staff, id=staff_id)

    # Toggle availability
    staff.is_available = not staff.is_available
    staff.save()

    return redirect('staff')