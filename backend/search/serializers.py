from rest_framework import serializers

from .models import Descriptor, Action,  MousePheno, Hgene, Hprotein, Intact, Pathway, Reactome, Signor, Gwas
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




class MousePhenoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MousePheno
        fields = ["target1", "target2", "similarity"]

# TODO parent child with Model Serializer ?

# class NodeSimilaritySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = MousePheno
#         fields = ["target1", "target2", "similarity"]

# class NodeSimilaritySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = MousePheno
#         fields = ["target1", "target2", "similarity"]
# class MousePhenoSerializer(NodeSimilaritySerializer):
#     pass

# class MousePhenoSerializer(NodeSimilaritySerializer):
#     pass