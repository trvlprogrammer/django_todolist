from rest_framework import serializers
from .models import Todo, Tag

class TodoItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = '__all__'


class TagItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

