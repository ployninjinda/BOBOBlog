from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255 , unique=True) #ความยาวตัวอักษร,ชื่อบทความห้ามซ้ำกัน

    def __str__(self):
        return str(self.name)