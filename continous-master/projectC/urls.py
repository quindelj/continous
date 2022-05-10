from django.urls import path
from . import views
from django.urls import path
#from django.contrib.atuh import views as auth_views


urlpatterns = [
    path('', views.index),
    path('register', views.register, name='register_user'),
    path('register_teacher', views.register_teacher, name='register_teacher'),
    path('register_student', views.register_student, name='register_student'),
    #path('login_user', views.index, name = 'login_user'),
    path('login_user', views.login_user, name='login_user'),
    path('logout_user', views.logout_user, name='logout_user'), 

    path('home', views.home, name='home'),
    path('teacher', views.teacher),
    path('student', views.student),
    #path('parent', views.parent),

    # teacher
    path('create_course', views.create_course),
    path('view_course/<int:course_id>', views.view_course),
    path('add_student/<int:course_id>', views.add_student),
    path('attendance/<int:course_id>', views.attendance),
    path('take_attendance/<int:course_id>/<str:date>', views.take_attendance, name='attendance-page'),
    path('report_behavior', views.report_behavior),
    
    path('data_report/<int:course_id>', views.view_data),

    #student
    path('view_behavior/<int:student_id>', views.view_behavior),
    path('view_attendance/<int:student_id>', views.view_attendance),
]