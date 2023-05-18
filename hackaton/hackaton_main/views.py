from django.shortcuts import render, redirect
from .models import *
from .forms import CreateUserForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.urls import reverse_lazy
from django.views import generic
import os, datetime, subprocess
from .forms import EditorForm
from datetime import datetime

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
    users = User.objects.all()
    user_rates = {}
    for user in users:
        user_rates[user.username] = UserTask.objects.filter(user_id=user.id, status=True).count()
    user_rates = dict(sorted(user_rates.items(), key=lambda item: item[1], reverse=True))
    context = {'user_rates': user_rates}
    print(context)
    return render(request, 'main/ratings.html', context)


def user_page(request, pk):
    user = User.objects.get(id=request.user.id)
    user_tasks = UserTask.objects.filter(user_id=request.user.id)
    context = {'user': user, 'tasks': user_tasks}
    return render(request, 'main/user_page.html', context)


def tasks(request):
    tasks_objects = Task.objects.filter(language=1)
    user_tasks = UserTask.objects.filter(user_id=request.user.id,status=True)
    task_list = [task.id for task in user_tasks]
    tasks_count = tasks_objects.count()
    context = {'tasks_objects': tasks_objects, 'tasks_count': tasks_count, 'task_list': task_list}
    return render(request, 'main/tasks.html', context)


def py_tasks(request):
    tasks_objects = Task.objects.filter(language=2)
    user_tasks = UserTask.objects.filter(user_id=request.user.id,status=True)
    task_list = [task.id for task in user_tasks]
    tasks_count = tasks_objects.count()
    context = {'tasks_objects': tasks_objects, 'tasks_count': tasks_count, 'task_list': task_list}
    return render(request, 'main/py_tasks.html', context)


def rb_tasks(request):
    tasks_objects = Task.objects.filter(language=3)
    user_tasks = UserTask.objects.filter(user_id=request.user.id,status=True)
    task_list = [task.id for task in user_tasks]
    tasks_count = tasks_objects.count()
    context = {'tasks_objects': tasks_objects, 'tasks_count': tasks_count, 'task_list': task_list}
    return render(request, 'main/rb_tasks.html', context)


def task_page(request, pk):
    task = Task.objects.get(id=pk)
    user = request.user 
    user_this_task = UserTask.objects.filter(user_id=user.id, task_id=task.id) 
    count = 0 
    for u_t_s in user_this_task: 
    	if u_t_s.time.date() == datetime.now().date(): 
    		count += 1 
    if count >= 5: 
    	blocked = True
    else: 
    	blocked = False
    print(count, 'count')
    result = False
    if request.method == 'POST':
        form = EditorForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            language = form.cleaned_data['language']
            output_task = output_task = [i for i in task.output if i != '\r']
            if language == '1': 
            	output_code = start_docker_python(code)[:-1]
            	print(output_code)
            	if list(output_code) == output_task:
            		result = True
            else: 
            	output_code = start_docker_ruby(code)[:-1]
            	if list(output_code) == output_task: 
            		result = True
            		
        user_task = UserTask.objects.create(user_id=request.user, task_id=task, status=result, code=code, language=int(language))
        if result: 
        	task.try_true += 1 
        	task.try_all += 1
        else: 
        	task.try_all += 1
        task.save()
    else:
        form = EditorForm()
    context = {'task': task, "form": form, 'result': result, 'blocked': blocked}
    return render(request, 'main/task.html', context)

def start_docker_python(code):
    docker_cmd = 'docker run -i --rm --name running-script -v /home/maha:/home/maha -w /home/maha python python main.py'
    file_path = '/home/maha/main.py'
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(code)
        
    ret = subprocess.run(
        docker_cmd, timeout=5, shell=True, text=True, capture_output=True)
    return ret.stdout

    
def start_docker_ruby(code):
    docker_cmd = 'docker run -i --rm --name running-script -v /home/maha:/home/maha -w /home/maha ruby ruby main.rb'
    file_path = '/home/maha/main.rb'
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(code)
        
    ret = subprocess.run(docker_cmd, timeout=5, shell=True, text=True,	capture_output=True)
    return ret.stdout


'''
class Home(generic.FormView):
    template_name = 'main/task.html'
    form_class = EditorForm
    success_url = reverse_lazy('main:home')

    def form_valid(self, form):
        code = form.cleaned_data['code']
        output = start_docker(code)
        context = self.get_context_data(form=form, output=output)
        return self.render_to_response(context)'''
# Create your views here.
