from django.db import models
from django.contrib.auth.models import User
import secrets
import string

class APIKey(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='api_key')
    key = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    usage_count = models.IntegerField(default=0)
    
    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_api_key()
        super().save(*args, **kwargs)
    
    @staticmethod
    def generate_api_key():
        """Generate a secure random API key"""
        alphabet = string.ascii_letters + string.digits
        return 'sk_' + ''.join(secrets.choice(alphabet) for _ in range(48))
    
    def __str__(self):
        return f"API Key for {self.user.username}"
    
    class Meta:
        verbose_name = "API Key"
        verbose_name_plural = "API Keys"
