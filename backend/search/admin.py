from django.contrib import admin

# Register your models here.
from .models import Descriptor
from .models import Target
from .models import AdverseEvent

class DescriptorsAdmin(admin.ModelAdmin):
    list_display = ("descriptor_name",)

class TargetsAdmin(admin.ModelAdmin):
    list_display = ("name", "description")

class AdverseEventsAdmin(admin.ModelAdmin):
    list_display = ("name", "description")

# Renders Descriptors class to the admin page
admin.site.register(Target, TargetsAdmin)
admin.site.register(Descriptor, DescriptorsAdmin)
admin.site.register(AdverseEvent, AdverseEventsAdmin)