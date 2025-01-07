from django.db import models

# Create your models here.
class Profile(models.Model):
    profile_picture  = models.ImageField(upload_to="proifle_pic/")
