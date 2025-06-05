from django.contrib import admin
from .models import APIKey

@admin.register(APIKey)
class APIKeyAdmin(admin.ModelAdmin):
    list_display = ('user', 'key', 'created_at', 'is_active', 'usage_count')
    list_filter = ('is_active', 'created_at')
    search_fields = ('user__username', 'user__email', 'key')
    readonly_fields = ('key', 'created_at', 'usage_count')
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            return self.readonly_fields + ('user',)
        return self.readonly_fields
