from rest_framework import serializers

from .models import (
    Descriptor, 
    MousePheno, 
    Hgene, 
    Hprotein, 
    Intact, 
    Pathway, 
    Reactome, 
    Signor, 
    Gwas
)


# Translate Django models into other text-based format

class DescriptorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Descriptor
        fields = ["name"]

class NodeSimilaritySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["target1", "target2", "similarity"]

class MousePhenoSerializer(NodeSimilaritySerializer):
    class Meta:
        model = MousePheno
        fields = ["target1", "target2", "similarity"]

class HgeneSerializer(NodeSimilaritySerializer):
    class Meta:
        model = Hgene
        fields = ["target1", "target2", "similarity"]

class HproteinSerializer(NodeSimilaritySerializer):
    class Meta:
        model = Hprotein
        fields = ["target1", "target2", "similarity"]

class IntactSerializer(NodeSimilaritySerializer):
    class Meta:
        model = Intact
        fields = ["target1", "target2", "similarity"]

class PathwaySerializer(NodeSimilaritySerializer):
    class Meta:
        model = Pathway
        fields = ["target1", "target2", "similarity"]

class ReactomeSerializer(NodeSimilaritySerializer):
    class Meta:
        model = Reactome
        fields = ["target1", "target2", "similarity"]

class SignorSerializer(NodeSimilaritySerializer):
    class Meta:
        model = Signor
        fields = ["target1", "target2", "similarity"]

class GwasSerializer(NodeSimilaritySerializer):
    class Meta:
        model = Gwas
        fields = ["target1", "target2", "similarity"]

class AverageSimilaritySerializer(serializers.Serializer):
    target2 = serializers.CharField()
    average_similarity = serializers.FloatField()

class AverageNodeSimilaritySerializer(serializers.Serializer):
    target1 = serializers.CharField()
    target2 = serializers.CharField()
    average = serializers.FloatField()
    descriptors = serializers.ListField(child=serializers.CharField())