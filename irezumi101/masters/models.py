from django.db import models
from django.urls import reverse


class Master(models.Model):
    name = models.CharField(max_length=255, verbose_name="Имя мастера")
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    century = models.IntegerField(verbose_name="Век")
    bio = models.TextField(blank=True, verbose_name="Биография")

    objects = models.Manager()

    class Meta:
        ordering = ['century', 'name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('master', kwargs={'master_slug': self.slug})