from django.urls import path
from . import views

urlpatterns = [
    path('', views.news, name="news"),
    path('courses', views.courses),
    path('ratings', views.ratings),
    path('tasks', views.tasks),
    path('c_tasks', views.c_tasks),
    path('java_tasks', views.java_tasks),
    path('register', views.register_page),
    path('login', views.login_page, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('tasks/<str:pk>', views.task_page)

]
