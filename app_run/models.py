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
    distance = models.FloatField(null=True)
    run_time_seconds = models.IntegerField(null=True, default=0,)

    def __str__(self):
        return f"id = {self.id} created_at = {self.created_at} comment = {self.comment} "


class AthleteInfo(models.Model):
    weight = models.IntegerField(null=True)
    goals = models.TextField(null=True)
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, related_name='athlete_info')

class Challenge(models.Model):
    full_name = models.TextField()
    athlete = models.ForeignKey(User, on_delete=models.CASCADE, related_name='challenges')

    def __str__(self):
        return (f"id = {self.id} full_name = {self.full_name} athlete ="
                f" {self.athlete}")


class Position(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    run = models.ForeignKey(Run, on_delete=models.CASCADE, related_name='positions')
    date_time = models.DateTimeField(null=True)

    def __str__(self):
        return (f"id = {self.id} latitude = {self.latitude} longitude = "
                f"{self.longitude} run = {self.run_id} date_time = {self.date_time}")

class CollectibleItem(models.Model):
    name = models.TextField()
    uid = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    picture = models.URLField()
    value = models.IntegerField()
    collitems = models.ManyToManyField(User,
                                       related_name='collectibleitems',
                                       blank=True)

    def __str__(self):
        return (f"id = {self.id} name = {self.name} uid = "
                f"{self.uid} latitude = {self.latitude} longitude = "
                f"{self.longitude} picture = {self.picture} value = {self.value}")