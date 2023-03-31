from django.contrib import admin

# Register your models here.
from .models import Descriptor

class DescriptorsAdmin(admin.ModelAdmin):
    list_display = ("descriptor_name",)

# Renders Descriptors class to the admin page
admin.site.register(Descriptor, DescriptorsAdmin)