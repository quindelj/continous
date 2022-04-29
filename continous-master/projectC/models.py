from django.db import models
from django.contrib.auth.models import AbstractUser
from django.forms import CharField, DateField, ModelChoiceField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
import re
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def basic_validator(self, form):
        errors = {}
        email_checker = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(form['first_name']) < 2:
            errors["first_name"] = "First Name should be at least 2 characters"
        if len(form['last_name']) < 3:
            errors["last_name"] = "Last Name should be at least 2 characters"
        if len(form['email']) < 8:
            errors["email"] = "Email should be at least 10 characters"
        if not EMAIL_REGEX.match(form['email']):
            errors['email'] = 'Invalid Email Address'
        email_check = self.filter(email=form['email'])
        if email_check:
            errors['email'] = "Email already in use"
        if len(form['password']) < 8:
            errors["password"] = "Password should be at least 8 characters"
        if form['password'] != form['confirm']:
            errors['password'] = 'Passwords do not match'
        
        return errors

    def authenticate(self, email, password):
        users = self.filter(email=email)
        if not users:
            return False

        user = users[0]
        return password
        #return bcrypt.checkpw(password.encode(), user.password.encode())

    def register(self, form):
        #pw = bcrypt.hashpw(form['password'].encode(), bcrypt.gensalt()).decode()
 
        return self.create(
            first_name = form['first_name'],
            last_name = form['last_name'],
            email = form['email'],
            username = form['username'],
            password = form['password'],
            type = form['type'],
            #isStudent = form['isStudent'],
            #isParent = form['isParent'],
            #password = pw,
        )
#Filter the User table for user type
class TeacherManager(models.Manager):
    def get_querset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type = User.Types.TEACHER)

class StudentManager(models.Manager):
    def get_querset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type = User.Types.STUDENT)

class ParentManager(models.Manager):
    def get_querset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type = User.Types.PARENT)
# Create your models here.
class User(AbstractUser):

    ''' TEACHER = 'TEACHER'
    STUDENT = 'STUDENT'
    PARENT = 'PARENT'
    
    USER_TYPE = [
        (TEACHER, 'Teacher'),
        (STUDENT, 'Student'),
        (PARENT, 'Parent'),
    ] '''
    class Types(models.TextChoices):
        TEACHER = "TEACHER", "Teacher"
        STUDENT = "STUDENT", "Student"
        PARENT = "PARENT", "Parent"
#user type
    #type = models.CharField(max_length=250, choices = USER_TYPE.choices, default = STUDENT,)

    ''' def is_upperclass(self):
        return self.type in{
            self.TEACHER,
            self.STUDENT,
        } '''

    isTeacher = models.BooleanField('Teacher', default=False)
    isStudent = models.BooleanField('Student', default=False)
    isParent = models.BooleanField('Parent', default=False)
    
    first_name = models.CharField(max_length=225, null=True)
    last_name = models.CharField(max_length=225, null=True)
    username = models.CharField(unique = True, max_length=225, null=True)
    type = models.CharField(_('Type'), max_length=250, choices = Types.choices, default = Types.STUDENT)
    email = models.EmailField(unique=True)
    profilePic = models.ImageField(blank = True, null = True)
    #password = models.CharField(max_length=225)
    #password2 = models.CharField(max_length=225, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = 'username'
    

    #objects = UserManager()

class Admin(models.Model):
    admin = models.OneToOneField(User, on_delete=models.CASCADE)

class Course(models.Model):
    title = models.CharField(max_length=225)
    descrption = models.TextField()
    teacher = models.ForeignKey(User, related_name="course_teacher", on_delete = models.CASCADE)
    student = models.ManyToManyField(User, related_name= "course_student",  blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
class Teacher(User):
    object = TeacherManager()

    #class Meta:
        #proxy = True
    #overrides save method
    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = User.Types.TEACHER
        return super().save(*args, **kwargs)

    course = models.ForeignKey(Course, related_name = 'course', on_delete = models.CASCADE, null=True) 
    admins = models.OneToOneField(User, related_name='teacher_admin', on_delete= models.CASCADE, null=True)
    #created_at = models.DateTimeField(auto_now_add=True)
    #updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return "%s  %s" % ( self.first_name, self.last_name )
        #return str(self.first_name) 
class Parent(User):
    class Meta:
        proxy = True #doesn't create new table
    #student = models.ForeignKey(User, related_name= 'child', on_delete = models.CASCADE, null = True)
    #created_at = models.DateTimeField(auto_now_add=True)
    #updated_at = models.DateTimeField(auto_now=True)

class Student(User):
    object = StudentManager()

    #class Meta:
        #proxy = True #doesn't create new table

    #overrides save method
    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = User.Types.STUDENT
        return super().save(*args, **kwargs)
    #parent = models.ForeignKey(Parent, related_name='parent', on_delete= models.CASCADE)
    #user_type = models.OneToOneField(User,related_name='student', on_delete= models.CASCADE, primary_key=True)
    course = models.ForeignKey(Course, related_name='student_course', on_delete = models.CASCADE, null=True)
    #created_at = models.DateTimeField(auto_now_add=True)
    #updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return "%s  %s" % ( self.first_name, self.last_name )
        #return str(self.first_name + self.last_name)


class GradeBook(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    test = models.FloatField(default = 0)
    exam = models.FloatField(default = 0)
    assignment = models.FloatField(default = 0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Attendance(models.Model):
    attendance_type = [('P', 'Present'), ('T', 'Tardy'), ('A', 'Absent')]
    course = models.ForeignKey(Course,related_name = 'course_attendance', on_delete= models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=1, choices=attendance_type, default='Present')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Behavior(models.Model):
    student = models.ForeignKey(Student, on_delete= models.CASCADE)
    report = models.TextField()
    reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.report




"""class User(AbstractUser):
    class Types(models.TextChoices):
        TEACHER = "TEACHER", "Teacher"
        STUDENT = "STUDENT", "Student"
        PARENT = "PARENT", "Parent"
#user type
    type = models.CharField(__('Type'), max_length='250', choices = Types.choices, default = Types.STUDENT)
    #name = models.CharField(_("Name of User"), blank = True, max_length = 255)
    first_name = models.CharField(max_length=225, null=True)
    last_name = models.CharField(max_length=225, null=True)
    #username = models.CharField(max_length=225, null=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=225)
    phoneNum = models.CharField(max_length=225)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

#Extends from the use tabel proxy sets user level
class Teacher(User):
    object = TeacherManager()

    class Meta:
        proxy = True
    #overrides save method
    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = User.Types.TEACHER
        return super().save(*args, **kwargs)

class Student(User):
    object = StudentManager()

    class Meta:
        proxy = True #doesn't create new table

    #overrides save method
    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = User.Types.STUDENT
        return super().save(*args, **kwargs)

class Parent(User):
    object = ParentManager()

    class Meta:
        proxy = True

    #overrides save method
    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = User.Types.PARENT
        return super().save(*args, **kwargs) """


