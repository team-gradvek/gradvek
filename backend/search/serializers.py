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

# TODO inheritence class with Model Serializer ?
# class MousePhenoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = MousePheno
#         fields = ["target1", "target2", "similarity"]

class NodeSimilaritySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["target1", "target2", "similarity"]

class MousePhenoSerializer(NodeSimilaritySerializer):
    class Meta:
        model = MousePheno
        fields = ["target2", "similarity"]
        # fields = '__all__'

class HgeneSerializer(NodeSimilaritySerializer):
    class Meta:
        model = Hgene
        fields = ["target2", "similarity"]

class HproteinSerializer(NodeSimilaritySerializer):
    class Meta:
        model = Hprotein
        fields = ["target2", "similarity"]

class IntactSerializer(NodeSimilaritySerializer):
    class Meta:
        fields = ["target2", "similarity"]

class PathwaySerializer(NodeSimilaritySerializer):
    class Meta:
        model = Pathway
        fields = ["target2", "similarity"]

class ReactomeSerializer(NodeSimilaritySerializer):
    class Meta:
        model = Reactome
        fields = ["target2", "similarity"]

class SignorSerializer(NodeSimilaritySerializer):
    class Meta:
        model = Signor
        fields = ["target2", "similarity"]

class GwasSerializer(NodeSimilaritySerializer):
    class Meta:
        model = Gwas
        fields = ["target2", "similarity"]