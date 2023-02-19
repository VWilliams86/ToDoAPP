from django.forms import ModelForm
from django import forms

from todo_application.models import Task, Comment, Tag


class TaskForm(forms.ModelForm):
    ''' Pull the 'description' column from the Task  model into a form '''
    class Meta:
        model = Task
        fields = ['description']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']

    def __init__(self, *args, **kwargs):
        task_object = kwargs.pop('task')

        super().__init__(*args, **kwargs)

        self.instance.task = task_object
        self.fields['body'].label = ''



class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = ''

    def save(self, task, *args, **kwargs):
        tag_name = self.data['name']
        try:
            tag = Tag.objects.get(name=tag_name)
        except Tag.DoesNotExist:
            tag = Tag.objects.create(name=tag_name)

        task.tags.add(tag) 