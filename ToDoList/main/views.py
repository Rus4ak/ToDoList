from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound

from .forms import TaskForm
from .models import Task


def index(request):
    if request.user.is_authenticated:
        tasks = Task.objects.filter(user=request.user)

        context = {
            'tasks': tasks
        }

        return render(request, 'main/index.html', context)

    return redirect('users:login')


def create_task(request):
    '''Create a task using form'''

    if request.user.is_authenticated:
        if request.method == 'POST':
            form = TaskForm(request.POST)

            if form.is_valid():
                task = form.save(commit=False)
                task.user = request.user
                task.save()

                return redirect('/')

        form = TaskForm()

        context = {
            'form': form
        }

        return render(request, 'main/create_task.html', context)

    return redirect('users:login')


def mark_done(request, task_id):
    ''' mark the task as completed, 
        or not completed if it is already marked as completed'''

    if request.user.is_authenticated:
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return HttpResponseNotFound()

        if task.user == request.user:
            if not task.mark: # Checking if a task is marked as completed
                task.mark = True
            else:
                task.mark = False

            task.save() # Change task status

            return redirect(request.META.get('HTTP_REFERER'))

        return HttpResponseNotFound()

    return redirect('users:login')


def view_task(request, task_id):
    '''View the task in more detail'''

    if request.user.is_authenticated:
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return HttpResponseNotFound()

        if task.user == request.user:
            context = {
                'task': task
            }

            return render(request, 'main/view-task.html', context)

        return HttpResponseNotFound()

    return redirect('users:login')


def delete_task(request, task_id):
    if request.user.is_authenticated:
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return HttpResponseNotFound()

        if task.user == request.user:
            task.delete()
            return redirect('/')

        return HttpResponseNotFound()

    return redirect('users:login')


def edit_task(request, task_id):
    if request.user.is_authenticated:
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return HttpResponseNotFound()

        if task.user == request.user:
            if request.method == 'POST':
                # Take new values
                title = request.POST.get('title')
                description = request.POST.get('description')

                # Save new values
                task.title = title
                task.description = description

                task.save()

                return redirect('main:view-task', task_id=task_id)

            context = {
                'task': task
            }

            return render(request, 'main/edit-task.html', context)

        return HttpResponseNotFound()

    return redirect('users:login')
