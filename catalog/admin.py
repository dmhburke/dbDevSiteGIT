from django.contrib import admin

# Register your models here.
from catalog.models import uploadImage

#Define admin class - UPLOADIMAGES
class uploadImageAdmin(admin.ModelAdmin):
     list_display = ('uploadImage', 'pre_save', 'uploaded_at',)

# Register the admin class with the associated model
admin.site.register(uploadImage, uploadImageAdmin)
