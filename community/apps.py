from django.apps import AppConfig

class CommunityConfig(AppConfig):
    name = 'community'
    
    def ready(self): #method just to import the signals
        import community.signals