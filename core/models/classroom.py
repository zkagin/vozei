from django.db import models
from .base import BaseModel
from .user import User


class Classroom(BaseModel):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    members = models.ManyToManyField(User, related_name="classroom_membership")

    def __str__(self):
        return self.name


class Assignment(BaseModel):
    classroom = models.ForeignKey(Classroom, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=200)
    text = models.TextField()

    def __str__(self):
        return self.title
