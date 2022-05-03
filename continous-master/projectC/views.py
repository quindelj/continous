from django.shortcuts import get_object_or_404, render, redirect
from .models import *
from django.contrib import messages
from .forms import CreateCourseForm,TeacherForm, StudentForm, AddStudentForm
from django.contrib.auth import authenticate, login, logout,get_user_model
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

# Create your views here.
User = get_user_model

def index(request):
    return render (request, 'index.html')

def register(request):
    return render(request, 'register.html')

def register_teacher(request):
    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request,user)
            messages.success(request,'You have successfully registured!')
            return redirect('/home')
    else:
        form = TeacherForm()
    return render(request, 'authenticate/teacher_reg.html', {'form' : form})

def register_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request,user)
            request.session['user_id'] = user.id
            messages.success(request,'You have successfully registured!')
            return redirect('/home')
    else:
        form = StudentForm()
    return render(request, 'authenticate/student_reg.html', {'form' : form})


def login_user(request):
    if request.method == "POST":
        username = request.POST ['username']
        password = request.POST ['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['user_id'] = user.id
            messages.info(request, f"You are now logged in as {username}.")
            return redirect("home")
        else:
            messages.error(request,"Invalid username or password.")
            return redirect('login_user')
    else:
        '''
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
        course = Course.objects.all();
        #teacher = request.session['user_id'] = User.id

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
    return render (request, 'home.html', {'course':course})

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
def create_course(request):
    submitted = False
    form =CreateCourseForm(request.POST or None)
    context = {
        'form':form
    }
    if request.method == 'POST':
        if form.is_valid():
            title = form.cleaned_data.get('name')
            descrption = form.cleaned_data.get('descrption')
            teacher = form.cleaned_data.get('teacher')
            student = form.cleaned_data.get('student')
            try:
                course = Course()
                course.title = title
                course.descrption = descrption
                course.teacher = teacher
                course.student =student
                course.save()
                messages.success(request, 'Course created')
                return HttpResponseRedirect('/create_course?submitted=True')
            except Exception as e:
                messages.error(request, 'Error' + str(e))
        else:
            messages.error(request, 'Error try again')
            '''form = CreateCourseForm()
            if 'submitted' in request.GET:
                submitted = True'''
    return render(request, 'create_course.html', context)


    '''submitted = False
    teacher = Teacher.objects.all()
    student = Student.objects.all()
    #print (teacher, student)
    #for student in students:

    if request.method == 'POST':
        form = CreateCourseForm(request.POST)
        if form.is_valid():
            
            #course = Course.objects.create() 
            #student.course.add(course) 
            form.save()
            student.course.add()
            return HttpResponseRedirect('/create_course?submitted=True')
    else:
        form = CreateCourseForm()
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'create_course.html', {'form' : form, 'submitted': submitted, 'teacher': teacher, 'student':student})''' 

def view_course(request, id):
    course = Course.objects.get(id=id)
    teacher = Teacher.objects.filter(course_teacher = course)
    student = Student.objects.filter(course = course)
    
    print(student, teacher)
    return render(request, 'view_course.html',{'course': course, 'teacher': teacher, 'student':student})   

def take_attdance(request):

    return render(request, '/' )

def report_behavior(request):

    return redirect('/')

def record_grades(request):

    return redirect('/')

def add_student(request, course_id):
    submitted = False
    course_add = Course.objects.filter(id=course_id)
    students = Student.objects.all()

    if request.method == 'POST':
        form = AddStudentForm(request.POST)
        if form.is_valid():
            for student in students:
                    student.course  = course_add
            form.save()
            return HttpResponseRedirect('/add_student?submitted=True')
    else:
        form = AddStudentForm()
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'add_student.html', {'form' : form, 'submitted': submitted,}) 

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