from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Author(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    country = models.CharField(max_length=255)
    biography = models.TextField()

    def __str__(self):
        return self.name


class Book(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=100)
    author = models.ManyToManyField(Author, blank=True)
    category = models.ManyToManyField(Category, blank=True)
    summary = models.TextField()

    def __str__(self):
        return self.name
