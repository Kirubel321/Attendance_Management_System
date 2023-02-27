from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import User, Teacher_u,Student_u, Dept, Class, Student, Attendance, Course, Teacher, Assign, AttendanceTotal, time_slots, DAYS_OF_WEEK, AssignTime, AttendanceClass, StudentCourse, NotificationStudent, NotificationTeacher
from django.forms import ModelForm



class TeacherCustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Teacher_u
        fields = UserCreationForm.Meta.fields 

class StudentCustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Student_u
        fields = UserCreationForm.Meta.fields 
class AdminCustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields 
        
class TeacherForm(ModelForm):
    class Meta:
        model = Teacher
        fields = '__all__'
        
class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = '__all__'

class ClassForm(ModelForm):
    class Meta:
        model = Class
        fields = '__all__'

class DeptForm(ModelForm):
    class Meta:
        model = Dept
        fields = '__all__'

class NotificationStudentForm(ModelForm):
    class Meta:
        model = NotificationStudent
        fields = '__all__'   

class NotificationTeacherForm(ModelForm):
    class Meta:
        model = NotificationTeacher
        fields = '__all__'  

class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = '__all__'  

