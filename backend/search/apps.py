from django.apps import AppConfig
from . import startup_functions


class SearchConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "search"

# https://stackoverflow.com/questions/6791911/execute-code-when-django-starts-once-only
# Startup function appear to hook in here?
    def ready(self):
        
        # Call your startup functions here
        startup_functions.check_and_load_data()