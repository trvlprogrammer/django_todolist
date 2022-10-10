from datetime import datetime
from django import forms
from .models import Tag, Todo

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields=('name',)


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields=('body','datetime_todo','tags')

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        if kwargs.get("initial") :
            self.fields['tags'].queryset = kwargs.get("initial").get("tags_data")
            self.fields['tags'].widget.attrs.update({'class':'form-control widget-many2many-tags'})

class TodoUpdateForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields=('body','datetime_todo')