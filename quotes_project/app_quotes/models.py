import json

from django.contrib.auth import admin
from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Author(models.Model):
    fullname = models.CharField(max_length=255)
    born_date = models.CharField(max_length=255)
    born_location = models.CharField(max_length=255)
    description = models.TextField(null=True)

    def __str__(self):
        return f"{self.fullname}"


class Tag(models.Model):
    tag = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"{self.tag}"


class Quote(models.Model):
    tags = models.ManyToManyField(Tag)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    quote = models.TextField()


    def __str__(self):
        return f"{self.quote}"



