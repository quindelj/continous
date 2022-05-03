from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register, name='register_user'),
    path('register_teacher', views.register_teacher, name='register_teacher'),
    path('register_student', views.register_student, name='register_student'),
    #path('login_user', views.index, name = 'login_user'),
    path('login_user', views.login_user, name='login_user'),
    path('logout', views.logout),

    path('home', views.home, name='home'),
    path('teacher', views.teacher),
    path('student', views.student),
    path('parent', views.parent),

    path('create_course', views.create_course),
    path('view_course/<int:id>', views.view_course),
    path('add_student/<int:course_id>', views.add_student),
]