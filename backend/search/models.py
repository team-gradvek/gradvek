from django.db import models

# Create your models here.

class Descriptor(models.Model):
    """
    Target Similarity indices, potential descriptors
    """
    descriptor_name = models.CharField(max_length=30)

class Target(models.Model):
    """
    Targets for Typeahead
    """
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=60)

class AdverseEvent(models.Model):
    """
    Adverse Events for Typeahead
    """
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=60)