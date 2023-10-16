from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.http import require_http_methods
from django.views.generic import FormView

from .models import ToDo, Category, RegisterForm, Profile, ProfileForm


@login_required
def index(request):
    categories_list = Category.objects.filter(user_id=request.user.id)
    todo_list = ToDo.objects.all()[::-1]
    return render(request, 'todoapp/index.html', {'title': 'Index', 'categories_list': categories_list, 'todo_list': todo_list})


@require_http_methods(['POST'])
def add(request):
    title = request.POST['title']
    category_id = request.POST['category']
    todo = ToDo(title=title, category=Category.objects.get(id=category_id))
    todo.save()
    return redirect('index')


@require_http_methods(['POST'])
def add_category(request):
    title = request.POST['name']
    category = Category(user=request.user, title=title)
    category.save()
    return redirect('index')


@require_http_methods(['POST'])
def delete_category(request):
    category_id = request.POST['category']
    category = Category.objects.get(id=category_id)
    category.delete()
    return redirect('index')


@require_http_methods(['POST'])
def update(request, todo_id):
    todo = ToDo.objects.get(id=todo_id)
    todo.title = request.POST['title']
    todo.description = request.POST['description']
    todo.category_id = request.POST['category']
    if request.POST['starts'] == '':
        todo.starts = None
    else:
        todo.starts = request.POST['starts'] + '+03:00'
    todo.is_complete = True if request.POST.get('is_complete', False) else False
    todo.save()
    return redirect('index')


def delete(request, todo_id):
    todo = ToDo.objects.get(id=todo_id)
    todo.delete()
    return redirect('index')


@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = Profile.objects.get(user=request.user)
            profile.image = form.cleaned_data['image']
            profile.save()
            return redirect('profile')
    else:
        form = ProfileForm()
    return render(request, 'todoapp/profile.html', {'form': form})


class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    # success_url = reverse_lazy('todolist:profile')
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        form.save()
        form_valid = super().form_valid(form)
        if form_valid:
            #get the username and password
            username = self.request.POST['username']
            password = self.request.POST['password1']
            #authenticate user then login
            user = authenticate(username=username, password=password)
            login(self.request, user)
            # after user creating, running signals.py, where creates profile for user
            return redirect('profile')
        return form_valid


@login_required
def settings(request):
    return render(request, 'todoapp/settings.html')


@require_http_methods(['POST'])
def update_settings(request):
    user = request.user
    user.email = request.POST['email']
    user.save()

    profile = Profile.objects.get(user=request.user)
    profile.address = request.POST['address']
    profile.phone = request.POST['phone']
    profile.is_notifications = True if request.POST.get('is_notifications', False) else False
    try:
        profile.tg_chat_id = int(request.POST['tg_chat_id'])
        profile.time_before_notification = int(request.POST['time_before_notification'])
    except ValueError:
        return redirect('settings')
    except MultiValueDictKeyError:
        pass
    profile.save()
    return redirect('settings')


def statistics(request):
    categories = Category.objects.filter(user_id=request.user.id)
    labels = []
    values = []
    for c in categories:
        todos = ToDo.objects.filter(category=c)
        labels.append(c.title)
        values.append(len(todos))
    categories_data = {
        "labels": labels,
        "values": values,
    }
    todos = []
    for c in categories:
        todos.extend(ToDo.objects.filter(category=c))

    completed_tasks = len(list(filter(lambda todo: todo.is_complete, todos)))
    completed = {
        "labels": ['Выполнено', 'В работе'],
        "values": [completed_tasks, len(todos) - completed_tasks]
    }

    todo_starts = [todo.starts for todo in todos if todo.starts is not None]
    tasks_by_hour = {}
    # Перебираем время выполнения задач и разбиваем их по часам
    for todo in todo_starts:
        # Получаем час из времени выполнения
        hour = todo.strftime("%Y-%m-%dT%H")
        tasks_by_hour[hour] = tasks_by_hour.get(hour, 0) + 1

    tasks_by_minute = {}
    for todo in todo_starts:
        minute = todo.strftime("%Y-%m-%dT%H:%M")
        tasks_by_minute[minute] = tasks_by_minute.get(minute, 0) + 1

    tasks_by_day = {}
    for todo in todo_starts:
        day = todo.strftime("%Y-%m-%d")
        tasks_by_day[day] = tasks_by_day.get(day, 0) + 1

    if len(tasks_by_day) > 3:
        todo_times = tasks_by_day
    elif len(tasks_by_hour) > 3:
        todo_times = tasks_by_hour
    else:
        todo_times = tasks_by_minute

    todo_times = {
        "labels": list(todo_times.keys()),
        "values": list(todo_times.values())
    }

    return render(request, 'todoapp/statistics.html',
                  {"categories": categories_data,
                   "completed": completed,
                   "todo_times": todo_times
                   })