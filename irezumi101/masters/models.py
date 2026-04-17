from django.db import models
from django.urls import reverse

class Studio(models.Model):
    name = models.CharField(max_length=150, verbose_name="Название студии")
    address = models.CharField(max_length=255, verbose_name="Адрес (Город)")

    class Meta:
        verbose_name = "Студия"
        verbose_name_plural = "Студии"
    def __str__(self):
        return self.name

class Master(models.Model):
    name = models.CharField(max_length=255, verbose_name="Имя мастера")
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    century = models.IntegerField(verbose_name="Век")
    bio = models.TextField(blank=True, verbose_name="Биография")
    studio = models.OneToOneField(Studio, on_delete=models.SET_NULL, null=True, blank=True, related_name='master',
                                  verbose_name="Студия")
    objects = models.Manager()

    class Meta:
        ordering = ['century', 'name']
        verbose_name = "Мастер"
        verbose_name_plural = "Мастера"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('master', kwargs={'master_slug': self.slug})