from django.db import models
from django.contrib.auth.models import User
from slugify import slugify
from unidecode import unidecode
from django.urls import reverse
import uuid

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Назва')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Назва')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Вміст')
    slug = models.SlugField(max_length=200, unique=True, blank=True, verbose_name='URL')
    categories = models.ManyToManyField(Category, related_name='articles', verbose_name='Категорії')
    tags = models.ManyToManyField(Tag, related_name='articles', verbose_name='Теги')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Створено')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles', verbose_name='Автор')

    def save(self, *args, **kwargs):
        unique_id = str(uuid.uuid4())
        transliterated_title = unidecode(self.title)
        self.slug = slugify(transliterated_title) + '-' + unique_id[:8]
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('article_detail', kwargs={'article_slug':self.slug})

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Стаття'
        verbose_name_plural = 'Статті'
