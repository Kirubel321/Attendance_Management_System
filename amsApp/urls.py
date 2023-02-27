from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [

    path('login/', views.login_view, name='login_url'),
    path('logout/',views.logoutview, name='logout_url'),

    path('teacher_register/',views.teacher_register_view, name='teacher_register_url'),
    path('student_register/',views.student_register_view, name='student_register_url'),   
    path('hod_register/',views.hod_register_view, name='hod_registration_url'),   

    path('student/<slug:stud_id>/attendance/', views.student_attendance, name='student_attendance_url'),
    path('student/<slug:stud_id>/<slug:course_id>/attendance/', views.student_attendance_detail, name='student_attendance_detail_url'),
    path('student/',views.student_view,name='student_home_url'),
    path('student/<slug:student_id>/notification', views.student_notification, name='student_notification_url'),

    path('teacher/',views.teacher_view,name='teacher_home_url'),
    path('teacher/<slug:teacher_id>/', views.t_clas, name='t_clas_url'),
    path('teacher/<int:assign_id>/Students/attendance/', views.t_student, name='t_student_url'),
    path('teacher/<int:assign_id>/ClassDates/', views.t_class_date, name='t_class_date_url'),
    
    path('teacher/<int:ass_c_id>/attendance/', views.t_attendance, name='t_attendance_url'),
    path('teacher/<int:ass_c_id>/Edit_att/', views.edit_att, name='edit_att_url'),
    path('teacher/<int:ass_c_id>/attendance/confirm/', views.confirm, name='confirm_url'),
  
    path('teacher/<slug:teacher_id>/notification', views.t_notification, name='t_notification_url'),
     

   
    path('hod/',views.admin_home_view, name='admin_home_url'), 
    
    path('hod/manage_teacher/',views.admin_teacher_view, name='admin_teacher_url'), 
    path('hod/manage_teacher_update/<int:pk>/',views.admin_teacher_update_view, name='admin_teacher_update_url'),
    path('hod/manage_teacher_delete/<int:pk>/',views.admin_teacher_delete_view, name='admin_teacher_delete_url'),

    path('hod/manage_student/',views.admin_student_view, name='admin_student_url'), 
    path('hod/manage_student_update/<slug:pk>/',views.admin_student_update_view, name='admin_student_update_url'),
    path('hod/manage_student_delete/<slug:pk>/',views.admin_student_delete_view, name='admin_student_delete_url'),
    
    path('hod/manage_course/',views.admin_course_view, name='admin_course_url'), 
    path('hod/manage_course_update/<slug:pk>/',views.admin_course_update_view, name='admin_course_update_url'),
    path('hod/manage_course_delete/<slug:pk>/',views.admin_course_delete_view, name='admin_course_delete_url'),
    
    path('hod/manage_notification_teacher/',views.admin_notification_teacher_view, name='admin_notification_teacher_url'), 
    path('hod/manage_notification_teacher_update/<slug:pk>/',views.admin_notification_teacher_update_view, name='admin_notification_teacher_update_url'),
    path('hod/manage_notification_teacher_delete/<slug:pk>/',views.admin_notification_teacher_delete_view, name='admin_notification_teacher_delete_url'),
    
    path('hod/manage_notification_student/',views.admin_notification_student_view, name='admin_notification_student_url'), 
    path('hod/manage_notification_student_update/<int:pk>/',views.admin_notification_student_update_view, name='admin_notification_student_update_url'),
    path('hod/manage_notification_student_delete/<int:pk>/',views.admin_notification_student_delete_view, name='admin_notification_student_delete_url'),


   
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_sent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_form.html'), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset_complete_.html'), name='password_reset_complete'),     

]