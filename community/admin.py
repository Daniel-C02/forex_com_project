from django.contrib import admin
from .models import Trade, UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    readonly_fields = ('dateregistered',)

admin.site.register(Trade)
admin.site.register(UserProfile, UserProfileAdmin)
