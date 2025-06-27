from django.shortcuts import render, redirect
from django.shortcuts import authenticate
from django.contrib import messages

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
