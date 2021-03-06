from dataclasses import fields
from pyexpat import model
from django import forms
from django.forms import HiddenInput, ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models  import Attendance, AttendanceReport, Behavior, Course, GradeBook, User, Teacher, Student
from django.forms import inlineformset_factory

attendance_type = (
    ('P', 'Present'), 
    ('T', 'Tardy'), 
    ('A', 'Absent')
)

test_name = (
    ('test 1', 'test 1'),
    ('test 2', 'test 2'),
    ('test 3', 'test 3'),
    ('test 4', 'test 4'),
    ('Final Exam', 'Final Exam'),
)
class TeacherForm(UserCreationForm):
    # creates a user as a student
    class Meta:
        model = Teacher
        fields = ('username', 'first_name', 'last_name','type', 'email', 'password1','password2')
        def save(self):
            user = super().save(commit=False)
            user.isTeacher = True
            user.type = 'TEACHER'
            user.save()
            teacher = Teacher.objects.create(user=user)
            teacher.user_type.add()
            return user

    # removes form lables
    lables = {
        'username': '',
        'first_name': '',
        'last_name': '',
        'email': '',
        'password1': '',
        'password2': '',
    }
    # adds form-control class and placeholder for form
    widgets = {
        'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Username'}),
        'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
        'last_name': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
        'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
        'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
    }

    def __init__(self, *args, **kwargs ):
        super(TeacherForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'

class StudentForm(UserCreationForm):
    # creates a user as a student
    class Meta:
        model = Student
        fields = ('username', 'first_name', 'last_name','type', 'email', 'password1','password2')
        def save(self):
            user = super().save(commit=False)
            user.isStudent = True
            user.type = 'STUDENT'
            user.save()
            student = Student.objects.create(user=user)
            student.user_type.add()
            return user
            
    # removes form lables
    lables = {
        'username': '',
        'first_name': '',
        'last_name': '',
        'email': '',
        'password1': '',
        'password2': '',
    }

    # adds form-control class and placeholder for form
    widgets = {
        'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Username'}),
        'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
        'last_name': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
        'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
        'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
    }

    def __init__(self, *args, **kwargs ):
        super(StudentForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'

class CreateCourseForm(forms.ModelForm):
    teacher = forms.ModelChoiceField(queryset=Teacher.objects.all()) # gets the teachers form the database
    student = forms.ModelMultipleChoiceField(widget= forms.CheckboxSelectMultiple, queryset=Student.objects.all()) # gets all students from the database and allows you to selcet more than one
    #student = CustomModelChoiceField(widget= forms.CheckboxSelectMultiple, queryset=Student.objects.all()) # gets all students from the database and allows you to selcet more than one

    class Meta:
        model = Course
        fields = ('title','teacher','student', 'courseImage')
    lables = {

    }
    widgets = {
        'title': forms.TextInput(attrs={'class': 'form-control'}),
        #'descrption': forms.TextInput(attrs={'class': 'form-control'}),
        'teacher': forms.Select(attrs={'class': 'form-control', 'placeholder': 'teacher'}),
        'student': forms.CheckboxSelectMultiple(attrs={'class': 'form-control'}),

    }
class AddStudentForm(ModelForm):
    student = forms.ModelChoiceField(queryset=Student.objects.all())
    course = forms.ModelChoiceField(queryset=Course.objects.all())
    class Meta:
        model = Student
        fields = ('course', 'student')
    widgets = {
        'student': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder':'Course Title'}),
        'course': forms.Select(attrs={'class': 'form-control', 'placeholder': 'About Course'}),
    }

class BehaviorForm(ModelForm):
    student = forms.ModelChoiceField(queryset=Student.objects.all())
    teacher = forms.ModelChoiceField(queryset=Teacher.objects.all()) #
    class Meta:
        model = Behavior
        fields = ('student', 'teacher', 'incident_date' ,'location', 'details', 'sign')
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'teacher': forms.Select(attrs={'class': 'form-control'}),
            'incident_date': forms.DateInput(format=('%Y-%m-%d'), attrs={'class': 'form-control', 'placeholder': 'Select a date','type': 'date'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'details': forms.Textarea(attrs={'class': 'form-control'}),
            'sign': forms.TextInput(attrs={'class': 'form-control'}),
        }
class AttendanceForm(forms.Form):
    ststus = forms.ChoiceField(widget=forms.RadioSelect, choices=attendance_type )

    class Meta:
        model = Attendance
        fields = ('stasus')
        widgets = {
        'status': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder':'Course Title'}),
        }
AttendanceFormset = inlineformset_factory(Student,Attendance,form=AttendanceForm,fields=('student', 'status')) 

class TakeAttendanceForm(forms.Form):
    mark_attendance = forms.ChoiceField(widget=forms.RadioSelect, choices=attendance_type)

class GradeForm(forms.Form):

    select_test = forms.ChoiceField(widget=forms.Select, choices=test_name)

GradeFormset = inlineformset_factory(Student,GradeBook,form=GradeForm,fields=('student', 'grade')) 
