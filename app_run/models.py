from django.db import models
from django.contrib.auth.models import User
from django.core import validators


# Create your models here.
class Run(models.Model):
    STATUS_CHOICES = [
        ('init', 'init'),
        ('in_progress', 'in_progress'),
        ('finished', 'finished'),
    ]
    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()
    athlete = models.ForeignKey(User, on_delete=models.CASCADE, related_name='runs')
    status = models.CharField(choices=STATUS_CHOICES,default='init')

    def __str__(self):
        return f"id = {self.id} created_at = {self.created_at} comment = {self.comment} "


class AthleteInfo(models.Model):
    weight = models.IntegerField(null=True)
    goals = models.TextField(null=True)
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, related_name='athlete_info')
