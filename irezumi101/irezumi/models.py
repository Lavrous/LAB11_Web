# irezumi/models.py
from django.db import models
from django.urls import reverse


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Motif.Status.PUBLISHED)

class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Категория")
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

class TagPost(models.Model):
    tag = models.CharField(max_length=100, db_index=True, verbose_name="Тег")
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.tag
    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug': self.slug})


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

    views_count = models.IntegerField(default=0, verbose_name="Просмотры")
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, null=True, related_name='motifs',
                            verbose_name="Категория")
    tags = models.ManyToManyField('TagPost', blank=True, related_name='motifs', verbose_name="Теги")
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