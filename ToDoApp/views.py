from django.shortcuts import render, redirect
#Generic Views
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView ,FormView

from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Task
# Create your views here.
class CustomLoginView(LoginView):
    fileds = '__all__'
    template_name= 'ToDoApp/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('tasks')
    
class RegisterPage(FormView):
    template_name = 'ToDoApp/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')
    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request,user)
        return super(RegisterPage,self).form_valid(form)
    def get(self,*args,**kwargs):# This function will restict the user form login page and register page
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage,self).get(*args,**kwargs)

# This class will show all the tasks in the database 
class TaskList(LoginRequiredMixin,ListView):
    model = Task
    context_object_name = 'tasks'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] =  context['tasks'].filter(user =self.request.user)
        context['count'] = context['tasks'].filter(complete = False).count()
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__startswith= search_input)
            
        context['search_input'] = search_input

        return context
#This class will show all the details of the selected task
class TaskDetails(LoginRequiredMixin,DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'ToDoApp/task.html'
#This class is uesd to create a new task 
class TaskCreate(LoginRequiredMixin,CreateView):
    model = Task
    fields = ['title','description','complete']
    success_url = reverse_lazy('tasks')
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate,self).form_valid(form)
#This class is uesd to update a task which is already in the list
class TaskUpdate(LoginRequiredMixin,UpdateView):
    model = Task
    fields = ['title','description','complete']
    success_url = reverse_lazy('tasks')
#This class is used to delete an specific task from the lisk
class TaskDelete(LoginRequiredMixin,DeleteView):
    model = Task
    context_object_name = 'task' 
    success_url = reverse_lazy('tasks')

