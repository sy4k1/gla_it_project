from django.db import models
from django.utils.timezone import now

# Create your models here.
class Account(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100, db_index=True)
    # sha512 with salt
    password = models.CharField(max_length=500, db_index=True)
    role = models.CharField(max_length=20)
    bio = models.TextField()
    avatar = models.CharField(max_length=1000)
    wallpaper = models.CharField(max_length=1000)
    create_datetime = models.DateTimeField(default=now, blank=True, editable=False)


class AccountAccessToken(models.Model):
    account_email = models.EmailField(db_index=True)
    # uuid as user access token
    access_token = models.CharField(db_index=True, max_length=100)
    create_datetime = models.DateTimeField(default=now, blank=True, editable=False)


class AccountPasscode(models.Model):
    account_email = models.EmailField(db_index=True)
    passcode = models.CharField(max_length=10, db_index=True)
    create_datetime = models.DateTimeField(default=now, blank=True, editable=False)


class Follower(models.Model):
    follower_email = models.EmailField(db_index=True)
    followed_email = models.EmailField(db_index=True)
    read = models.BooleanField(default=False)
    create_datetime = models.DateTimeField(default=now, blank=True, editable=False)
