from cmath import log
from curses.ascii import US
from email import message
from urllib import request
from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from .forms import SignUpForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

# Create your views here.
def index(request):
    return render (request, 'index.html')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            login(request,user)
            messages.success(request,'You have successfully registured!')
            return redirect('/home')
    else:
        form = SignUpForm()
    '''if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request,'You have successfully registured!')
            return redirect('/home')
        else:
            messages.error(request,'An error occured please try again')
    else:
        form = SignUpForm()'''
    return render(request, 'authenticate/register.html', {'form' : form})

def login_user(request):
    if request.method == "POST":
        username = request.POST ['username']
        password = request.POST ['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['user_id'] = user.id
            print(username + password)

            messages.info(request, f"You are now logged in as {username}.")
            return redirect("home")
        else:
            messages.error(request,"Invalid username or password.")
            return redirect('login_user')
    else:
        '''form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("/home")
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
    form = AuthenticationForm()'''
    return render(request, 'authenticate/login.html', context={})


def logout_user(request):
    logout(request)
    messages.info(request, "You have successfully logged out.") 
    request.session.clear()
    return redirect('/login')

#@login_required
def home(request):
    if request.user.is_authenticated:
        '''if request.user.isTeacher:
            return redirect('teacher')
        elif request.user.isStudent:
            return redirect('student')
        else:
            return redirect('parent')
        

    if 'user_id' not in request.session:
        return redirect('/login_user')
    if User.isTeacher == True:
        return redirect('/teacher')
    elif User.isParent == True:
        return redirect('/parent')
    elif User.isStudent == True:
        return redirect('student')
    else:
        user = User.objects.get(id = request.session['user_id'])'''
    return render (request, 'home.html')

#@login_required
def teacher(request):
    if 'user_id' not in request.session:
        return redirect('/login_user')
    user = User.objects.get(id = request.session['user_id'])
    return render (request, 'TeacherHome.html')

#@login_required
def student(request):
    if 'user_id' not in request.session:
        return redirect('/login_user')
    user = User.objects.get(id = request.session['user_id'])
    return render (request, 'studentHome.html')
        

#@login_required
def parent(request):
    if 'user_id' not in request.session:
        return redirect('/login_user')
    user = User.objects.get(id = request.session['user_id'])
    return render (request, 'parentHome.html')

#teacher options
def create_course(resuest):
    Course.objects.create(
        title = request.POST['title'],
        descrption = request.POST['description'],
        teacher  = User.objects.get(id = request.session['user_id'])
    )
    messages.info(request, "Course created")
    return redirect('/teacher')   

def take_attdance(request):

    return render(request, '/' )

def report_behavior(request):

    return redirect('/')

def record_grades(request):

    return redirect('/')

def add_student(request):

    return redirect ('/')

def drop_student(request):

    return redirect('/')

#student options
def join_course(request):

    return redirect('/')

def drop_course(request):

    return redirect('/')

def view_grades(request):

    return redirect('/')

def view_behavior(request):

    return redirect('/')