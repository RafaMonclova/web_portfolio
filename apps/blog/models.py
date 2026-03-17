from django.db import models
from django.utils.text import slugify
from tinymce.models import HTMLField

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = HTMLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey('users.User', on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            # Genera el slug automáticamente a partir del título
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)