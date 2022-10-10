from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

app_name = "todos"   

urlpatterns = [
    path("", login_required(views.TodosCreateAndListView.as_view()), name="index"),
    path("todo/<pk>/update/", login_required(views.TodoUpdateView.as_view()), name="update_todo"),
    path("todo/<pk>/delete/", login_required(views.TodoDeleteView.as_view()), name="delete_todo"),
    path("tags/", login_required(views.TagsCreateAndListView.as_view()), name="tags"),
    path("tag/<pk>/delete/", login_required(views.TagDeleteView.as_view()), name="delete_tag"),
    path("tag/<pk>/update/", login_required(views.TagUpdateView.as_view()), name="update_tag"),
]