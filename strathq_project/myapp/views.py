from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import SignupForm
from .models import Profile

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
def staff(request):
    if request.user.profile.role != 'staff':
        return redirect('login')
    return render(request, 'staff.html')

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
    
     return render(request, 'join_queue.html', )
         

@login_required
def my_queues(request):
    return render(request, 'my_queues.html')
