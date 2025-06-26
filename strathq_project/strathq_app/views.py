from django.shortcuts import render

# Create your views here.
def login_view(request):
    return render(request, 'login.html')

def signup_view(request):
    return render(request, 'signup.html')

def student_view(request):
    return render(request, 'student.html')

def my_queues_view(request):
    return render(request, 'my_queues.html')

def join_queue_view(request):
    return render(request, 'join_queue.html')

def role_selection_view(request):
    return render(request, 'role_selection.html')
def staff_view(request):
    return render(request, 'staff.html')

def admin_view(request):
    return render(request, 'admin.html')


