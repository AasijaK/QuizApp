from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('login/',views.login_view,name='login'),
    path('register/',views.register,name='register'),
    path('logout/',views.logout_view,name='logout'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('admin-dashboard/',views.admin_dashboard,name='admin_dashboard'),
    path('subjects/',views.subjects,name='subjects'),
    path('subjects/add/',views.add_subject,name='add_subject'),
    path('subjects/delete/<int:id>/',views.delete_subject,name='delete_subject'),
    path('questions/',views.questions,name='questions'),
    path('questions/add/',views.add_question,name='add_question'),
    path('quiz/',views.quiz_setup,name='quiz_setup'),
    path('quiz/start/',views.start_quiz,name='start_quiz'),
    path('quiz/play/',views.quiz,name='quiz'),
    path('quiz/result/',views.result,name='result'),
    path('history/',views.history,name='history'),
]