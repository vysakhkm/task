from django.shortcuts import render,redirect
from django.views.generic import View
from taskweb.forms import UserForm,LoginForm,TaskForm,TaskEditForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from api.models import Tasks
from django.utils.decorators import method_decorator
from django.contrib import messages
# Create your views here.
def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            return redirect("signin")
        else:
            return fn(request,*args,**kwargs)
    return wrapper


class SignUpView(View):
    def get(self,request,*args,**kwargs):
        form=UserForm()
        return render(request,"register.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=UserForm(request.POST)
        if form.is_valid():
            User.objects.create_user(**form.cleaned_data)
            messages.success(request,"your account has been created succesfully")
            return redirect("signin")
        else:
            messages.error(request,"failed to create account!")
            return render(request,"register.html",{"form":form})


class LogInView(View):
    def get(self,request,*args,**kwargs):
        form=LoginForm()
        return render(request,"loging.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            usr=authenticate(request,username=uname,password=pwd)
            if usr:
                login(request,usr)
                return redirect("home")
            else:
                return render(request,"loging.html",{"form":form})

@method_decorator(signin_required,name="dispatch")                
class LOgoutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        messages.success(request,"logout")
        return redirect("signin")

@method_decorator(signin_required,name="dispatch")                
class IndexView(View):
    def get(self,request,*args,**kwargs):
          return render(request,"index.html")
    
@method_decorator(signin_required,name="dispatch")                
class TaskCreateView(View):
    def get(self,request,*args,**kwargs):
        form=TaskForm()
        return render(request,"task-add.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=TaskForm(request.POST)
        if form.is_valid():
            form.instance.user=request.user
            form.save()
            print("saved")
            messages.success(request,"succesfullly created task")
            return redirect("task-list")
        else:
            messages.error(request,"failed to create task!")
            return render(request,"task-add.html",{"form":form})

@method_decorator(signin_required,name="dispatch")                
class TaskListView(View):
    def get(self,request,*args,**kwargs):
        qs=Tasks.objects.filter(user=request.user).order_by("-created_date")
        return render(request,"task-list.html",{"tasks":qs})

@method_decorator(signin_required,name="dispatch")                
class TaskDetailView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        qs=Tasks.objects.get(id=id)
        return render(request,"task-detail.html",{"task":qs})

@method_decorator(signin_required,name="dispatch")                
class TaskDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        Tasks.objects.filter(id=id).delete()
        messages.success(request,"Task has been removed")
        return redirect("task-list")

@method_decorator(signin_required,name="dispatch")                
class TaskEditView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        obj=Tasks.objects.get(id=id)
        form=TaskEditForm(instance=obj)
        return render(request,"task-edit.html",{"form":form})
    def post(self,request,*args,**kwargs):
        id=kwargs.get("id")
        obj=Tasks.objects.get(id=id)
        form=TaskEditForm(request.POST,instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request,"succesfully updated task")
            return redirect("task-list")
        else:
            messages.error(request,"failed to change task")
            return render(request,"task-edit.html",{"form":form})



