from django.urls import path

from todo_application.views import HomeView, TaskDetailView

urlpatterns = [
    path('', HomeView.as_view(), name= 'home'),
    path('<int:task_id>', TaskDetailView.as_view(), name='task_detail')
    ]