
# Create your models here.
from django.db import models
from django.conf import settings
import helper.billing

# Create your models here.

User = settings.AUTH_USER_MODEL #"auth.user"

#OntoOneField because we only want one stripe customer per one user
# models.CASCADE makes it so if the User is deleted then so is their customer number

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stripe_id = models.CharField(max_length=120, null=True, blank=True)


    def __str__(self):
        return f"{self.user.username}"

    def save(self, *args, **kwargs):
        
        
        if not self.strip_id:
            email = self.user.email
            if email != "" or email is not None:

                stripe_id = helper.billing.create_customer(email= email, raw=True)
                self.strip_id = stripe_id
        

        super().save(*args, **kwargs)