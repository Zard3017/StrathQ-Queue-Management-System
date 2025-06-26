from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('student/', views.student_view, name='student'),
    path('join_queue/', views.join_queue_view, name='join_queue'),
    path('my_queues/', views.my_queues_view, name='my_queues'),
    path('staff/', views.staff_view, name='staff'),
   
    path('admin/', views.admin_view, name='admin'),

]