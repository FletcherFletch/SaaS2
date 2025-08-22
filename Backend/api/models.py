from django.db import models
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.models import User
# Create your models here.


class djUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=225)


class Note(models.Model):
    title = models.CharField(max_length=200)
    content = models.CharField(max_length=300)

    def __str__(self):
        return(self.title)
    

    