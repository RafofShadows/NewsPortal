from django.db import models

from django.contrib.auth.models import User
from django.urls import reverse


# Create your models here.
class Author(models.Model):
    rating = models.IntegerField(default=0)
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)

    def update_rating(self):
        res = 0
        for post in Post.objects.filter(author=self.pk):
            res += post.rating * 3
            for comment in Comment.objects.filter(post=post.pk):
                res += comment.rating
        for comment in Comment.objects.filter(user_id=self.user_id):
            res += comment.rating
        self.rating = res
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)


News = 'NEW'
Article = 'ART'
TYPES = [
    (News, 'Новость'),
    (Article, 'Статья')
]


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=3, choices=TYPES, default='ART')
    timestamp = models.DateTimeField(auto_now_add=True)
    header = models.CharField(max_length=255, default='')
    text = models.TextField(default='')
    rating = models.IntegerField(default=0)

    categories = models.ManyToManyField(Category, through='PostCategory')

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[:124] + '...'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.pk)])

    def __str__(self):
        return f"{self.header}\n{self.text}"


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(default='')
    timestamp = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
