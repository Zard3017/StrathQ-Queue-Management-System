from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Service, Queue, Notification, Student, Staff
from .decorators import student_required, staff_required


def signup(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
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


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            student = Student.objects.get(student_id=username)
            if student.password == password:
                request.session.flush()
                request.session['user_id'] = student.id
                request.session['role'] = 'student'
                return redirect('student')
        except Student.DoesNotExist:
            pass

        try:
            staff = Staff.objects.get(staff_id=username)
            if staff.password == password:
                request.session.flush()
                request.session['user_id'] = staff.id
                request.session['role'] = 'staff'
                return redirect('staff')
        except Staff.DoesNotExist:
            pass

        messages.error(request, 'Invalid credentials. Please try again.')
        return redirect('login')

    return render(request, 'login.html')


def student(request):
    if request.session.get('role') != 'student':
        return redirect('login')

    student_id = request.session.get('user_id')
    student = get_object_or_404(Student, id=student_id)

    return render(request, 'student.html', {'student': student})


def staff(request):
    if request.session.get('role') != 'staff':
        return redirect('login')

    staff_id = request.session.get('user_id')
    staff = get_object_or_404(Staff, id=staff_id)
    department_services = Service.objects.filter(department=staff.department)
    queues = Queue.objects.filter(service__in=department_services, status='active').order_by('joined_at')

    # Attach position and student info
    for queue in queues:
        all_queues = Queue.objects.filter(service=queue.service, status='active').order_by('joined_at')
        queue.position = list(all_queues).index(queue) + 1
        queue.student_name = f"{queue.student.first_name} {queue.student.last_name}"

    context = {
        'staff': staff,
        'services': department_services,
        'queues': queues,
    }
    return render(request, 'staff.html', context)



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



def update_queue_status(request, queue_id, new_status):
    queue = get_object_or_404(Queue, id=queue_id)
    if new_status == 'completed':
        queue.status = 'completed'
        queue.served_at = timezone.now()
    elif new_status == 'removed':
        queue.status = 'removed'
    queue.save()
    return redirect('staff')


def unauthorized(request):
    messages.error(request, 'You are not authorized to view this page.')
    return redirect('login')


def admin(request):
    if request.user.profile.role != 'admin':
        return redirect('login')
    return render(request, 'admin.html')


def logout_view(request):
    request.session.flush()  # Clears all session data
    return redirect('login')

def join_queue(request):
    if request.session.get('role') != 'student':
        return redirect('login')
    selected_department = request.GET.get('department')
    selected_service = request.GET.get('service')

    services = Service.objects.all()
    admin_online_staff = Staff.objects.filter(department='Administration', status='online') if selected_department == 'Administration' else []
    sces_online_staff = Staff.objects.filter(department='SCES Helpdesk', status='online') if selected_department == 'SCES Helpdesk' else []
    lecturer_online_staff = Staff.objects.filter(department='Lecturer Consultation', status='online') if selected_department == 'Lecturer Consultation' else []


    context = {
        'services': services,
        'selected_department': selected_department,
        'selected_service': selected_service,
        'admin_online_staff': admin_online_staff,
        'sces_online_staff': sces_online_staff,
        'lecturer_online_staff': lecturer_online_staff
    }
    return render(request, 'join_queue.html', context)


def my_queues(request):
    if request.session.get('role') != 'student':
        return redirect('login')

    student_id = request.session.get('user_id')
    student = get_object_or_404(Student, id=student_id)
    current_queues = Queue.objects.filter(student=student, status='active').order_by('joined_at')
    past_queues = Queue.objects.filter(student=student).exclude(status='active').order_by('-joined_at')

    for queue in current_queues:
        all_in_queue = Queue.objects.filter(service=queue.service, status='active').order_by('joined_at')
        position = list(all_in_queue).index(queue) + 1
        queue.position = position
        queue.total = all_in_queue.count()
        queue.estimated_wait = (position - 1) * 2

    return render(request, 'my_queues.html', {
        'current_queues': current_queues,
        'past_queues': past_queues,
    })


def get_staff_by_service(request, service_id):
    if request.method == 'GET':
        staff_list = Staff.objects.filter(service_id=service_id)
        data = [{
            'id': staff.id,
            'name': f"{staff.first_name} {staff.last_name}",
            'status': staff.status,
        } for staff in staff_list]
        return JsonResponse({'staff': data})



def leave_queue(request, queue_id):
    if request.session.get('role') != 'student':
        return redirect('login')

    student_id = request.session.get('user_id')
    student = get_object_or_404(Student, id=student_id)
    
    queue = get_object_or_404(Queue, id=queue_id, student=student)
    queue.delete()
    
    return redirect('my_queues')

def position_in_queue(self):
    if self.status != 'active':
        return None
    same_service_queues = Queue.objects.filter(service=self.service, status='active').order_by('joined_at')
    return list(same_service_queues).index(self) + 1


def toggle_availability(request):
    if request.method == 'POST':
        staff_id = request.session.get('user_id')
        staff = get_object_or_404(Staff, id=staff_id)
        department = request.POST.get('department')
        if department:
            staff.department = department
        staff.is_available = not staff.is_available
        staff.save()
    return redirect('staff')


def update_staff_services(request):
    if request.method == "POST":
        staff = get_object_or_404(Staff, pk=request.POST.get("staff_id"))
        selected_services = request.POST.getlist("services")
        services = Service.objects.filter(id__in=selected_services)
        staff.services_offered.set(services)
        return redirect('staff')


def get_online_staff_for_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    staff_list = Staff.objects.filter(department=service.department, status='online')
    return render(request, 'partials/staff_dropdown.html', {'staff_list': staff_list})


def update_status(request):
    if request.method == 'POST':
        staff_id = request.POST.get('staff_id')
        new_status = request.POST.get('status')
        staff = Staff.objects.filter(id=staff_id).first()
        if staff:
            staff.status = new_status
            staff.save()
    return redirect('staff')



def enqueue(request):
    if request.session.get('role') != 'student':
        return redirect('login') 

    if request.method == 'POST':
        student_id = request.session.get('user_id')
        service_name = request.POST.get('service')
        staff_id = request.POST.get('staff_id')
        
        if not all([student_id, service_name, staff_id]):
            messages.error(request, "Missing information. Please try again.")
            return redirect('join_queue')

        student = get_object_or_404(Student, id=student_id)
        staff = get_object_or_404(Staff, id=staff_id)
        service = get_object_or_404(Service, name=service_name)

        already_queued = Queue.objects.filter(student=student, service=service, status='waiting').exists()
        if already_queued:
            messages.warning(request, "You're already in the queue for this service.")
            return redirect('join_queue')

        Queue.objects.create(
            student=student,
            service=service,
            assigned_staff=staff,
        )

        messages.success(request, f"You have joined the queue for {service.name} with {staff.first_name}.")
        return redirect('my_queues')

    return redirect('join_queue')
