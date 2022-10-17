from django.shortcuts import HttpResponseRedirect
from django.views.generic import (
    CreateView,
    DeleteView, 
    UpdateView,
    ListView
    )
from .models import Tag, Todo 
from .forms import TagForm, TodoForm, TodoUpdateForm
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.shortcuts import redirect
import csv
from django.http import HttpResponse
from io import StringIO 
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

class TagsCreateAndListView(SuccessMessageMixin, CreateView):
    template_name = "todos/tags.html"
    form_class = TagForm
    model = Tag
    paginate_by = 5
    success_url = reverse_lazy("todos:tags")
    success_message = 'Success create Tag'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = self.request.GET.get('page', 1)
        tags = self.model.objects.filter(user_id=self.request.user).order_by('-id')
        paginator = Paginator(tags, self.paginate_by)
        tags = paginator.get_page(page)

        context["tags"] = tags        
        context["prev_url"] = tags.previous_page_number() if tags.has_previous() else None
        context["next_url"] = tags.next_page_number() if tags.has_next() else None

        return context
    
    def form_valid(self, form):
        form.instance.user_id = self.request.user
        return super().form_valid(form)

class TagDeleteView(SuccessMessageMixin, DeleteView):
    model = Tag
    success_url = reverse_lazy("todos:tags")
    success_message = 'Success delete tag'

class TagUpdateView(SuccessMessageMixin, UpdateView):
    model = Tag
    form_class = TagForm
    success_url = reverse_lazy("todos:tags")
    success_message = 'Success update tag'

class TodosCreateAndListView(SuccessMessageMixin, CreateView):
    template_name = "todos/index.html"
    form_class = TodoForm
    model = Todo
    paginate_by = 5
    success_url = reverse_lazy("todos:index")
    success_message = 'Success create todo'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = self.request.GET.get('page', 1)
        todos = self.model.objects.filter(user_id=self.request.user, active=True).order_by('-id')
        paginator = Paginator(todos, self.paginate_by)
        todos = paginator.get_page(page)
        
        context["page_name"] = "index" 
        context["todos"] = todos               
        context["prev_url"] = todos.previous_page_number() if todos.has_previous() else None
        context["next_url"] = todos.next_page_number() if todos.has_next() else None

        return context
    
    def form_valid(self, form):
        form.instance.user_id = self.request.user
        # if form.instance.datetime_todo :
        #     form.instance.datetime_todo = form.instance.datetime_todo.utcnow()
        return super().form_valid(form)

    def get_initial(self):   
        initial = super().get_initial()            
        initial['tags_data'] = Tag.objects.filter(user_id=self.request.user)
        return initial


class TodoDeleteView(SuccessMessageMixin, DeleteView):
    model = Todo
    success_url = reverse_lazy("todos:index")
    success_message = 'Success delete todo'

class TodoUpdateView(SuccessMessageMixin, UpdateView):
    model = Todo
    form_class = TodoUpdateForm
    success_url = reverse_lazy("todos:index")
    success_message = 'Success update todo'

class TodoAchiveView(SuccessMessageMixin, UpdateView):
    model = Todo
    fields = ["active"]
    success_url = "/"
    success_message = 'Success archive todo'
    
    def form_valid(self, form):
        try :
            form.instance.active = not Todo.objects.get(id=form.instance.id).active
        except:
            form.instance.active = not form.instance.id
        return super().form_valid(form)

    def get_success_url(self) -> str:
        if self.kwargs.get("name") and self.kwargs.get("name") == "index":
            return reverse_lazy("todos:index")
        else :
            return reverse_lazy("todos:todos_archive")

class TodoArchiveView(ListView):
    template_name = "todos/index.html"
    model = Todo
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = self.request.GET.get('page', 1)
        todos = self.model.objects.filter(user_id=self.request.user, active=False).order_by('-id')
        paginator = Paginator(todos, self.paginate_by)
        todos = paginator.get_page(page)
        
        context["todos"] = todos  
        context["page_name"] = "archive"             
        context["prev_url"] = todos.previous_page_number() if todos.has_previous() else None
        context["next_url"] = todos.next_page_number() if todos.has_next() else None

        return context


def export_todos_csv(request):
    file_name = "todos_{}".format(request.user.username)
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="{}.csv"'.format(file_name)},
    )
    todos = Todo.objects.filter(user_id=request.user)
    writer = csv.writer(response)
    writer.writerow(['Todo', 'Active', 'Datetime', 'Tags'])
    for todo in todos:
        
        writer.writerow([todo.body, todo.active, todo.datetime_todo.strftime("%d-%m-%Y %H:%M:%S"), ",".join([tag.name for tag in todo.tags.all()])])

    return response


    
def import_todos_csv(request):
    try :
        if request.method == 'POST' and request.FILES['file']:
            print("a")
            csv_file = request.FILES["file"]
            file_data = csv_file.read().decode("utf-8")
            lines = file_data.split("\n")
            print(lines)
            for line in lines :
                if len(line)>0:
                    fields = line.split(",")
                    data_dict = {}
                    data_dict["body"] = fields[0]
                    data_dict["datetime_todo"] = fields[1]
                    try:
                        form = TodoForm(data_dict)
                        if form.is_valid():
                            form.instance.user_id = request.user
                            form.save()					
                        else :
                            print(form.errors)               
                    except Exception as e:
                        print(e)				
                        pass

            return redirect("todos:index")
        else :
            return redirect("todos:index")
    except Exception as e :
        print(e)
    

def export_and_email(request):
    file_name = "todos_{}".format(request.user.username)
    todos = Todo.objects.filter(user_id=request.user)
    csvfile = StringIO()
    writer = csv.writer(csvfile)
    writer.writerow(['Todo', 'Active', 'Datetime', 'Tags'])
    for todo in todos:        
        writer.writerow([todo.body, todo.active, todo.datetime_todo.strftime("%d-%m-%Y %H:%M:%S"), ",".join([tag.name for tag in todo.tags.all()])])
    
    email = render_to_string("todos/export_todo_email_template.txt", {"username" : request.user.username})
    message = EmailMessage("Export todo list csv",email,"alfatihridho@gmail.com",[request.user.email])
    message.attach(file_name, csvfile.getvalue(), 'text/csv')
    message.send()
    return redirect("todos:index")
