from django.shortcuts import render, redirect

from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login

# Create your views here.
def login(request):
    if request.method == 'POST':
        # Get the username and password from the form
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user against the database
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # User is authenticated, redirect to the student page
            return redirect('student')
        else:
            # User is not authenticated, display an error message
            messages.error(request, 'Invalid username or password')
            return redirect('login')
    else:
        return render(request, 'login.html')

   
def signup(request):
    if request.method == 'POST':
        # Get the user data from the form
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        #Validation
        if not username or not email or not password:
            messages.error(request, 'All fields are required.')
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('signup')
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, 'Account created successfully.')
            return redirect('login')
        except Exception as e:
            messages.error(request, 'An error occurred while creating the account.')
            return redirect('signup')

        
    return render(request, 'signup.html')

def student(request):
    return render(request, 'student.html')

def join_queue(request):
    return render(request, 'join_queue.html')

def my_queues(request):
    return render(request, 'my_queues.html')

def staff(request):
    return render(request, 'staff.html')

def admin(request):
    return render(request, 'admin.html')
