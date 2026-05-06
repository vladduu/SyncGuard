from django.db import models

# Create your models here.
class SyncLog(models.Model):
    original_name = models.CharField(max_length=255)
    encrypted_name = models.CharField(max_length=255)
    file_size = models.BigIntegerField() 
    timestamp = models.DateTimeField(auto_now_add=True) 
    status = models.CharField(max_length=50, default="Success")

    def __str__(self):
        return f"{self.original_name} -> {self.encrypted_name}"