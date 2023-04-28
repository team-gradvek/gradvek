from django.apps import AppConfig

class SearchConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "search"

    def ready(self):
        # This hooks into the startup process of Django
        # and runs the startup tasks defined in
        # gradvekbackend.startup
        from gradvekbackend.startup import run_startup_tasks
        run_startup_tasks()


