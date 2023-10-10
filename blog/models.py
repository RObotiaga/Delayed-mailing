from django.db import models
from django.utils.text import slugify


class BlogPost(models.Model):
    title = models.CharField(max_length=200, verbose_name='название')
    slug = models.CharField(max_length=200, unique=True, verbose_name='slug')
    content = models.TextField(verbose_name='содержание')
    preview_image = models.ImageField(upload_to='blog_images/', verbose_name='превью')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    is_published = models.BooleanField(default=True, verbose_name='статус публикации')
    views_count = models.PositiveIntegerField(default=0, verbose_name='количество просмотров')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'пост'
        verbose_name_plural = 'посты'

    def add_view(self):
        self.views_count += 1
        self.save()

    def save(self, *args, **kwargs):
        # Генерируем slug из заголовка поста
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
