#from curses.ascii import US
#from django import forms
from curses.ascii import SI
from tkinter import Widget
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models  import User

class SignUpForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'isTeacher', 'isStudent', 'isParent')

    def __init__(self, *args, **kwargs ):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['class'] = 'form-control'

'''class LoginForm(forms.Form):
    class meta:
        model = User
        fields = ("username", "password")'''

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    username = forms.ChoiceField(
        widget=forms.TextInput(
                attrs = {
                "class" : "form-control"
            }
        )
    )

    password = forms.ChoiceField(
        widget=forms.PasswordInput(
                attrs = {
                "class" : "form-control"
            }
        )
    )

'''class SignUpForm(UserCreationForm):
    username = forms.ChoiceField(
        widget=forms.TextInput(
                attrs = {
                "class" : "form-control"
            }
        )
    )

    password1 = forms.ChoiceField(
        widget=forms.PasswordInput(
                attrs = {
                "class" : "form-control"
            }
        )
    )

    password2 = forms.ChoiceField(
        widget=forms.PasswordInput(
                attrs = {
                "class" : "form-control"
            }
        )
    )

    email = forms.ChoiceField(
        widget=forms.TextInput(
                attrs = {
                "class" : "form-control"
            }
        )
    )

    first_name = forms.ChoiceField(
        widget=forms.TextInput(
                attrs = {
                "class" : "form-control"
            }
        )
    )

    last_name = forms.ChoiceField(
        widget=forms.TextInput(
                attrs = {
                "class" : "form-control"
            }
        )
    )

    isTeacher = forms.BooleanField( 
        widget=forms.CheckboxInput(
            attrs= {
                "class" : "form-control"
            }
        )
    ) 

    isStudent = forms.BooleanField( 
        widget=forms.CheckboxInput(
            attrs= {
                "class" : "form-control"
            }
        )
    )

    isPsrent = forms.BooleanField( 
        widget=forms.CheckboxInput(
            attrs= {
                "class" : "form-control"
            }
        )
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'isTeacher', 'isStudent', 'isParent')'''