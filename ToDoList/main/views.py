from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound

from . import forms, models

# Create your views here.

def index(request):
    if request.user.is_authenticated:
        tasks = models.Task.objects.filter(user = request.user)

        context = {
            'tasks': tasks
        }

        return render(request, 'main/index.html', context)

    else:
        return redirect('users:login')
    

def create_task(request):
    '''Create a task using form'''
    
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = forms.TaskForm(request.POST)

            if form.is_valid():
                task = form.save(commit=False)
                task.user = request.user
                task.save()

                return redirect('/')
        else:
            form = forms.TaskForm()

            context = {
                'form': form
            }

            return render(request, 'main/create_task.html', context)
    else:
        return redirect('users:login')
    

def mark_done(request, task_id):
    ''' mark the task as completed, 
        or not completed if it is already marked as completed'''

    if request.user.is_authenticated:
        try:
            task = models.Task.objects.get(id=task_id)
        except:
            return HttpResponseNotFound()
        
        if task.user == request.user:
            if not task.mark: # Checking if a task is marked as completed
                task.mark = True
            else:
                task.mark = False
            
            task.save() # Change task status

            return redirect(request.META.get('HTTP_REFERER'))
        
        else:
            return HttpResponseNotFound()
    else:
        return redirect('users:login')


def view_task(request, task_id):
    '''View the task in more detail'''

    if request.user.is_authenticated:
        try:
            task = models.Task.objects.get(id=task_id)
        except:
            return HttpResponseNotFound()
        
        if task.user == request.user:
            context = {
                'task': task
            }

            return render(request, 'main/view-task.html', context)

        else:
            return HttpResponseNotFound()

    else:
        return redirect('users:login')


def delete_task(request, task_id):
    '''Delete task'''

    if request.user.is_authenticated:
        try:
            task = models.Task.objects.get(id=task_id)
        except:
            return HttpResponseNotFound()
        
        if task.user == request.user:
            task.delete()
            return redirect('/')
        
        else:
            return HttpResponseNotFound()
    else:
        return redirect('users:login')


def edit_task(request, task_id):
    '''Edit task'''

    if request.user.is_authenticated:
        try:
            task = models.Task.objects.get(id=task_id)
        except:
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

            else:
                context = {
                    'task': task
                }

                return render(request, 'main/edit-task.html', context)
    
        else:
            return HttpResponseNotFound()
    else:
        return redirect('users:login')
