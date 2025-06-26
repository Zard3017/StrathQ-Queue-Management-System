from django.shortcuts import render

# Create your views here.
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        return render(request, 'role_selection.html', {'username': username, 'password': password})
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
