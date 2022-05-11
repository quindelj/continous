from datetime import datetime
from itertools import count
from multiprocessing import context
from tabnanny import check
from urllib import response
from django.urls import reverse
from django.forms import formset_factory
from django.shortcuts import get_object_or_404, render, redirect
from .models import *
from django.contrib import messages
from .forms import AttendanceForm, BehaviorForm, CreateCourseForm, GradeForm,TeacherForm, StudentForm, AddStudentForm, TakeAttendanceForm
from django.contrib.auth import authenticate, login, logout,get_user_model
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
import json

# Create your views here.
User = get_user_model

def index(request):
    return render (request, 'authenticate/login.html')

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
        print(user)
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
            return redirect('/teacher')
        else: 
            user.isStudent
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
                return HttpResponseRedirect('/home')
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
    course_id = get_object_or_404(Course, id = course_id)
    teacher = Teacher.objects.filter(course_teacher = course_id)
    students = Student.objects.filter(course_student = course_id)
    attendance = Attendance.objects.filter(course = course_id)
    user=request.session
    student = Student.objects.filter(course_student = course_id)
    behavior = Behavior.objects.all()

    print(student, teacher,attendance,behavior,student)
    return render(request, 'view_course.html',{'course': course_id, 'teacher': teacher, 'students':students, 'behavior':behavior,'user':user, 'student':student})   

def view_data(request, course_id):
    
    course_id = get_object_or_404(Course, id = course_id)
    teacher = Teacher.objects.filter(course_teacher = course_id)
    students = Student.objects.filter(course_student = course_id)
    attendance = Attendance.objects.filter(course = course_id)
    grades = GradeBook.objects.filter(course = course_id)
    behavior = Behavior.objects.filter(teacher = teacher, student = students)
    print(grades)
    context = {
        'course':course_id,
        'teacher':teacher,
        'student':students,
        'attendance':attendance,
        'behavior':behavior,
        'grades':grades
    }
    return render(request, 'data.html', context)  

def attendance(request, course_id):
    '''
    Get the course and student to take attendance
    AttendaceForm gets the attendance status
    '''
    course_id = get_object_or_404(Course, id = course_id)
    student = Student.objects.filter(course_student = course_id)
    count = student.count()
    attendance_formset = formset_factory(TakeAttendanceForm, extra=count)
    date = datetime.today().date


    if request.user.is_authenticated:
        #teacher = request.user
        if request.method == 'POST':
            formset = attendance_formset(request.POST)
            list = zip(student,formset) #add student and attendance tuple list
            if formset.is_valid():
                try:
                    for form, student in zip(formset,student): #for loop to get studens and attendance type
                        date = datetime.today()
                        mark = form.cleaned_data['mark_attendance']
                        #print(mark)
                        check_attendance = Attendance.objects.filter(course=course_id, date=date, student=student) # checks if attendance exist
                        #print(check_attendance)
                        '''
                        if attendance exist matcing querset it removes the the values
                        '''
                        if check_attendance:
                            attendance = Attendance.objects.get(course=course_id,date=date,student=student)
                            if attendance.status == 'A':
                                student.absent = student.absent - 1
                            elif attendance.status == 'P':
                                student.present = student.present - 1
                            elif attendance.status == 'T':
                                student.present = student.present - 1
                            attendance.status = mark
                            attendance.save() 
                except Exception as e:
                #returns exception error
                    print(e)
                    #messages.error(request, str(e))
                else:
                    ''''
                    If no attendance exist one is created
                    takes the valuses and submit them
                    '''
                    attendance = Attendance()
                    attendance.course = course_id
                    #attendance.teacher = teacher
                    attendance.student = student
                    attendance.date = date
                    attendance.status= mark
                    attendance.save()
                try:
                    if mark == 'Absent':
                        student.absent = student.absent + 1
                    if mark == 'Present':
                        student.present = student.present + 1
                    student.save()
                    context = {
                        'students': student,
                        'course': course_id,
                    }
                    messages.success(request,'Attendance submited')
                    return redirect ('/view_course/'+str(course_id.id))
                except Exception as e:
                    messages.error(request, 'Please mark all students')
                return redirect ('/attendance/'+ str(course_id.id))
            else:
                messages.error(request,'An error occured try again')
                return redirect ('/attendance/'+ str(course_id.id))
        else:
            list = zip(student,attendance_formset())
            context = {
                'formset': attendance_formset(),
                'students': student,
                'teacher': teacher,
                'course':course_id,
                'list': list,
                'date':date,
            }
            print(list)
            return render(request, 'take_attendance.html', context)

    else:
        return HttpResponse(status=403)


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
                bForm.sign = sign                
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



def record_grades(request):
    return redirect('/')

def grade(request, course_id):
    course_id = get_object_or_404(Course, id = course_id)
    students = Student.objects.filter(course_student = course_id)
    # counts the number students in the qureset
    count = students.count()
    # set the number of form field based on number of sutdents
    grade_formset = formset_factory(GradeForm, extra=count)
    course = course_id

    if request.user.is_authenticated:
        if request.method == 'POST':
            formset = grade_formset(request.POST)
            list = zip(students,formset)
            if formset.is_valid():
                try:
                    for form, students in zip(formset,students):
                        grade = form.cleaned_data['grade']
                        test = form.cleaned_data['select_test']
                        check_exist = GradeBook.objects.filter(course = course_id, students=students, test=test)
                        if check_exist:
                            messages.info(request, 'Grade already recored')
                except Exception as e:
                    print(e)
                else:
                    grades = GradeBook()
                    grades.student = students
                    grades.course = course_id
                    grades.test = test
                    grades.grade = grade
                    grades.save()
                try:
                    students.save()
                    context = {
                        'students':students,
                        'course': course_id,
                    }
                    messages.success(request, 'Grades submitted')
                    return redirect('/view_course/' + str(course_id.id))
                except Exception as e:
                    messages.error(request, 'Please mark all grades')
                return redirect ('/grade/' + str(course_id.id))
            else:
                messages.error(request, 'An error occured, try again')
        else:
            list = zip(students, grade_formset())

            context = {
                'formset': grade_formset,
                'students': students,
                'course_id': course_id,
                'course': course_id,
                'list': list,
                #'grade':grade,
            }
    return render(request, 'grades.html', context)

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

#student options

def view_grades(request, student_id):
    student_id = get_object_or_404(Student, id = student_id)
    #grade = GradeBook.objects.filter(student = student_id)
    grade = GradeBook.objects.all()
    student = student_id.id
    #teacher = Teacher.objects.filter(course_teacher = behavior_id)

    return render(request, 'view_grade.html',{ 'grade':grade, 'student_id':student_id, 'student':student})  

def view_behavior(request, student_id):
    student_id = get_object_or_404(Student, id = student_id)
    behavior = Behavior.objects.filter(student = student_id)
    student = student_id.id
    #teacher = Teacher.objects.filter(course_teacher = behavior_id)

    return render(request, 'view_behavior.html',{ 'behavior':behavior, 'student_id':student_id, 'student':student})  

def view_attendance(request, student_id):
    student_id = get_object_or_404(Student, id = student_id)
    attendance = Attendance.objects.filter(student = student_id)
    student = student_id.id
    #teacher = Teacher.objects.filter(course_teacher = behavior_id)

    return render(request, 'view_attendance.html',{ 'attendance':attendance, 'student_id':student_id, 'student':student})  