from django.db import models
from ckeditor.fields import RichTextField

class Recipe(models.Model):
    name         = models.CharField(max_length=200)
    difficulty   = models.CharField(max_length=100)
    instructions = RichTextField()
    image        = models.ImageField(upload_to='recipes/')
    created_at   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
