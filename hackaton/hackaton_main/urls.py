from django.urls import path
from . import views

urlpatterns = [
    path('', views.news, name="news"),
    path('courses', views.courses),
    path('ratings', views.ratings),
    path('tasks', views.tasks),
    path('rb_tasks', views.rb_tasks),
    path('py_tasks', views.py_tasks),
    path('register', views.register_page),
    path('login', views.login_page, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('tasks/<str:pk>', views.task_page),
    path('user/<str:pk>', views.user_page),
]
