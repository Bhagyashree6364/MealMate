from django.apps import AppConfig


class DeliveryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'delivery'

# In delivery/apps.py (in DeliveryConfig class)

def ready(self):
    import delivery.signals

