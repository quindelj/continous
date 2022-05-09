from datetime import datetime
from multiprocessing import context
from urllib import response
from webbrowser import get
from django.shortcuts import get_object_or_404, render, redirect
from .models import *
from django.contrib import messages
from .forms import BehaviorForm, CreateCourseForm, TakeAttendanceForm,TeacherForm, StudentForm, AddStudentForm, AttendanceFormset
from django.contrib.auth import authenticate, login, logout,get_user_model
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
import json

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
            #request.session['user_id'] = user.id
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
            if user.type == 'TEACHER':
                messages.info(request, f"You are now logged in as {user.first_name}.")
                return redirect('/teacher')

            else: 
                user.type == 'STUDENT'
                messages.info(request, f"You are now logged in as {user.first_name}.")

            return redirect ('/student')
            #messages.info(request, f"You are now logged in as {user.first_name}.")
            #return redirect("home")
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
        user=request.user
        course = Course.objects.all()
        if user.isTeacher:
            messages.info(request, f"You are now logged in as {user.first_name}.")
            return redirect('/teacher')
        else: 
            user.isStudent
            messages.info(request, f"You are now logged in as {user.first_name}.")
        return redirect ('/student')

    return render (request, 'home.html', {'course':course})

@login_required
def teacher(request):
    user=request.user
    course = Course.objects.all()
    #user = User.objects.get(id = request.session['user_id'])
    return render (request, 'TeacherHome.html',{'course':course})

@login_required
def student(request):
    user=request.user
    course = Course.objects.all()
    return render (request, 'studentHome.html',{'course':course})


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
                return HttpResponseRedirect('/create_course/course.id')
            except Exception as e:
                #returns exception error
                messages.error(request, str(e))
        else:
            form = CreateCourseForm()
            if 'submitted' in request.GET:
                submitted = True
            messages.error(request, 'Error try again')

    return render(request, 'create_course.html', context,)

def view_course(request, course_id):
    #course_id= Course.objects.get(id=course_id)
    #student_id = Student.objects.get(id=id)
    course_id = get_object_or_404(Course, id = course_id)
    teacher = Teacher.objects.filter(course_teacher = course_id)
    student = Student.objects.filter(course_student = course_id)
    attendance = Attendance.objects.filter(course = course_id)
    behavior = Behavior.objects.all()

    print(student, teacher,attendance,behavior)
    return render(request, 'view_course.html',{'course': course_id, 'teacher': teacher, 'student':student, 'behavior':behavior})   

def attendance(request, course_id, date = None):
    course_id = get_object_or_404(Course, id = course_id)
    teacher = Teacher.objects.filter(course_teacher = course_id)
    students = Student.objects.filter(course_student = course_id)
    #form = TakeAttendanceForm(request.POST or None)
    #context['course'] = course_id
    #context['date'] = date

    attendance_data = {}
    for student in students:
        attendance_data[student.id] = {}
        attendance_data[student.id]['data'] = student
        if not date is None:
            date = datetime.strptime(date,'%Y-%m-%d')
            year = date.strftime('%Y')
            month = date.strftime('%m')
            day = date.strftime('%d')
            attendance = Attendance.objects.filter(date__year = year, date__month = month, date__day = day, course = course_id).all()
            for atten in attendance:
                attendance_data[atten.student.id]['status'] = atten.status
            context = {
                'attendance_data' : list(attendance.values()),
                'students':students
                }
            
    return render(request, 'take_attendance.html', context)
    #{'course': course_id, 'teacher': teacher, 'student':students, 'attendance':attendance }
''' class Attendancecreate(CreateView):
    
    model = Attendance
    form_class = TakeAttendanceForm
    success_url = '/attendance/'

    def get_context_data(self,** kwargs):
        context = super(Attendancecreate, self).get_context_data(**kwargs)
        course = course.objects.get(id=id)
        context['formset'] = AttendanceFormset(queryset=Attendance.objects.none(), instance=course.objects.get(id=id), initial=[{'student': student} for student in self.get_initial()['student']])
        return context

    def get_initial(self):
        course_id = get_object_or_404(Course, id = course_id)
        course = course.objects.get(id=course_id)
        initial = super(Attendancecreate , self).get_initial()
        initial['student'] = Student.objects.filter(student_course=course)
        return initial

    def post(self, request, *args, **kwargs,):
        course = course.objects.get(id=id)
        formset = AttendanceFormset(request.POST,queryset=Attendance.objects.none(), instance=course.objects.get(id=id), initial=[{'student': student} for student in self.get_initial()['student']])
        if formset.is_valid():
            return self.form_valid(formset)

    def form_valid(self,formset):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.course_attendance = get_object_or_404(Course, id=id)
            instance.save()
        return HttpResponseRedirect('/dashboard/') '''

def take_attendance(request):
    response = {'ststus':'failed', 'msg':''}
    if request.method == 'POST':
        post = request.POST
        date = datetime.strptime(post['attendance_date'], '%Y-%m-%d')
        year = date.strftime('%Y')
        month = date.strftime('%m')
        day = date.strftime('%d')
        _class = Course.objects.get(id=post['course'])
        Attendance.objects.filter(date__year = year, date__month = month, date__day = day, course = _class).delete()
        for student in post.getlist('student[]'):
            status = post['typeclassIns['+student+']']
            studInstance = Student.objects.get(id = student)
            att = Attendance(student=studInstance, status = status, course = _class, date=post['date']).save()
        response['status'] = 'success'
        messages.success(request,"Attendance has been saved successfully.")
    return HttpResponse(json.dumps(response),content_type="application/json")
    ''' course_id = get_object_or_404(Course, id = course_id)
    teacher = Teacher.objects.filter(course_teacher = course_id)
    students = Student.objects.filter(course_student = course_id)
    date = datetime.date.today
    #form = TakeAttendanceForm(request.POST or None)
        #course,student,date,statu

    if request.method == 'POST':
        for stu in students:
            student = get_object_or_404(Student, id = stu.id)
            if request.POST.get('status') == 'on':
                Attendance.status == 'A'
            elif request.POST.get('field_name', '') == 'on':
                Attendance.status == 'T'
            else:
                Attendance.status == 'P'
            attendance = Attendance(course_id=course_id.id, student=student, status=Attendance.status, date=date)
            attendance.save()

    messages.success(request,"Attendance Recored")

    return redirect('/attendance/course_id')'''

def report_behavior(request):
    form =BehaviorForm(request.POST or None)
    context = {
        'form':form
    }
    if request.method == 'POST':
        if form.is_valid():
            # assigns variables to the post data
            student = form.cleaned_data.get('student')
            teacher = form.cleaned_data.get('teacher')
            incident_date = form.cleaned_data.get('incident_date')
            location = form.cleaned_data.get('loaction')
            details = form.cleaned_data.get('details')
            sign = form.cleaned_data.get('sign')
            try:
                # attemps to create a new Course based on variables above
                bForm = Behavior()
                bForm.student = student
                bForm.teacher = teacher
                bForm.incident_date = incident_date
                bForm.location = location
                bForm.details = details                
                bForm.save()
                messages.success(request, 'Behavior form subbmitted')
                return redirect('/teacher')
            except Exception as e:
                #returns exception error
                messages.error(request, str(e))
        else:
            form = CreateCourseForm()
            messages.error(request, 'Error try again')
    return render(request, 'behavior.html', {'form': form})

def view_behavior(request, name, behavior_id):
    behavior_id = get_object_or_404(Behavior, id = behavior_id)
    #teacher = Teacher.objects.filter(course_teacher = behavior_id)
    name = Student.objects.filter(student_behavior = behavior_id)

    print(student, teacher)
    return render(request, 'view_behavior.html',{'name':name})   

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
            return HttpResponseRedirect('/view_course/course_add')
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