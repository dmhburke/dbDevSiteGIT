import os
from django.db import models
from catalog.utilities import rotate_image
from django.urls import reverse
from io import BytesIO
from django.core.files import File
from PIL import Image, ExifTags
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.conf import settings
import boto3
from PIL import Image as Img
from exiffield.fields import ExifField


# Create your models here.
class uploadImage(models.Model):
    """Simple model for uploading images"""
    uploadImage = models.ImageField(upload_to='uploadImage', blank=True, null=True)
    pre_save = models.CharField(max_length=30, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        try:
            if self.uploadImage:
                pilImage = Img.open(BytesIO(self.uploadImage.read()))
                for orientation in ExifTags.TAGS.keys():
                    if ExifTags.TAGS[orientation] == 'Orientation':
                        break
                exif = dict(pilImage._getexif().items())

                if exif[orientation] == 3:
                    pilImage = pilImage.rotate(180, expand=True)
                elif exif[orientation] == 6:
                    pilImage = pilImage.rotate(270, expand=True)
                elif exif[orientation] == 8:
                    pilImage = pilImage.rotate(90, expand=True)

                output = BytesIO()
                pilImage.save(output, format='JPEG', quality=75)
                output.seek(0)
                self.uploadImage = File(output, self.uploadImage.name)
        except (AttributeError, KeyError, IndexError):
            # cases: image don't have getexif
            pass

        return super(uploadImage, self).save(*args, **kwargs)

@receiver(pre_save, sender=uploadImage)
def add_metadata(sender, instance, **kwargs):
    if instance.uploadImage:
        pre_save = 'success'
    else:
        pass


# # ROTATE IMAGE FUNCTION
# @receiver(post_save, sender=uploadImage, dispatch_uid="update_image_profile")
# def update_image(sender, instance, **kwargs):
#   if instance.uploadImage:
#       # # DEVELOPMENT
#       # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#       # MEDIA_CONVERTER = '/catalog/static'
#       # fullpath = BASE_DIR + MEDIA_CONVERTER + instance.uploadImage.url
#       # rotate_image(fullpath)
#
#       # PRODUCTION
#       # Download instance.uploadImage from S3 to temp folder
#       s3_client = boto3.client('s3')
#       bucket_name = settings.AWS_STORAGE_BUCKET_NAME
#       subfolder_name = 'media/'
#       target_image = str(instance.uploadImage)
#       image_path = subfolder_name + target_image
#       image_name = '/tmp/image.jpg'
#       # fullpath = temp_folder + target_image
#
#       s3_client.download_file(bucket_name, image_path, image_name)
#
#       # Rotate image in temp folder
#       rotate_image(image_name)
#
#       # Upload rotated image from temp folder back to S3
#       s3_client.upload_file(image_name, bucket_name, image_path)
