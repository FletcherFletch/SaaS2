from django.shortcuts import render
from rest_framework import viewsets
from .models import Note
from django.contrib.auth.models import User
from .serializer import NoteSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny


# Create your views here.

class NoteListCreateView(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [AllowAny]

class UserListCreateView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]