from django.db import models

# Create your models here.

class Descriptor(models.Model):
    """
    Target Similarity indices, potential descriptors
    """
    descriptor_name = models.CharField(max_length=30)