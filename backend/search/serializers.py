from rest_framework import serializers

from .models import Descriptor, Action
# from .models import Target
# from .models import AdverseEvent

# Collect data from database and format it to send back
#  to next.js
class DescriptorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Descriptor
        fields = ["name"]


class ActionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Action
        fields = ["action"]
        # fields = ["action", "count"]
