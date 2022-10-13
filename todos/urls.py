from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

app_name = "todos"   

urlpatterns = [
    path("", login_required(views.TodosCreateAndListView.as_view()), name="index"),
    path("todos/archive", login_required(views.TodoArchiveView.as_view()), name="todos_archive"),
    path("todo/<pk>/update/", login_required(views.TodoUpdateView.as_view()), name="update_todo"),
    path("todo/<pk>/archive/<str:name>", login_required(views.TodoAchiveView.as_view()), name="archive_todo"),
    path("todo/<pk>/delete/", login_required(views.TodoDeleteView.as_view()), name="delete_todo"),
    path("todos/export", views.export_todos_csv, name="export_todos"),
    path("todos/import", views.import_todos_csv, name="import_todos"),
    path("todos/export-email", views.export_and_email, name="export_email_todos"),

    path("tags/", login_required(views.TagsCreateAndListView.as_view()), name="tags"),
    path("tag/<pk>/delete/", login_required(views.TagDeleteView.as_view()), name="delete_tag"),
    path("tag/<pk>/update/", login_required(views.TagUpdateView.as_view()), name="update_tag"),
]