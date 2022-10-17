from django.db import models
from django.contrib.auth.models import User

class Tag(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    class Meta:
       indexes = [
            models.Index(fields=['user_id',]),
            models.Index(fields=['name',])
        ]

    def __str__(self):
        return self.name

class Todo(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.CharField(max_length=200)
    datetime_todo = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=True)
    tags = models.ManyToManyField(Tag, blank=True)

    class Meta:
       indexes = [
            models.Index(fields=['user_id',]),
            models.Index(fields=['active',]),
            models.Index(fields=['datetime_todo',]),
        ]

    def __str__(self):
        return self.body

