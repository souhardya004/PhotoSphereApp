
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Photo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to='photos/')
    uploaded_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
    
class Photo_category(models.Model):
    Photo_category_Types = [
        ('Nature', 'Nature'),
        ('Portrait', 'Portrait'),
        ('Architecture', 'Architecture'),
        ('Street', 'Street'),
        ('Wildlife', 'Wildlife'),
        ('Abstract', 'Abstract'),
        ]
    title = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='category')
    category_types = models.CharField(max_length=20, choices=Photo_category_Types)

    def __str__(self):
        return self.category_types