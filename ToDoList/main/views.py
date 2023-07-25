from django.shortcuts import render, redirect
from django.http import HttpResponse

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
        return HttpResponse('Error - User is not authorized')
    

def mark_done(request, task_id):
    ''' mark the task as completed, 
        or not completed if it is already marked as completed'''

    try:
        task = models.Task.objects.get(id=task_id)
    except:
        return HttpResponse('Error. Task not found')
    
    if not task.mark: # Checking if a task is marked as completed
        task.mark = True
    else:
        task.mark = False
    
    task.save() # Change task status

    return redirect(request.META.get('HTTP_REFERER'))


def view_task(request, task_id):
    '''View the task in more detail'''

    try:
        task = models.Task.objects.get(id=task_id)
    except:
        return HttpResponse('Error. Task not found')
    
    context = {
        'task': task
    }

    return render(request, 'main/view-task.html', context)