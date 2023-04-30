from django.db import models


class Descriptor(models.Model):
    """
    Target Similarity indices, potential descriptors
    """
    name = models.CharField(max_length=30)


class Action(models.Model):
    action = models.CharField(max_length=30, null=True, blank=True)
    count = models.IntegerField( null=True, blank=True)

class NodeSimilarity(models.Model):
    target1 = models.CharField(max_length=100)
    target2 = models.CharField(max_length=100)
    similarity = models.FloatField()

class MousePheno(NodeSimilarity):
    pass

class Hgene(NodeSimilarity):
    pass

class Hprotein(NodeSimilarity):
    pass

class Intact(NodeSimilarity):
    pass

class Pathway(NodeSimilarity):
    pass

class Reactome(NodeSimilarity):
    pass

class Signor(NodeSimilarity):
    pass

class Gwas(NodeSimilarity):
    pass
