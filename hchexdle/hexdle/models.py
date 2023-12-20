from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from hashlib import md5
from os import getenv

class Contestant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    hash = models.CharField(max_length=256)
    rattempts = models.IntegerField(default=int(getenv('DJANGO_ATTEMPTS')))

    def __str__(self):
        return "{user}".format(user=self.user)

@receiver(post_save, sender=User)
def create_contestant(sender, instance, created, **kwargs):
    if created:
        Contestant.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_contestant(sender, instance, **kwargs):
    instance.contestant.hash = md5(bytes(instance.username+getenv('DJANGO_SALT'), 'utf-8')).hexdigest()[int(getenv('DJANGO_FIRST_CHAR')):int(getenv('DJANGO_FIRST_CHAR'))+int(getenv('DJANGO_COLS'))]
    instance.contestant.save()
