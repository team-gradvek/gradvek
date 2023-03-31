from rest_framework import serializers

from .models import Descriptor

# Collect data from database and format it to send back
#  to next.js
class DescriptorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Descriptor
        fields = ["descriptor_name"]