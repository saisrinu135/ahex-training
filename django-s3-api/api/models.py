from django.db import models
from storages.backends.s3boto3 import S3Boto3Storage
# Create your models here.


class Profile(models.Model):
    name = models.CharField(max_length=20)
    age = models.IntegerField()
    email = models.EmailField(max_length=50)
    image = models.ImageField(upload_to='profiles', storage=S3Boto3Storage())
    gender = models.CharField(max_length=10)