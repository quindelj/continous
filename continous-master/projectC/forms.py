from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models  import Course, User, Teacher, Student

class TeacherForm(UserCreationForm):
    class Meta:
        model = Teacher
        fields = ('username', 'first_name', 'last_name','type', 'email', 'password1','password2')
        def save(self):
            user = super().save(commit=False)
            user.type = 'TEACHER'
            user.save()
            teacher = Teacher.objects.create(user=user)
            teacher.user_type.add()
            return user


    def __init__(self, *args, **kwargs ):
        super(TeacherForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'

class StudentForm(UserCreationForm):
    class Meta:
        model = Student
        fields = ('username', 'first_name', 'last_name','type', 'email', 'password1','password2')
        def save(self):
            user = super().save(commit=False)
            user.type = 'STUDENT'
            user.save()
            student = Student.objects.create(user=user)
            student.user_type.add()
            return user

    def __init__(self, *args, **kwargs ):
        super(StudentForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'

'''class (ModelForm):
    class meta:
        model = Teacher
        fields = ('username', 'first_name', 'last_name', 'email', 'password1','type')

        def save(self):
            user = super().save(commit=False)
            user.isTeacher = True
            user.set_password(user.password)
            user.save()
            Teacher.objects.create(user=user)
            return user
                
        lables = {
        'username': '',
        'first_name': '',
        'last_name': '',
        'email': '',
        'password': '',
    }
    
    widgets = {
        'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Course Title'}),
        'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'About Course'}),
        'last_name': forms.Select(attrs={'class': 'form-control', 'placeholder': 'teacher'}),
        'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'About Course'}),
        'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'teacher'}),
    }'''
    


class CreateCourseForm(forms.ModelForm):
    #teacherList = Teacher.objects.all()
    teacher = forms.ModelChoiceField(queryset=Teacher.objects.all())
    student = forms.ModelMultipleChoiceField(widget= forms.CheckboxSelectMultiple, queryset=Student.objects.all())
    class Meta:
        model = Course
        fields = ('title', 'descrption','teacher', 'student', 'courseImage')
    lables = {

    }
    widgets = {
        'title': forms.TextInput(attrs={'class': 'form-control'}),
        'descrption': forms.TextInput(attrs={'class': 'form-control'}),
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

'''class StudentAddForm(ModelForm):
    class Meta:
        model = Course
        fields = ('course','teacher')
    
    widgets = {
        'course': forms.Select(attrs={'class': 'form-control', 'placeholder':'Course Title'}),
        'teacher': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'teacher'}),
    }'''