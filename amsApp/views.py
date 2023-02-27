from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from .models import User, Student_u, Teacher_u, Dept, Class, Student, Attendance, Course, Teacher, Assign, AttendanceTotal, time_slots, DAYS_OF_WEEK, AssignTime, AttendanceClass, StudentCourse, NotificationTeacher, NotificationStudent
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .forms import TeacherCustomUserCreationForm,AdminCustomUserCreationForm, StudentCustomUserCreationForm, StudentForm, ClassForm, DeptForm, NotificationStudentForm,  NotificationTeacherForm, ClassForm, CourseForm 
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


# Create your views here.
def login_view(request): 
    if request.method == 'POST':
        usern = request.POST['username']
        passwd = request.POST['password']
        if not (usern and passwd):
            messages.error(request, 'Please provide all the details!!')
            return render(request, 'login_page.html')
        user = authenticate(request, username=usern, password=passwd)
        if not user:
            messages.error(request, 'Invalid Login Credentials!!')
            return render(request, 'login_page.html')
        if user is not None:
            login(request, user)
        if user.role == "STUDENT":
            return redirect('student_home_url')
        elif user.role == "TEACHER":
            return redirect('teacher_home_url')
        elif user.role == "ADMIN":
            return redirect('admin_home_url')

    return render(request, 'login_page.html')

def logoutview(request):
    logout(request)
    return redirect('login_url')



def student_register_view(request):
    if request.user.is_authenticated:
        return redirect('login_url')
    else:
        form = StudentCustomUserCreationForm()
        if request.method == 'POST':
            form = StudentCustomUserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user )
                return redirect('login_url')
        context = {'form':form}
    return render(request, 'student_registration.html', context)

def teacher_register_view(request):
    if request.user.is_authenticated:
        return redirect('login_url')
    else:
        form = TeacherCustomUserCreationForm()
        if request.method == 'POST':
            form = TeacherCustomUserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user )
                return redirect('login_url')
        context = {'form':form}
    return render(request, 'teacher_registration.html', context)


def hod_register_view(request):
    form = AdminCustomUserCreationForm()
    if request.method == 'POST':
        form = AdminCustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user )
            return redirect('admin_home_url')
    context = {'form':form}
    return render(request, 'admin_registration.html', context)

# student view

@login_required()
def student_view(request):
    return render(request, 'student_home.html')

@login_required()
def student_attendance(request, stud_id):
    stud = Student.objects.get(USN=stud_id)
    ass_list = Assign.objects.filter(class_id_id=stud.class_id)
    att_list = []
    for ass in ass_list:
        try:
            a = AttendanceTotal.objects.get(student=stud, course=ass.course)
        except AttendanceTotal.DoesNotExist:
            a = AttendanceTotal(student=stud, course=ass.course)
            a.save()
        att_list.append(a)
    return render(request, 'student_attendance.html', {'att_list': att_list})


@login_required()
def student_attendance_detail(request, stud_id, course_id):
    stud = get_object_or_404(Student, USN=stud_id)
    cr = get_object_or_404(Course, id=course_id)
    att_list = Attendance.objects.filter(course=cr, student=stud).order_by('date')
    return render(request, 'student_attendance_detail.html', {'att_list': att_list, 'cr': cr})

@login_required()
def student_notification(request, student_id):
    studentNote = NotificationStudent.objects.filter(student_id=student_id)
    return render(request, 'student_notification.html', {'studentNote':studentNote})
 


# Teacher Views

@login_required()
def teacher_view(request):
    return render(request, 'teacher_home.html')

@login_required
def t_clas(request, teacher_id):
    teacher1 = get_object_or_404(Teacher, id=teacher_id)
    return render(request, 'teacher_class.html', {'teacher1': teacher1})


@login_required()
def t_student(request, assign_id):
    ass = Assign.objects.get(id=assign_id)
    att_list = []
    for stud in ass.class_id.student_set.all():
        try:
            a = AttendanceTotal.objects.get(student=stud, course=ass.course)
        except AttendanceTotal.DoesNotExist:
            a = AttendanceTotal(student=stud, course=ass.course)
            a.save()
        att_list.append(a)
    return render(request, 'teacher_student.html', {'att_list': att_list})


@login_required()
def t_class_date(request, assign_id):
    now = timezone.now()
    ass = get_object_or_404(Assign, id=assign_id)
    att_list = ass.attendanceclass_set.order_by('date')
    return render(request, 'teacher_class_date.html', {'att_list': att_list})



@login_required()
def t_attendance(request, ass_c_id):
    assc = get_object_or_404(AttendanceClass, id=ass_c_id)
    ass = assc.assign
    c = ass.class_id
    context = {
        'ass': ass,
        'c': c,
        'assc': assc,
    }
    return render(request, 'teacher_attendance.html', context)


@login_required()
def edit_att(request, ass_c_id):
    assc = get_object_or_404(AttendanceClass, id=ass_c_id)
    cr = assc.assign.course
    att_list = Attendance.objects.filter(attendanceclass=assc, course=cr)
    context = {
        'assc': assc,
        'att_list': att_list,
    }
    return render(request, 'teacher_edit_attendance.html', context)


@login_required()
def confirm(request, ass_c_id):
    assc = get_object_or_404(AttendanceClass, id=ass_c_id)
    ass = assc.assign
    cr = ass.course
    cl = ass.class_id
    for i, s in enumerate(cl.student_set.all()):
        status = request.POST[s.USN]
        if status == 'present':
            status = 'True'
        else:
            status = 'False'
        if assc.status == 1:
            try:
                a = Attendance.objects.get(course=cr, student=s, date=assc.date, attendanceclass=assc)
                a.status = status
                a.save()
            except Attendance.DoesNotExist:
                a = Attendance(course=cr, student=s, status=status, date=assc.date, attendanceclass=assc)
                a.save()
        else:
            a = Attendance(course=cr, student=s, status=status, date=assc.date, attendanceclass=assc)
            a.save()
            assc.status = 1
            assc.save()

    return HttpResponseRedirect(reverse('t_class_date_url', args=(ass.id,)))



@login_required()
def t_notification(request, teacher_id):
    note = NotificationTeacher.objects.filter(teacher_id=teacher_id)
    return render(request, 'teacher_notification.html', {'note':note})
    

# Hod

@login_required()
def admin_home_view(request):
    return render(request, 'admin_home.html')

@login_required()
def admin_teacher_view(request):
    teacher_p = Teacher.objects.all()
    context ={'teacher_p':teacher_p}
    return render(request, 'admin_teacher.html', context)

@login_required()
def admin_teacher_update_view(request, pk):
    teacherProfile = Teacher.objects.get(id=pk)
    form = TeacherForm(instance = teacherProfile)
    if request.method == 'POST':
        formProfile = TeacherForm(request.POST, instance = teacherProfile)
        if formProfile.is_valid():
            formProfile.save()            
            messages.success(request, 'Teacher assigning is successfully updated ' )
            formProfile = TeacherForm()
            return redirect('admin_teacher_url')
    context = {'form':form}
    return render(request, 'admin_teacher.html',context)

@login_required()
def admin_teacher_delete_view(request,pk):
    teacher = Teacher.objects.get(id=pk)
    if request.method == 'POST':
        teacher.delete()
        return redirect('admin_teacher_url')
    context = {'teacher':teacher}
    return render(request, 'admin_teacher_delete.html', context)

@login_required()
def admin_student_view(request):
    student_p = Student.objects.all()
    context ={'student_p':student_p}
    return render(request, 'admin_student.html', context)

@login_required()
def admin_student_update_view(request, pk):
    studentProfile = Student.objects.get(USN=pk)
    formProfile = StudentForm(instance = studentProfile)
    if request.method == 'POST':
        formProfile = StudentForm(request.POST, instance = studentProfile)
        if formProfile.is_valid():
            formProfile.save()            
            messages.success(request, 'Student assigning is successfully updated ' )
            formProfile = StudentForm()
            return redirect('admin_student_url')
    context = {'formProfile':formProfile}
    return render(request, 'admin_student.html',context)

@login_required()
def admin_student_delete_view(request,pk):
    student = Student.objects.get(USN=pk)
    if request.method == 'POST':
        student.delete()
        return redirect('admin_student_url')
    context = {'student':student}
    return render(request, 'admin_student_delete.html', context)

@login_required()
def admin_course_view(request):
    form = CourseForm()
    course = Course.objects.all()
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()            
            messages.success(request, 'Course information added successfully  ' )
            form = CourseForm()
    context ={'form':form,'course':course}
    return render(request, 'admin_course.html', context)

@login_required()
def admin_course_update_view(request, pk):
    course = Course.objects.get(id=pk)
    form = CourseForm(instance = course)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance = course)
        if form.is_valid():
            form.save()            
            messages.success(request, 'Course information updated successfully' )
            form = CourseForm()
            return redirect('admin_course_url')
    context = {'form':form}
    return render(request, 'admin_course.html',context)

@login_required()
def admin_course_delete_view(request,pk):
    course = Course.objects.get(id=pk)
    if request.method == 'POST':
        course.delete()
        return redirect('admin_course_url')
    context = {'course':course}
    return render(request, 'admin_course_delete.html', context)


@login_required()
def admin_notification_teacher_view(request):
    formTeacher = NotificationTeacherForm()

    notificationTeacher = NotificationTeacher.objects.all()
   
    if request.method == 'POST':
        formTeacher = NotificationTeacherForm(request.POST)
        if formTeacher.is_valid():
            formTeacher.save()            
            messages.success(request, 'Teacher Notification information added successfully  ' )
            formTeacher = NotificationTeacherForm()
    context ={'formTeacher':formTeacher,'notificationTeacher':notificationTeacher}
    return render(request, 'admin_notification_teacher.html', context)


@login_required()
def admin_notification_teacher_update_view(request, pk):
    notificationTeacher = NotificationTeacher.objects.get(id=pk)
    formTeacher = NotificationTeacherForm(instance = notificationTeacher)
    if request.method == 'POST':
        formTeacher = NotificationTeacherForm(request.POST, instance = notificationTeacher)
        if formTeacher.is_valid():
            formTeacher.save()            
            messages.success(request, 'Teacher Notification information updated successfully' )
            formTeacher = NotificationTeacherForm()
            return redirect('admin_notification_teacher_url')
    context = {'formTeacher':formTeacher}
    return render(request, 'admin_notification_teacher_update.html',context)


@login_required()
def admin_notification_teacher_delete_view(request,pk):
    notificationTeacher = NotificationTeacher.objects.get(id=pk)
    if request.method == 'POST':
        notificationTeacher.delete()
        return redirect('admin_notification_teacher_url')
    context = {'notificationTeacher':notificationTeacher}
    return render(request, 'admin_notification_teacher_delete.html', context)


@login_required()
def admin_notification_student_view(request):
    formStudent = NotificationStudentForm()

    notificationStudent = NotificationStudent.objects.all()
   
    if request.method == 'POST':
        formStudent = NotificationStudentForm(request.POST)
        if formStudent.is_valid():
            formStudent.save()            
            messages.success(request, 'Student notification information added successfully  ' )
            formStudent = NotificationStudentForm()
    context ={'formStudent':formStudent,'notificationStudent':notificationStudent}
    return render(request, 'admin_notification_student.html', context)

@login_required()
def admin_notification_student_update_view(request, pk):
    notificationStudent = NotificationStudent.objects.get(id=pk)
    formStudent = NotificationStudentForm(instance = notificationStudent)
    if request.method == 'POST':
        formStudent = NotificationTeacherForm(request.POST, instance = notificationStudent)
        if formTeacher.is_valid():
            formStudent.save()            
            messages.success(request, 'Teacher Notification information updated successfully' )
            formStudent = NotificationStudentForm()
            return redirect('admin_notification_student_url')
    context = {'formStudent':formStudent}
    return render(request, 'admin_notification_student_update.html',context)


@login_required()
def admin_notification_student_delete_view(request,pk):
    notificationStudent = NotificationStudent.objects.get(id=pk)
    if request.method == 'POST':
        notificationStudent.delete()
        return redirect('admin_notification_student_url')
    context = {'notificationStudent':notificationStudent}
    return render(request, 'admin_notification_student_delete.html', context)

 
