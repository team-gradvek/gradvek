import os
from django.apps import AppConfig

from gradvekbackend.startup import wait_for_neo4j_connection
from gradvekbackend.startup import run_startup_tasks
class SearchConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "search"

    def ready(self):
        # This hooks into the startup process of Django
        # and runs the startup tasks defined in
        # gradvekbackend.startup
        
        # Only run startup tasks in processes not spawned by the autoreloader
        # https://stackoverflow.com/a/28504072
        if os.environ.get('RUN_MAIN') != 'true':
            run_startup_tasks()
        else:
            # If the application is started by the autoreloader, it still needs the Neo4j connection to be established
            wait_for_neo4j_connection()


