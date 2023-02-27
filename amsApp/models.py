from django.db import models
import math
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser,  BaseUserManager
from django.db.models.signals import post_save, post_delete
from datetime import timedelta
from django.dispatch import receiver


# Create your models here.
gender_choice = (
    ('Male', 'Male'),
    ('Female', 'Female')
)

time_slots = (
    ('9:00 - 11:00', '9:00 - 11:00'),
    ('9:00 - 1:00', '9:00 - 1:00'),
    ('9:00 - 12:00', '9:00 - 12:00'),

    ('2:00 - 4:00', '2:00 - 4:00'),
    ('2:00 - 5:00', '2:00 - 5:00'),
)


DAYS_OF_WEEK = (
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
    ('Saturday', 'Saturday'),
)



class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        STUDENT = "STUDENT", "Student"
        TEACHER = "TEACHER", "Teacher"

    base_role = Role.ADMIN

    role = models.CharField(max_length=50, choices=Role.choices)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
            return super().save(*args, **kwargs)


class StudentManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.STUDENT)


class Student_u(User):

    base_role = User.Role.STUDENT

    student = StudentManager()

    class Meta:
        proxy = True




# @receiver(post_save, sender=Student_u)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created and instance.role == "STUDENT":
#         Student.objects.create(user=instance, USN=instance.id)



class TeacherManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.TEACHER)


class Teacher_u(User):

    base_role = User.Role.TEACHER

    teacher = TeacherManager()

    class Meta:
        proxy = True


# When using multi-table inheritance, a new database table is created for each subclass of a model. 
# This is usually the desired behavior, since the subclass needs a place to store any additional data fields that are not present on the base class.
#  Sometimes, however, you only want to change the Python behavior of a model – perhaps to change the default manager, or add a new method.

# This is what proxy model inheritance is for: creating a proxy for the original model. 
# You can create, delete and update instances of the proxy model and all the data will be saved as if you were using the original (non-proxied) model. 
# The difference is that you can change things like the default model ordering or the default manager in the proxy, without having to alter the original.

# @receiver(post_save, sender=Teacher_u)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created and instance.role == "TEACHER":
#         Teacher.objects.create(user=instance, id=instance.id)


class Dept(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Course(models.Model):
    dept = models.ForeignKey(Dept, on_delete=models.CASCADE)
    id = models.CharField(primary_key=True, max_length=50)
    name = models.CharField(max_length=50)
    shortname = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Class(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    dept = models.ForeignKey(Dept, on_delete=models.CASCADE)
    section = models.CharField(max_length=100)
    sem = models.IntegerField()

    class Meta:
        verbose_name_plural = 'classes'

    def __str__(self):
        d = Dept.objects.get(name=self.dept)
        return '%s : %d %s' % (d.name, self.sem, self.section)


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE, null=True)
    USN = models.CharField(primary_key='True', max_length=100)
    name = models.CharField(max_length=200)
    gender = models.CharField(max_length=50, choices=gender_choice)
    DOB = models.DateField(null=True)

    def __str__(self):
        return self.name


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dept = models.ForeignKey(Dept, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=50, choices=gender_choice)
    DOB = models.DateField(null=True)

    def __str__(self):
        return self.name


class Assign(models.Model):
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('course', 'class_id', 'teacher'),)

    def __str__(self):
        cl = Class.objects.get(id=self.class_id_id)
        cr = Course.objects.get(id=self.course_id)
        te = Teacher.objects.get(id=self.teacher_id)
        return '%s : %s : %s' % (te.name, cr.shortname, cl)


class AssignTime(models.Model):
    assign = models.ForeignKey(Assign, on_delete=models.CASCADE)
    period = models.CharField(max_length=50, choices=time_slots)
    day = models.CharField(max_length=15, choices=DAYS_OF_WEEK)


class AttendanceClass(models.Model):
    assign = models.ForeignKey(Assign, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Attendance'
        verbose_name_plural = 'Attendance'


class Attendance(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    attendanceclass = models.ForeignKey(AttendanceClass, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.BooleanField()

    def __str__(self):
        sname = Student.objects.get(name=self.student)
        cname = Course.objects.get(name=self.course)
        return '%s : %s' % (sname.name, cname.shortname)


class AttendanceTotal(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('student', 'course'),)

    @property
    def att_class(self):
        stud = Student.objects.get(name=self.student)
        cr = Course.objects.get(name=self.course)
        att_class = Attendance.objects.filter(course=cr, student=stud, status='True').count()
        return att_class

    @property
    def total_class(self):
        stud = Student.objects.get(name=self.student)
        cr = Course.objects.get(name=self.course)
        total_class = Attendance.objects.filter(course=cr, student=stud).count()
        return total_class

    @property
    def attendance(self):
        stud = Student.objects.get(name=self.student)
        cr = Course.objects.get(name=self.course)
        total_class = Attendance.objects.filter(course=cr, student=stud).count()
        att_class = Attendance.objects.filter(course=cr, student=stud, status='True').count()
        if total_class == 0:
            attendance = 0
        else:
            attendance = round(att_class / total_class * 100, 2)
        return attendance

    @property
    def classes_to_attend(self):
        stud = Student.objects.get(name=self.student)
        cr = Course.objects.get(name=self.course)
        total_class = Attendance.objects.filter(course=cr, student=stud).count()
        att_class = Attendance.objects.filter(course=cr, student=stud, status='True').count()
        cta = math.ceil((0.75 * total_class - att_class) / 0.25)
        if cta < 0:
            return 0
        return cta


class StudentCourse(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('student', 'course'),)
        verbose_name_plural = 'Marks'

    def __str__(self):
        sname = Student.objects.get(name=self.student)
        cname = Course.objects.get(name=self.course)
        return '%s : %s' % (sname.name, cname.shortname)

    def get_attendance(self):
        a = AttendanceTotal.objects.get(student=self.student, course=self.course)
        return a.attendance



class AttendanceRange(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


days = {
    'Monday': 1,
    'Tuesday': 2,
    'Wednesday': 3,
    'Thursday': 4,
    'Friday': 5,
    'Saturday': 6,
}


@receiver(post_save, sender=AssignTime)
def create_attendance(sender, instance, created, **kwargs):
    if created:
        start_date = AttendanceRange.objects.all()[:1].get().start_date
        end_date = AttendanceRange.objects.all()[:1].get().end_date
        for single_date in daterange(start_date, end_date):
            if single_date.isoweekday() == days[instance.day]:
                try:
                    AttendanceClass.objects.get(date=single_date.strftime("%Y-%m-%d"), assign=instance.assign)
                except AttendanceClass.DoesNotExist:
                    a = AttendanceClass(date=single_date.strftime("%Y-%m-%d"), assign=instance.assign)
                    a.save()


class NotificationStudent(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.student_id)
 
class NotificationTeacher(models.Model):
    teacher_id = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.teacher_id)


