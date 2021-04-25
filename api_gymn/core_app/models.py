from django.db import models
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager
from django.contrib.auth.models import User


class PostWorkout(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название тренировки')
    slug = models.SlugField(max_length=255, verbose_name='Url', unique=True)
    description = RichTextUploadingField(verbose_name='Начало контента')
    content = RichTextUploadingField(verbose_name='Продолжение контента')
    image = models.ImageField(upload_to='image/%Y/%m/%d/', blank=True, verbose_name='Фото/изображение')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано?')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тренировка(у)'
        verbose_name_plural = 'Тренировки'


class PostContent(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    slug = models.SlugField(max_length=255, verbose_name='Slug', unique=True)
    description = RichTextUploadingField(verbose_name='Начало контента')
    content = RichTextUploadingField(verbose_name='Продолжение контента')
    image = models.ImageField(upload_to='image/%Y/%m/%d/', blank=True, verbose_name='Фото/изображение')
    created_at = models.DateField(default=timezone.now, verbose_name='Дата публикации')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Имя автроа поста')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    tag = TaggableManager(verbose_name='Тэги', help_text='Введите теги через запятую')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-created_at']


class Comment(models.Model):
    post = models.ForeignKey(PostContent, on_delete=models.CASCADE, related_name='comments')
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_name')
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return self.text


