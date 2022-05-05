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
        # form used to create input fileds in html template
        form = TeacherForm(request.POST)
        if form.is_valid():
            # takes valid form data and creates a new Teacher
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # authenticate the user password and username is correct and logs the user in
            user = authenticate(username=username, password=password)
            login(request,user)
            messages.success(request,'You have successfully registured!')
            return redirect('/home')
    else:
        form = TeacherForm()
    return render(request, 'authenticate/teacher_reg.html', {'form' : form})

def register_student(request):
    if request.method == 'POST':
        # form used to create input fileds in html template
        form = StudentForm(request.POST)
        if form.is_valid():
            # takes valid form data and creates a new Teacher
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # authenticate the user password and username is correct and logs the user in
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
        # takes user POST data and authenatcte it to login user
        username = request.POST ['username']
        password = request.POST ['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['user_id'] = user.id
            messages.info(request, f"You are now logged in as {username}.")
            return redirect("home")
        else:
            # If authenicatation fail retuns error message
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
    return redirect('/')

@login_required
def home(request):
    if request.user.is_authenticated:
        user = request.user
        course = Course.objects.all();
        #teacher = request.session['user_id'] = User.id

    '''if 'user_id' not in request.session:
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

@login_required
def teacher(request):
    user = User.objects.get(id = request.session['user_id'])
    return render (request, 'TeacherHome.html')

@login_required
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
@login_required
def create_course(request):
    submitted = False
    # Course form used to create input fileds in html template
    form =CreateCourseForm(request.POST or None)
    context = {
        'form':form
    }
    if request.method == 'POST':
        if form.is_valid():
            # assigns variables to the post data
            title = form.cleaned_data.get('title')
            descrption = form.cleaned_data.get('descrption')
            teacher = form.cleaned_data.get('teacher')
            students = form.cleaned_data.get('student')
            try:
                # attemps to create a new Course based on variables above
                course = Course()
                course.title = title
                course.descrption = descrption
                course.teacher = teacher
                course.save()
                # loops through the Students and retun select students
                course.student.set(students)
                # saves the course
                course.save()
                messages.success(request, 'Course created')
                return HttpResponseRedirect('/create_course?submitted=True')
            except Exception as e:
                #returns exception error
                messages.error(request, str(e))
        else:
            messages.error(request, 'Error try again')
            '''form = CreateCourseForm()
            if 'submitted' in request.GET:
                submitted = True'''
    return render(request, 'create_course.html', context)

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
    teacher_courses = Course.objects.filter(teacher=request.user)
    course_add = Course.objects.get(id=course_id)
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