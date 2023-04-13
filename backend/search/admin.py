from django.contrib import admin

from .models import Descriptor
from .models import Target
from .models import AdverseEvent


class DescriptorsAdmin(admin.ModelAdmin):
    list_display = ("name",)

class TargetsAdmin(admin.ModelAdmin):
    list_display = ("name", "description")

class AdverseEventsAdmin(admin.ModelAdmin):
    list_display = ("name", "description")

class TargetsAdmin(admin.ModelAdmin):
    list_display = ("name", "description")

class AdverseEventsAdmin(admin.ModelAdmin):
    list_display = ("name", "description")

# Renders Descriptors class to the admin page
admin.site.register(Descriptor, DescriptorsAdmin)
