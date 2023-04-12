from django.db import models

from neomodel import (
    StringProperty,
    StructuredNode,
    RelationshipTo,
    RelationshipFrom,
    Relationship,
    UniqueIdProperty,
    IntegerProperty,
    config
)

class Descriptor(models.Model):
    """
    Target Similarity indices, potential descriptors
    """
    name = models.CharField(max_length=30)


class Action(models.Model):
    action = models.CharField(max_length=30)
    count = models.IntegerField()

