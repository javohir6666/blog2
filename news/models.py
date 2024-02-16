from django.db import models
from ckeditor.fields import RichTextField
from django.utils import timezone
from autoslug import AutoSlugField

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=200)
    category_image = models.ImageField(upload_to='category-img/')
    slug = AutoSlugField(populate_from='title')
    tranding = models.BooleanField(default=False)
    class Meta:
        verbose_name_plural='Categories'

    def __str__(self):
        return self.title

#TAG
class Tag(models.Model):
    name = models.CharField(max_length=35)
    slug = AutoSlugField(populate_from='name')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# Post [News]
class News(models.Model):
    id = models.AutoField
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    slug = AutoSlugField(populate_from='title')
    image = models.ImageField(upload_to='news-img/', blank=True)
    detail = RichTextField()
    add_time = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, blank=True, null=True)
    post_viewcount = models.PositiveIntegerField(default=0,)
    seo_keywords = models.CharField(max_length=300)
    seo_description = models.TextField()
    
    def publish(self):
        self.add_time = timezone.now()
        self.save()

    class Meta:
        verbose_name_plural='News'
        ordering = ['-add_time',]

    def __str__(self):
        return self.title