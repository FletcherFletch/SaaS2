from django.db import models
import helper.billing
from django.db import models
from django.db.models import Q
from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_save
from django.conf import settings 
from django.urls import reverse
from django.utils import timezone
import datetime

User = settings.AUTH_USER_MODEL

ALLOW_CUSTOM_GROUPS = True
SUBSCRIPTION_PERMISSIONS = [
    ("advanced", "Advanced Perm"), # subscriptions.advanced
    ("pro", "Pro Perm"),  # subscriptions.pro
    ("basic", "Basic Perm"),  # subscriptions.basic,
    ("basic_ai", "Basic AI Perm")
]

class Subscription(models.Model):
    name = models.CharField(max_length=120)
    subtitle = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)
    groups = models.ManyToManyField(Group) # one-to-one
    permissions =  models.ManyToManyField(Permission, limit_choices_to={
        "content_type__app_label": "subscriptions", "codename__in": [x[0]for x in SUBSCRIPTION_PERMISSIONS]
        }
    )
    stripe_id = models.CharField(max_length=120, null=True, blank=True)

    order = models.IntegerField(default=-1, help_text='Ordering on Django pricing page')
    featured = models.BooleanField(default=True, help_text='Featured on Django pricing page')
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    features = models.TextField(help_text="Features for pricing, seperated by new line", blank=True, null=True)


    def __str__(self):
        return f"{self.user.username}"

    class meta: 
        ordering = ['order', 'featured', '-updated']
        permissions = SUBSCRIPTION_PERMISSIONS
    
    
    def save(self, *args, **kwargs):
        
        if not self.stripe_id:
            stripe_id = helper.billing.create_product(name=self.name, metadata={
                "subscription_plan_id": self.id
            }, raw = False)
            
            self.stripe_id = stripe_id
        super().save(*args, **kwargs)

class SubscriptionPrice(models.Model):

    class IntervalChoices(models.TextChoices):
        MONTHLY = "month", "Monthly"
        YEARLY = "year", "Annual"

    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, null=True)
    
    stripe_id = models.CharField(max_length=120, null=True, blank=True)
    interval = models.CharField(max_length=120, default=IntervalChoices.MONTHLY,
                                choices=IntervalChoices.choices)
    
    price = models.DecimalField(max_digits=10, decimal_places=2, default=99.99)

    #property is python decorator that lets you defind a method that behaves like a read only attribute 
    # lets you do thing.product_stripe_id  Looks like an attribute...
    # but its actually calling a method 
    #thing.product_stripe_id()  # ← but you don't write the ()!
    #makes code look cleaner and more intuitive 

    @property
    def stripe_price(self):
        return self.price * 100

    @property
    def stripe_currency(self):
        return "usd"

    @property
    def product_stripe_id(self):
        if not self.subscription:
            return None
        return self.subscription.stripe_id
    
    def save(self, *args, **kwargs):
        if (not self.stripe_id and self.product_stripe_id is not None):
            
            stripe_id = helper.billing.create_price(
                currency=self.stripe_currency,
                unit_amount=self.stripe_price,
                interval=self.interval,
                
                product=self.product_stripe_id,
                metadata={
                    "subscription_plan_price_id": self.id
                },
                raw = False
            )
            self.stripe_id = stripe_id
        super().save(*args, **kwargs)
