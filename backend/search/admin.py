from django.contrib import admin

from .models import Descriptor


class DescriptorsAdmin(admin.ModelAdmin):
    list_display = ("name",)

# Renders Descriptors class to the admin page
admin.site.register(Descriptor, DescriptorsAdmin)
