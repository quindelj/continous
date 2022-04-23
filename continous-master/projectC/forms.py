from dataclasses import fields
from pyexpat import model
from tkinter import Widget
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models  import Course, User, Teacher, Student

class SignUpForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name','type', 'email', 'password',)
        #fields=('__all__')
        '''def save(self):
            user = super().save(commit=False)
            user.isTeacher = True
            user.save()
            teacher = Teacher.objects.create(user=user)
            teacher.user_type.add()
            return user'''

    def __init__(self, *args, **kwargs ):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['class'] = 'form-control'
        #self.fields['password2'].widget.attrs['class'] = 'form-control'

class TeacherForm(ModelForm):
    class meta:
        model = User
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
    }
    


class CreateCourseForm(ModelForm):
    class Meta:
        model = Course
        fields = ('title', 'descrption','teacher')
    lables = {

    }
    widgets = {
        'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Course Title'}),
        'descrption': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'About Course'}),
        'teacher': forms.Select(attrs={'class': 'form-control', 'placeholder': 'teacher'}),
    }