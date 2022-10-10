from django.views.generic import (
    CreateView,
    DeleteView, 
    UpdateView
    )
from .models import Tag, Todo 
from .forms import TagForm, TodoForm, TodoUpdateForm
from django.urls import reverse_lazy
from django.core.paginator import Paginator


class TagsCreateAndListView(CreateView):
    template_name = "todos/tags.html"
    form_class = TagForm
    model = Tag
    paginate_by = 5
    success_url = reverse_lazy("todos:tags")

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

class TagDeleteView(DeleteView):
    model = Tag
    success_url = reverse_lazy("todos:tags")

class TagUpdateView(UpdateView):
    model = Tag
    form_class = TagForm
    success_url = reverse_lazy("todos:tags")

class TodosCreateAndListView(CreateView):
    template_name = "todos/index.html"
    form_class = TodoForm
    model = Todo
    paginate_by = 5
    success_url = reverse_lazy("todos:index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = self.request.GET.get('page', 1)
        todos = self.model.objects.filter(user_id=self.request.user, active=True).order_by('-id')
        paginator = Paginator(todos, self.paginate_by)
        todos = paginator.get_page(page)
        
        context["todos"] = todos               
        context["prev_url"] = todos.previous_page_number() if todos.has_previous() else None
        context["next_url"] = todos.next_page_number() if todos.has_next() else None

        return context
    
    def form_valid(self, form):
        form.instance.user_id = self.request.user
        if form.instance.datetime_todo :
            form.instance.datetime_todo = form.instance.datetime_todo.utcnow()
        return super().form_valid(form)

    def get_initial(self):   
        initial = super().get_initial()            
        initial['tags_data'] = Tag.objects.filter(user_id=self.request.user)
        return initial

class TodoDeleteView(DeleteView):
    model = Todo
    success_url = reverse_lazy("todos:index")

class TodoUpdateView(UpdateView):
    model = Todo
    form_class = TodoUpdateForm
    success_url = reverse_lazy("todos:index")


    