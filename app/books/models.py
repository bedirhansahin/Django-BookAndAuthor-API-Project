from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    name = models.CharField(max_length=100, null=True)
    slug = models.SlugField(max_length=100, unique=True, null=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=100, null=True)
    slug = models.SlugField(max_length=100, unique=True, null=True)
    date_of_birth = models.DateField()
    country = models.CharField(max_length=255)
    books = models.ManyToManyField('Book', related_name='books', null=True, blank=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    name = models.CharField(max_length=100, null=True)
    slug = models.SlugField(max_length=100, unique=True, null=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category)
    summary = models.TextField()

    def __str__(self):
        return self.name
