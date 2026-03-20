# irezumi/models.py
from django.db import models
from django.urls import reverse


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Motif.Status.PUBLISHED)


class Motif(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    title = models.CharField(max_length=255, verbose_name="Название мотива")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL-слаг")
    content = models.TextField(blank=True, verbose_name="Легенда и значение")

    image = models.CharField(max_length=255, blank=True, default='', verbose_name="Путь к картинке")

    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")

    is_published = models.BooleanField(
        choices=Status.choices,
        default=Status.PUBLISHED,
        verbose_name="Статус публикации"
    )

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create']),
        ]
        verbose_name = "Мотив"
        verbose_name_plural = "Мотивы"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('motif', kwargs={'motif_slug': self.slug})