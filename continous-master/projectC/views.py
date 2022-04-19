from curses.ascii import US
from email import message
from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from .forms import SignUpForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

# Create your views here.
def index(request):
    return render (request, 'index.html')

def register(request):
    msg = messages
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request,'You have successfully registured!')
            return redirect('/home')
        else:
            messages.error(request,'An error occured please try again')
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form' : form, 'msg' : msg})

def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
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
    form = AuthenticationForm()
    return render(request=request, template_name="index.html", context={"login_form":form})

    
    #return render(request, 'home.html', {'form' : form, 'msg' : msg})

    #orm = LoginForm()
    
    
    #messages.success(request,"You have successfully logged in!")
    #return render(request, 'index.html', {'form' : form, 'msg' : msg})

def logout(request):
    logout(request)
    messages.info(request, "You have successfully logged out.") 
    request.session.clear()
    return redirect('/login')


"""

    def login(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username = username, password = password)
            if user is not None and User.isTeacher:
                login(request, user)
                return redirect('teacher')
            elif user is not None and User.isStudent:
                login(request, user)
                return redirect('student')
            elif user is not None and User.isParent:
                login(request, user)
                return redirect('parent')
            else:
                msg = 'Password or Email don\'t match'
        else:
            msg = 'An error occured while valadating'
    return render(request, 'login.html', {'form' : form, 'msg' : msg})"""

@login_required
def home(request):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.get(id = request.session['user_id'])
    return render (request, 'home.html')

@login_required
def teacher(request):
    if 'user_id' not in request.session:
        return redirect('/')
    if 'user_id' is User.isTeacher:
        return redirect('/teacher')
    elif 'user_id' is User.isParent:
        return redirect('/parent')
    user = User.objects.get(id = request.session['user_id'])
    return render (request, 'TeacherHome.html')

@login_required
def student(request):
    if 'user_id' not in request.session:
        return redirect('/')
    if 'user_id' is User.isTeacher:
        return redirect('/teacher')
    elif 'user_id' is User.isParent:
        return redirect('/parent')
    else:
        user = User.objects.get(id = request.session['user_id'])
        return render (request, 'studentHome.html')
        

@login_required
def parent(request):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.get(id = request.session['user_id'])
    return render (request, 'parentHome.html')
