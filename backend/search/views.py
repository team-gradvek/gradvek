from django.shortcuts import render
from rest_framework import generics

from .models import Descriptor
from .serializers import DescriptorSerializer

# Create your views here.

# Collect data from database and format it to send back
#  to next.js
class DescriptorListView(generics.ListAPIView):
    queryset = Descriptor.objects.all()
    serializer_class = DescriptorSerializer