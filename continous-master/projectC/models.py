from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
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
    
    first_name = models.CharField(max_length=225, null=True)
    last_name = models.CharField(max_length=225, null=True)
    username = models.CharField(unique = True, max_length=225, null=True)
    type = models.CharField(_('Type'), max_length=250, choices = Types.choices, default = Types.STUDENT)
    email = models.EmailField(unique=True)
    profilePic = models.ImageField(null=True, blank=True, upload_to='images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = 'username'
class SiteUser(models.Model):
    users = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

class Course(models.Model):
    title = models.CharField(max_length=225)
    courseImage = models.ImageField(null=True, blank=True, upload_to='images/')
    descrption = models.CharField(max_length=225)
    teacher = models.ForeignKey(SiteUser, related_name="course_teacher", on_delete = models.CASCADE)
    student = models.ManyToManyField(SiteUser, related_name= "course_student",  blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
class Teacher(User):
    object = TeacherManager()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = User.Types.TEACHER
        return super().save(*args, **kwargs)

    course = models.ForeignKey(Course, related_name = 'course', on_delete = models.CASCADE, null=True) 
    user = models.OneToOneField(SiteUser, related_name='teacher_user', on_delete= models.CASCADE, null=True)

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

    user = models.OneToOneField(SiteUser, related_name='student_user', on_delete=models.CASCADE,null=True)
    course = models.ForeignKey(Course, related_name='student_course', on_delete = models.CASCADE, null=True)
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = User.Types.STUDENT
        return super().save(*args, **kwargs)

    def __str__(self):
        return "%s  %s" % ( self.first_name, self.last_name)
        


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