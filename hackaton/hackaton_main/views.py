from django.shortcuts import render, redirect
from .models import *
from .forms import CreateUserForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import CodeForm
from django.conf import settings
from django.urls import reverse_lazy
from django.views import generic
import os, datetime, subprocess
from .forms import EditorForm

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
    user_tasks = UserTask.objects.filter(user_id=request.user.id)
    task_list = [task.id for task in user_tasks]
    tasks_count = tasks_objects.count()
    context = {'tasks_objects': tasks_objects, 'tasks_count': tasks_count, 'task_list': task_list}
    return render(request, 'main/tasks.html', context)


def java_tasks(request):
    tasks_objects = Task.objects.filter(language=2)
    user_tasks = UserTask.objects.filter(user_id=request.user.id)
    task_list = [task.id for task in user_tasks]
    tasks_count = tasks_objects.count()
    context = {'tasks_objects': tasks_objects, 'tasks_count': tasks_count, 'task_list': task_list}
    return render(request, 'main/java_tasks.html', context)


def c_tasks(request):
    tasks_objects = Task.objects.filter(language=3)
    user_tasks = UserTask.objects.filter(user_id=request.user.id)
    task_list = [task.id for task in user_tasks]
    tasks_count = tasks_objects.count()
    context = {'tasks_objects': tasks_objects, 'tasks_count': tasks_count, 'task_list': task_list}
    return render(request, 'main/c_tasks.html', context)

def task_page(request, pk):
    task = Task.objects.get(id=pk)
    print(request.POST.get('languages'))
    if request.method == 'POST':
        form = EditorForm(request.POST)
        if form.is_valid():
            pass
            #user = request.user
            #code = form.cleaned_data['text']
            #status = code_check(code, task)
            #task_solution = UserTask(user_id=user, task_id=task, status=status, code=code)
            #task_solution.save()
    else:
        form = EditorForm()
    context = {'task': task, "form": form}
    return render(request, 'main/task.html', context)

def start_docker(code):
    file_dir = os.path.join(settings.BASE_DIR, 'history')
    docker_cmd = 'docker run -i --rm --name my-running-script -v {}:/usr/src/myapp -w /usr/src/myapp python:3.7 python {}'
    file_name = '{}.py'.format(datetime.datetime.now().strftime("%m-%d-%Y-%H-%M-%S"))
    file_path = os.path.join(file_dir, file_name)
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(code)

    cmd = docker_cmd.format(file_dir, file_name)
    ret = subprocess.run(
        cmd, timeout=15, shell=True,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )
    print(ret.stdout)
    return ret.stdout.decode()

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
