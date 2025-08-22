from django.shortcuts import render
from rest_framework.views import APIView 
from rest_framework import viewsets
from rest_framework.response import Response 
from .models import Note
from django.contrib.auth.models import User
from .serializer import NoteSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.http import JsonResponse
from helper.billing import start_checkout_session
from customer.models import Customer 


# Create your views here.

class NoteListCreateView(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [AllowAny]

class UserListCreateView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class create_checkout_session_view(APIView):

    #ModelViewSet is meant for full CRUD on a django model(listing, creating, updating)
    #This isnt a model, its just triggering a Stripe session
    #best to use APIView from DRF 
    permission_classes = [AllowAny]



  

    def post(self, request):

        if request.user.is_authenticated:
            print("User is logged in:", request.user.username)
        else:
            print("Anonymous user")

        print("Authenticated user object:", request.user)


        
       
      
        try:
            customer = Customer.objects.get(user=request.user)
            #this queries the local database and assumes there is a model called customer
            #it finds the customer object that is associated with the authenticated user (request.user), the "user" in user=request.user comes from the customer model 
            #can do customer.stripe_customer_id to get the stripe id from local database 
        except Customer.DoesNotExist:
            return Response({'error': 'Customer not found'}, status=404)
        
        stripe_id = customer.stripe_id

        if not stripe_id:
            return Response({'error': "missing stripe_id"}, status=404)
        
        #Get line items from request 

        line_items = request.data.get('line_items')
        if not line_items:
            return Response({'error': 'Missing line_items'}, status=400)
        
        success_url = request.data.get('success_url', 'https://yourdomain.com/success')
        cancel_url = request.data.get('cancel_url', 'https://yourdomain.com/cancel')

        #call helper function to create the Stripe Checkout session 
        try:
            session = start_checkout_session(
                customer_id=customer.stripe_id,
                success_url=success_url,
                cancel_url=cancel_url,
                line_items = line_items,
            )
            return Response({'checkout_url': session.url})
        except Exception as e:
            return Response({'error': str(e)}, status=500)

        
        
        #this pulls customer_id from the request body(data sent in an API request (json))
        #this assumes the frontend or third-party-app is sending the customer_id in the request 


        #something like Customer.objects.get(stripe_customer_id=request.stripe_customer_id) isnt safe
        #stripe_customer_id is just a string like "cus_123abc" from stripe, this gets stored in the customer model as CharField
        #so doing customer.objects.get(stripe_customer_id='cus_123abc') this a valid query but the issue is where that ID comes from 
        #user is a Django User objects, django attaches request.user to every request automatically after the user logs in via sessions or tokens
        #customer.objects.get(user=request.user) is clean and secure because no user input 
