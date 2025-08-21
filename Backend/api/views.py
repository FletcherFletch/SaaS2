from django.shortcuts import render
from rest_framework.views import APIView 
from rest_framework import viewsets
from rest_framework import Response 
from .models import Note
from django.contrib.auth.models import User
from .serializer import NoteSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.http import JsonResponse
from helper.billing import start_checkout_session


# Create your views here.

class NoteListCreateView(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [AllowAny]

class UserListCreateView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class create_checkout_session_view(APIView):

    #ModelViewSet is meant for full CRUD on a django model(listing, creating, updating)
    #This isnt a model, its just triggering a Stripe session
    #best to use APIView from DRF 

    def post(self, request):

        response = start_checkout_session()
        return Response({'checkout_url': response.url})
    