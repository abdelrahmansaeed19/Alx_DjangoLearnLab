from django.apps import AppConfig


class RelationshipAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'relationship_app'

def ready(self):
    import relationship_app.signals  # Import the signals module to ensure signal handlers are registered
    # This will ensure that the signal handlers are connected when the app is ready
    # and will not cause any issues with circular imports.