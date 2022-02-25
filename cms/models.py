from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

from django.utils.text import slugify

from tinymce.models import HTMLField


class Category(models.Model):
    category = models.CharField(max_length=100,
                                verbose_name="Blog Category")
    slug = models.SlugField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['category']

    def __str__(self):
        return f'{self.category}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.category)
        return super().save(*args, **kwargs)


class Post(models.Model):
    publisher = models.ForeignKey(User, on_delete=models.CASCADE,
                                  related_name='published_user')
    title = models.CharField(max_length=150, verbose_name='Post Title')
    slug = models.SlugField(blank=True, null=True)
    category = models.ManyToManyField(Category)
    content = HTMLField()
    likes = models.ManyToManyField(User, blank=True, null=True, related_name='user_likes')
    like_count = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Posts'
        ordering = ['-created']

    def __str__(self) -> str:
        return f'{self.title} - {self.created}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(self, *args, **kwargs)


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='reviewer')
    review = models.TextField()
    likes = models.ManyToManyField(User, blank=True, null=True,
                                   related_name='reviewer_likes')
    like_count = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Reviews'
        ordering = ['-created']

    def __str__(self) -> str:
        return f'{self.review} - {self.created}'


