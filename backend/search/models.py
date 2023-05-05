from django.db import models


# Django models, contains fields and behaviors of the data


# Target Similarity indices, potential descriptors
#   Needs to be added manually on startup (Django admin)
class Descriptor(models.Model):
    name = models.CharField(max_length=30)


# On startup, Neo4j similarity score results 
#   must be saved to the database
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

class AverageSimilarity(NodeSimilarity):
    pass
