from django.db import models

from neomodel import (
    StringProperty,
    StructuredNode,
    RelationshipTo,
    RelationshipFrom,
    Relationship,
    UniqueIdProperty
)


class Descriptor(models.Model):
    """
    Target Similarity indices, potential descriptors
    """
    descriptor_name = models.CharField(max_length=30)

# For Demo
class Target(models.Model):
    """
    Targets for Typeahead
    """
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=60)

# For Demo
class AdverseEvent(models.Model):
    """
    Adverse Events for Typeahead
    """
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=60)

