from django.apps import AppConfig

class SearchConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "search"

    def ready(self):
        # put your startup code here
        from gradvekbackend.startup import run_startup_tasks
        run_startup_tasks()


