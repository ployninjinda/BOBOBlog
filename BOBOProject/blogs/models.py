from django.db import models
from category.models import Category

# Create your models here.
class Blogs(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    content = models.TextField()
    category = models.ForeignKey(Category,on_delete=models.CASCADE) #ถ้ายังมีบทความที่เกี่ยวกับหมวดหมู่นั้นอยู่ จะไม่สามารถลบหมวดหมู่นั้นทิ้งได้
    writer = models.CharField(max_length=255)
    views = models.IntegerField(default=0) #ยอดวิวเริ่มต้นที่0
    image = models.ImageField(upload_to="blogsImages",blank=True) #รูปปกจะใส่หรือไม่ก็ได้
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)


