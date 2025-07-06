from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('signup/', views.signup, name='signup'),
    path('student/', views.student, name='student'),
    path('join_queue/', views.join_queue, name='join_queue'),
    path('my_queues/', views.my_queues, name='my_queues'),
    path('staff/', views.staff, name='staff'),
    path('staff/queue/<int:queue_id>/<str:status>/', views.update_queue_status, name='update_queue_status'),
    path('unauthorized/', views.unauthorized, name='unauthorized'),
    path('admin/', views.admin, name='admin'),
    path('logout/', views.logout_view, name='logout'),
    path('queue_status/', views.get_queue_status, name='queue_status'),
    path('toggle_availability/', views.toggle_availability, name='toggle_availability'),
    path('api/staff/<int:service_id>/', views.get_staff_by_service, name='get_staff_by_service'),
    path('staff/update-services/', views.update_staff_services, name='update_staff_services'),
    path('update_status/', views.update_status, name='update_status'),
    path('enqueue/', views.enqueue, name='enqueue'),
    path('leave_queue/<int:queue_id>/', views.leave_queue, name='leave_queue'),
    path('queue/update/<int:queue_id>/<str:new_status>/', views.update_queue_status, name='update_queue_status'),
    path('reports/', reports_view, name='reports')
    
    
]