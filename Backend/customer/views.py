from django.shortcuts import render

# Create your views here.
from django.conf import settings
from django.shortcuts import render
# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
import stripe
from helper import billing
from .models import Customer
from rest_framework.permissions import AllowAny
import stripe
import os


stripe.api_key = os.getenv('STRIPE_SECRET_KEY')


class CustomerCreate(APIView):

    permission_classes = [AllowAny]

        #Need to use permission class because of settings i used

    def post(self, request):

        #when defining a method on a class the first argument must be self
        #refers to instance of the class
        # this is saying self = the instance of CreateCustomer
        # request = the HTTP request (an isntance of Request from DRF)
        # Django routes to class-based views like
        #view_instance = CreateCustomer()
        # response = view_instance.post(request)

        name = request.data.get('name')
        email = request.data.get('email')

        if not name or not email:
            return Response({'error': 'Name and email are required'}, status=400)

        stripe_response = billing.create_customer(name=name, email=email, raw=True)

        return Response({
            'name': stripe_response.get('name'),
            'stripe_customer_id': stripe_response.get('id'),
        })

    def get(self, request):
        email = request.query_params.get('email')

        if not email:
            return Response({'error': 'email is required'}, status=400)

        try:
            #name = request.data.get('name')
            #email = request.data.get('email')
            #stripe_response = billing.create_customer(name=name, email=email, raw=True)
            #These are wrong because request.data is meant for POST, PUT.. ETC
            #in GET request, data should come from query parameters
            #create_customer is a write operations, should not be done in a GET request


            customer = Customer.objects.get(user_email=email)
            # This sets the variable customer to a Customer model instance that matches the provided email
            # not storing the email in the variable
            # using the email to look up the corresponding customer

            stripe_customer = stripe.Customer.retrieve(customer.strip_id)

            return Response ({
              'name': stripe_customer.name,
              'stripe_customer_id': stripe_customer.id,
              'email': stripe_customer.email,
            })

        except Customer.DoesNotExist:
            return Response({"error"})

        except Exception as e:
            return Response({'err'})
