from django.urls import path
from taskweb import views


urlpatterns= [
    path("signup",views.SignUpView.as_view(),name="register"),
    path("",views.LogInView.as_view(),name="signin"),
    path("home",views.IndexView.as_view(),name="home"),
    path("tasks/add/",views.TaskCreateView.as_view(),name="task-add"),
    path("tasks/all",views.TaskListView.as_view(),name="task-list"),
    path("tasks/detail/<int:id>",views.TaskDetailView.as_view(),name="task-detail"),
    path("tasks/remove/<int:id>",views.TaskDeleteView.as_view(),name="task-delete"),
    path("tasks/<int:id>",views.TaskEditView.as_view(),name="task-edit"),
    path("signout",views.LOgoutView.as_view(),name="signout")

]