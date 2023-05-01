from django.contrib import admin

from .models import  (
    Descriptor, 
    MousePheno,
    Hgene,
    Hprotein,
    Intact,
    Pathway,
    Reactome,
    Signor,
    Gwas,
    )

# Create admin classes for the Django admin page
class DescriptorsAdmin(admin.ModelAdmin):
    list_display = ("name",)

class MousePhenoAdmin(admin.ModelAdmin):
    list_display = ("target1", "target2", "similarity")

class HgeneAdmin(admin.ModelAdmin):
    list_display = ("target1", "target2", "similarity")

class HproteinAdmin(admin.ModelAdmin):
    list_display = ("target1", "target2", "similarity")

class IntactAdmin(admin.ModelAdmin):
    list_display = ("target1", "target2", "similarity")

class PathwayAdmin(admin.ModelAdmin):
    list_display = ("target1", "target2", "similarity")

class ReactomeAdmin(admin.ModelAdmin):
    list_display = ("target1", "target2", "similarity")

class SignorAdmin(admin.ModelAdmin):
    list_display = ("target1", "target2", "similarity")

class GwasAdmin(admin.ModelAdmin):
    list_display = ("target1", "target2", "similarity")

# Render Model classes to the admin page
admin.site.register(Descriptor, DescriptorsAdmin)
admin.site.register(MousePheno, MousePhenoAdmin)
admin.site.register(Hgene, HgeneAdmin)
admin.site.register(Hprotein, HproteinAdmin)
admin.site.register(Intact, IntactAdmin)
admin.site.register(Pathway, PathwayAdmin)
admin.site.register(Reactome, ReactomeAdmin)
admin.site.register(Signor, SignorAdmin)
admin.site.register(Gwas, GwasAdmin)
