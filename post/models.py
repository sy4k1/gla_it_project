from django.db import models
from django.utils.timezone import now

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    content = models.TextField()
    images = models.CharField(max_length=2000)
    poster_email = models.EmailField(db_index=True)
    likes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    channel = models.CharField(max_length=100, db_index=True)
    create_datetime = models.DateTimeField(default=now, blank=True, editable=False)


class LikedPost(models.Model):
    liked_account_email = models.EmailField(db_index=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    poster_email = models.EmailField(db_index=True)
    read = models.BooleanField(default=False)
    create_datetime = models.DateTimeField(default=now, blank=True, editable=False)


class Comment(models.Model):
    parent_comment_id = models.BigIntegerField(db_index=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    poster_email = models.EmailField(db_index=True)
    commentator_email = models.EmailField(db_index=True)
    comment = models.TextField()
    read = models.BooleanField(default=False)
    create_datetime = models.DateTimeField(default=now, blank=True, editable=False)
