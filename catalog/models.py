import os
from django.db import models
from catalog.utilities import rotate_image
from django.urls import reverse
from io import BytesIO
from django.core.files import File
from PIL import Image, ExifTags
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings


# Create your models here.
class uploadImage(models.Model):
    """Add description explaining what model does"""
    # uploadImage = models.ImageField(upload_to='uploadImage', blank=True, null=True)
    # uploaded_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    # rotateImage = models.ImageField(upload_to='rotateImage', blank=True, null=True)
    uploadImage = models.ImageField(upload_to='uploadImage', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='rotateImage', blank=True, null=True)

@receiver(post_save, sender=uploadImage, dispatch_uid="update_image_profile")
def update_image(sender, instance, **kwargs):
  if instance.uploadImage:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    MEDIA_CONVERTER = '/catalog/static'
    fullpath = BASE_DIR + MEDIA_CONVERTER + instance.uploadImage.url

    rotate_image(fullpath)
