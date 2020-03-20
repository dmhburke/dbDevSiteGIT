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
      # DEVELOPMENT
      BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
      MEDIA_CONVERTER = '/catalog/static'
      fullpath = BASE_DIR + MEDIA_CONVERTER + instance.uploadImage.url

      rotate_image(fullpath)

      # # PRODUCTION
      # # Download instance.uploadImage from S3 to temp folder
      # s3_client = boto3.client('s3')
      # my_bucket = settings.AWS_STORAGE_BUCKET_NAME
      # target_image = instance.uploadImage
      # temp_folder = '/tmp/'
      # full_path = temp_folder + target_image
      #
      # s3_client.download_file(my_bucket, target_image, fullpath)
      #
      # # Rotate image in temp folder
      # rotate_image(fullpath)
      #
      # # Upload rotated image from temp folder back to S3
      # s3_client.upload_file(fullpath, my_bucket, target_image)

# SYNTHESIZE SPEECH FUNCTION
class reportInput(models.Model):
    player_name = models.CharField(max_length=50, blank=True, null=True)
    input_one = models.CharField(max_length=50, blank=True, null=True)

    def __unicode__(self):
         return self.player_name


# === VIRTUAL COCKTAIL ===

class addRestaurant(models.Model):
    restaurant_name = models.CharField(max_length=100, blank=True, null=True)
    is_yours = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    instagram_handle = models.CharField(max_length=50, blank=True, null=True)
    email_address = models.CharField(max_length=50, blank=True, null=True)

class restaurantRecord(models.Model):
    restaurant_name = models.CharField(max_length=50, blank=True, null=True)
    background_image = models.ImageField(upload_to='vcUploadImage', blank=True, null=True)
    venmo_details = models.CharField(max_length=100, blank=True, null=True)
    contact_email = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.restaurant_name

class transactionRecord(models.Model):
    date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    restaurant_name = models.ForeignKey('restaurantRecord', on_delete=models.CASCADE, blank=True, null=True)
    number_input = models.IntegerField(blank=True, null=True)
    amount = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)

class masterRecord(models.Model):
    restaurant_name = models.ForeignKey('restaurantRecord', on_delete=models.CASCADE, blank=True, null=True)
    total_number = models.IntegerField(blank=True, null=True)
    total_amount = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)

@receiver (post_save, sender=restaurantRecord)
def add_restaurant(sender, instance, **kwargs):

    masterRecord.objects.update_or_create(
    restaurant_name=instance,
    defaults = {
    'total_number': 0,
    'total_amount': 0,
    })

@receiver (post_save, sender=transactionRecord)
def add_total(sender, instance, **kwargs):

    # Increment transaction number and amount into the master totals
    old_number = masterRecord.objects.get(restaurant_name=instance.restaurant_name).total_number
    instance_number = instance.number_input
    old_amount = masterRecord.objects.get(restaurant_name=instance.restaurant_name).total_amount
    instance_amount = instance.amount

    new_number = old_number + instance_number
    new_amount = old_amount + instance_amount

    masterRecord.objects.update_or_create(
    restaurant_name=instance.restaurant_name,
    defaults = {
    'total_number': new_number,
    'total_amount': new_amount,
    })

# class userList(models.Model):
#     first_name
#     last_name
#     user_name
