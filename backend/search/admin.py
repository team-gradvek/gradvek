from django.contrib import admin

from .models import Descriptor, MousePheno



class DescriptorsAdmin(admin.ModelAdmin):
    list_display = ("name",)

class NodeSimilarityMousePhenoAdmin(admin.ModelAdmin):
    list_display = ("target1", "target2", "similarity")



# class TargetsAdmin(admin.ModelAdmin):
#     list_display = ("name", "description")

# class AdverseEventsAdmin(admin.ModelAdmin):
#     list_display = ("name", "description")

# Renders Descriptors class to the admin page
admin.site.register(Descriptor, DescriptorsAdmin)
admin.site.register(MousePheno, NodeSimilarityMousePhenoAdmin)
