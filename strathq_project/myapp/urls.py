from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('signup/', views.signup, name='signup'),
    path('student/', views.student, name='student'),
    path('join_queue/', views.join_queue, name='join_queue'),
    path('my_queues/', views.my_queues, name='my_queues'),
    path('staff/', views.staff, name='staff'),
    path('admin/', views.admin, name='admin'),
    path('logout/', views.logout_view, name='logout'),
    
]