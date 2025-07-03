from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import SignupForm
from .models import Profile
from .models import Service, Queue, Notification
from .models import QueueEntry

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        role = request.POST['role']  # from the role dropdown in the form

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('signup')

        # Create the user with password hashing
        user = User.objects.create_user(username=username, password=password)

        # Create associated profile with the selected role
        Profile.objects.create(user=user, role=role)

        messages.success(request, f'Successfully registered as {role}. You can now log in.')
        return redirect('login')

    return render(request, 'signup.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            role = user.profile.role
            if role == 'student':
                return redirect('student')
            elif role == 'staff':
                return redirect('staff')
            elif role == 'admin':
                return redirect('admin')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

@login_required
def student(request):
    if request.user.profile.role != 'student':
        return redirect('login')
    return render(request, 'student.html')

@login_required
def get_queue_status(request):
    if request.user.profile.role != 'student':
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    try:
        queue = Queue.objects.get(student=request.user, status='active')
    except Queue.DoesNotExist:
        return JsonResponse({'error': 'Not in queue'}, status=404)

    all_queues = Queue.objects.filter(service=queue.service, status='active').order_by('joined_at')
    position = list(all_queues).index(queue) + 1
    total = all_queues.count()

    # Simple estimate: 2 minutes per student
    estimated_wait = (position - 1) * 2

    return JsonResponse({
        'position': position,
        'total': total,
        'estimated_wait': f"{estimated_wait} minutes"
    })

@login_required
def staff(request):
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'staff':
        return redirect('login')
    return render(request, 'staff.html')
    services = Service.objects.filter(managed_by=request.user)
    queues = Queue.objects.filter(service__in=services).select_related('student', 'service')
    Notifications = Notification.objects.filter(user=request.user).order_by('-timestamp')
    context = {
        'services': services,
        'queues': queues,
    }
    return render(request, 'staff.html', context)

@login_required
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

@login_required
def admin(request):
    if request.user.profile.role != 'admin':
        return redirect('login')
    return render(request, 'admin.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def join_queue(request):
    if request.method == 'POST':
        department = request.POST['department']
        service = request.POST['service']
        QueueEntry.objects.create(user=request.user, department=department, service=service)
        return redirect('my_queues')
    else:
        return redirect('join_queues')

@login_required
def my_queues(request):
    current_queues = QueueEntry.objects.filter(user=request.user, status='waiting')
    past_queues = QueueEntry.objects.filter(user=request.user).exclude(status='waiting')

    # Calculate position for each current queue
    for q in current_queues:
        q.position = q.position_in_queue()

    return render(request, 'my_queues.html', {
        'current_queues': current_queues,
        'past_queues': past_queues,
    })

@login_required
def leave_queue(request, queue_id):
    queue = get_object_or_404(QueueEntry, id=queue_id, user=request.user)
    queue.status = 'left'
    queue.save()
    return redirect('my_queues')

