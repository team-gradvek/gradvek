from rest_framework import serializers

from .models import Descriptor
from .models import Target
from .models import AdverseEvent

# Collect data from database and format it to send back
#  to next.js
class DescriptorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Descriptor
        fields = ["descriptor_name"]

class TargetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Target
        fields = ["name", "description"]

class AdverseEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = AdverseEvent
        fields = ["name", "description"]