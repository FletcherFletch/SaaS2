from django.db import models
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
# Create your models here.


class Note(models.Model):
    title = models.CharField(max_length=200)
    content = models.CharField(max_length=300)

    def __str__(self):
        return(self.title)
    

    