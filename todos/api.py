from .models import Todo, Tag
from rest_framework import permissions, viewsets, generics
from .serializers import TodoItemSerializer, TagItemSerializer


class TodoItemViewset(viewsets.ModelViewSet):
    permission_classes = [        
        permissions.IsAuthenticated
    ]
    serializer_class = TodoItemSerializer

    def get_queryset(self):
        return Todo.objects.filter(user_id=self.request.user, active=True)

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)

class TodoItemArchiveViewset(viewsets.ModelViewSet):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = TodoItemSerializer

    def get_queryset(self):
        return Todo.objects.filter(user_id=self.request.user, active=False)


class TagItemViewset(viewsets.ModelViewSet):
    permission_classes = [        
        permissions.IsAuthenticated
    ]
    serializer_class = TagItemSerializer

    def get_queryset(self):
        return Tag.objects.filter(user_id=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)