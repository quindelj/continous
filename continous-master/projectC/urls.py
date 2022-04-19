from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.index),
    path('logout', views.logout),

    path('home', views.home),
    path('teacher', views.teacher),
    path('student', views.student),
    path('parent', views.parent),
]