from django.shortcuts import redirect

def student_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.session.get('role') != 'student':
            return redirect('unauthorized')
        return view_func(request, *args, **kwargs)
    return wrapper

def staff_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.session.get('role') != 'staff':
            return redirect('unauthorized')
        return view_func(request, *args, **kwargs)
    return wrapper
