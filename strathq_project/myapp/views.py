from django.shortcuts import render, redirect

from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login , logout
from .forms import SignupForm
from django.contrib.auth.decorators import login_required
from .models import Profile

# Create your views here.


   
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            role= user.profile.role
            if role == 'student':
                return redirect('student')
            elif role == 'staff':
                return redirect('staff')
            elif role == 'admin':
                return redirect('admin')
            else:
                return redirect('login')
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'login.html')
    @login_required
    def student(request):
        if request.user.profile.role != 'student':
            return redirect('login')
        else:
            return render(request, 'student.html')
    @login_required
    def staff(request):
        if request.user.profile.role != 'staff':
            return redirect('login')
        else:
            return render(request, 'staff.html')
    def logout_view(request):
        logout(request)
        return redirect('login')
    return render(request, 'login.html')



def student(request):
    return render(request, 'student.html')

def staff(request):
    return render(request, 'staff.html')

def admin(request):
    return render(request, 'admin.html')

def logout_view(request):
    logout(request)
    return redirect('login')
def join_queue(request):
    return render(request, 'join_queue.html')

def my_queues(request):
    return render(request, 'my_queues.html')

