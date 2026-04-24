from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .models import Contact
from .serializers import ContactSerializer


class ContactViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [AllowAny]

from django.shortcuts import render

# Create your views here.
