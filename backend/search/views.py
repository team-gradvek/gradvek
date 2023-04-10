from django.shortcuts import render
from rest_framework import generics

from .models import Descriptor
from .serializers import DescriptorSerializer

from .models import Target
from .serializers import TargetSerializer

from .models import AdverseEvent
from .serializers import AdverseEventSerializer

# Create your views here.

# Collect data from database and format it to send back
#  to next.js
class DescriptorListView(generics.ListAPIView):
    queryset = Descriptor.objects.all()
    serializer_class = DescriptorSerializer

class TargetListView(generics.ListAPIView):
    queryset = Target.objects.all()
    serializer_class = TargetSerializer

class AdverseEventListView(generics.ListAPIView):
    queryset = AdverseEvent.objects.all()
    serializer_class = AdverseEventSerializer