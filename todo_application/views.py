
from django.shortcuts import redirect, render

from django.views import View
# Create your views here.

from todo_application.forms import TaskForm, CommentForm, TagForm
from todo_application.models import Task, Comment, Tag

class HomeView(View):
    def get(self, request):
        task_form = TaskForm()
        tasks = Task.objects.all()

        html_data = {
            'form': task_form,
            'task_list': tasks,
        }

        return render(
            request=request,
            template_name='index.html',
            context = html_data,
        )
    
    def post(self, request):
        task_form = TaskForm(request.POST)
        task_form.save()

        return redirect('home')


class TaskDetailView(View):
    def get(self, request, task_id):
        task = Task.objects.get(id=task_id)
        task_form = TaskForm(instance=task)

        comments = Comment.objects.filter(task=task)
        comment_form = CommentForm(task=task)

        all_tags = Tag.objects.filter(task=task)
        tag_form = TagForm()

        html_data = {
            'task_form': task_form,
            'task': task,
            'comment_list': comments,
            'comment_form': comment_form,
            'tag_list': all_tags,
            'tag_form': tag_form,
        }

        return render(
            request=request,
            template_name='detail.html',
            context= html_data,
        )
    
    def post(self, request, task_id):
        task = Task.objects.get(id=task_id)

        if 'update' in request.POST:
            task_form = TaskForm(request.POST, instance=task)
            task_form.save()
        elif 'delete' in request.POST:
            task.delete()
        elif 'add' in request.POST:
            comment_form = CommentForm(request.POST, task=task)
            comment_form.save()

            return redirect('task_detail', task.id)
        
        elif 'tag' in request.POST:
            tag = TagForm(request.POST)
            tag.save(task)
            return redirect('task_detail', task.id)

        return redirect('home')
