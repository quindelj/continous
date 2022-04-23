from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register_user', views.register_user, name='register_user'),
    #path('login_user', views.index, name = 'login_user'),
    path('login_user', views.login_user, name='login_user'),
    path('logout', views.logout),

    path('home', views.home, name='home'),
    path('teacher', views.teacher),
    path('student', views.student),
    path('parent', views.parent),

    path('create_course', views.create_course),
    path('view_course', views.view_course),
]