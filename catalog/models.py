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
import boto3


# Create your models here.
class uploadImage(models.Model):
    """Simple model for uploading images"""
    uploadImage = models.ImageField(upload_to='uploadImage', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    # rotateImage = models.ImageField(upload_to='rotateImage', blank=True, null=True)
    # uploadImage = models.ImageField(upload_to='uploadImage', blank=True, null=True)
    # thumbnail = models.ImageField(upload_to='rotateImage', blank=True, null=True)

# ROTATE IMAGE FUNCTION
@receiver(post_save, sender=uploadImage, dispatch_uid="update_image_profile")
def update_image(sender, instance, **kwargs):
  if instance.uploadImage:
      # # DEVELOPMENT
      # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
      # MEDIA_CONVERTER = '/catalog/static'
      # fullpath = BASE_DIR + MEDIA_CONVERTER + instance.uploadImage.url
      #
      # rotate_image(fullpath)

      # PRODUCTION
      # Download instance.uploadImage from S3 to temp folder
      s3_client = boto3.client('s3')
      bucket_name = settings.AWS_STORAGE_BUCKET_NAME
      subfolder_name = 'media/'
      target_image = str(instance.uploadImage)
      image_path = subfolder_name + target_image
      image_name = '/tmp/image.jpg'
      # fullpath = temp_folder + target_image

      s3_client.download_file(bucket_name, image_path, image_name)

      # Rotate image in temp folder
      rotate_image(image_name)

      # Upload rotated image from temp folder back to S3
      s3_client.upload_file(image_name, bucket_name, image_path)
