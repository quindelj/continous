from email.policy import default
from django.db import models
from django.contrib.auth.models import AbstractUser
import math
from datetime import timedelta
from django.core.validators import MinValueValidator, MaxValueValidator
from django.forms import BooleanField
from django.utils.translation import gettext_lazy as _

DAYS_OF_WEEK = (
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
    ('Saturday', 'Saturday'),
)
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
    class Types(models.TextChoices):
        TEACHER = "TEACHER", "Teacher"
        STUDENT = "STUDENT", "Student"
        PARENT = "PARENT", "Parent"

    isTeacher = models.BooleanField(default=False) 
    isStudent = models.BooleanField(default=False) 
    
    first_name = models.CharField(max_length=225, null=True)
    last_name = models.CharField(max_length=225, null=True)
    username = models.CharField(unique = True, max_length=225, null=True)
    type = models.CharField(_('Type'), max_length=250, choices = Types.choices, default = Types.STUDENT)
    email = models.EmailField(unique=True)
    profilePic = models.ImageField(null=True, blank=True, upload_to='images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = 'username'
'''class SiteUser(User):
    users = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, parent_link=True)'''

class Course(models.Model):
    title = models.CharField(max_length=225, null=False)
    courseImage = models.ImageField(null=True, blank=True, upload_to='images/')
    #descrption = models.CharField(max_length=225)
    teacher = models.ForeignKey(User, related_name="course_teacher", on_delete = models.CASCADE)
    student = models.ManyToManyField(User, related_name= "course_student",  blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    

    def __str__(self):
        return str(self.title)
class Teacher(User):
    object = TeacherManager()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = User.Types.TEACHER
        return super().save(*args, **kwargs)

    course = models.ForeignKey(Course, related_name = 'course', on_delete = models.CASCADE, null=True) 
    user = models.OneToOneField(User, related_name='teacher_user', on_delete= models.CASCADE, null=True)

    def __str__(self):
        return "%s  %s" % ( self.first_name, self.last_name )
class Parent(User):
    class Meta:
        proxy = True #doesn't create new table
    #student = models.ForeignKey(User, related_name= 'child', on_delete = models.CASCADE, null = True)
    #created_at = models.DateTimeField(auto_now_add=True)
    #updated_at = models.DateTimeField(auto_now=True)

class Student(User):
    object = StudentManager()

    user = models.OneToOneField(User, related_name='student_user', on_delete=models.CASCADE,null=True)
    course = models.ForeignKey(Course, related_name='student_course', on_delete = models.CASCADE, null=True)
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = User.Types.STUDENT
        return super().save(*args, **kwargs)

    def __str__(self):
        name = f'{self.first_name} {self.last_name}'
        return str(name)
        
    def get_present(self):
        student =  self.user
        _class =  self.course
        try:
            present = Attendance.objects.filter(course= _class, student=student, status = 'P').count()
            return present
        except:
            return 0
    
    def get_tardy(self):
        student =  self.user
        _class =  self.course
        try:
            present = Attendance.objects.filter(course= _class, student=student, status = 'T').count()
            return present
        except:
            return 0

    def get_absent(self):
        student =  self.user
        _class =  self.course
        try:
            present = Attendance.objects.filter(course= _class, student=student, status = 'A').count()
            return present
        except:
            return 0
class GradeBook(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    test = models.CharField(max_length=50, choices=test_name)
    grade = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Attendance(models.Model):
    course = models.ForeignKey(Course,related_name = 'course_attendance', on_delete= models.CASCADE)
    teacher = models.ForeignKey(Teacher, related_name= 'teacher_taking', on_delete=models.DO_NOTHING, blank=True, null=True)
    student = models.ForeignKey(Student, related_name =  'student_attendance', on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=8, choices= attendance_type , default='Present')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.course)+' '+ str(self.student)

class AttendanceReport(models.Model):
    student = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    attendance = models.ForeignKey(Attendance,on_delete=models.CASCADE)
    status = models.CharField(max_length=8, choices=attendance_type, default='Present')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Behavior(models.Model):
    student = models.ForeignKey(Student, related_name='student_behavior', on_delete= models.CASCADE)
    teacher = models.ForeignKey(Teacher, related_name='student_teacher', on_delete= models.CASCADE)
    incident_date = models.DateField(null=True, blank=True,)
    location = models.CharField(max_length=250, null = True)
    details = models.TextField(null=True, blank=True)
    sign = models.CharField(max_length=220, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.details