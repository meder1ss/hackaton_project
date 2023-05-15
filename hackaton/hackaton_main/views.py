from django.shortcuts import render, redirect
from .models import *
from .forms import CreateUserForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

def register_page(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Создан аккаунт ' + form.cleaned_data.get('username'))
            return redirect('login')
    context = {'form': form, 'errors': form.errors.as_text()}
    return render(request, 'main/register.html', context)

def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('news')
        else:
            messages.info(request, 'Имя пользователя или пароль неверные')
    context = {}
    return render(request, 'main/login.html', context)

def logout_user(request):
    logout(request)
    return redirect('login')

def news(request):
    news_objects = News.objects.all()
    context = {'news_objects': news_objects}
    return render(request, 'main/news.html', context)


def courses(request):
    context = {}
    return render(request, 'main/courses.html', context)


def ratings(request):
    context = {}
    return render(request, 'main/ratings.html', context)


def tasks(request):
    tasks_objects = Task.objects.filter(language=1)
    tasks_count = tasks_objects.count()
    context = {'tasks_objects': tasks_objects, 'tasks_count': tasks_count}
    return render(request, 'main/tasks.html', context)


def java_tasks(request):
    tasks_objects = Task.objects.filter(language=2)
    tasks_count = tasks_objects.count()
    context = {'tasks_objects': tasks_objects, 'tasks_count': tasks_count}
    return render(request, 'main/java_tasks.html', context)


def c_tasks(request):
    tasks_objects = Task.objects.filter(language=3)
    tasks_count = tasks_objects.count()
    context = {'tasks_objects': tasks_objects, 'tasks_count': tasks_count}
    return render(request, 'main/c_tasks.html', context)

def task_page(request, pk):
    task = Task.objects.get(id=pk)
    context = {'task': task}
    return render(request, 'main/task.html', context)

# Create your views here.
