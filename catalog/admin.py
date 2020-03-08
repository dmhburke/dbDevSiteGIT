from django.contrib import admin

# Register your models here.
from catalog.models import uploadImage, reportInput

#Define admin class - UPLOADIMAGES
class uploadImageAdmin(admin.ModelAdmin):
     list_display = ('uploadImage', 'uploaded_at',)

# Register the admin class with the associated model
admin.site.register(uploadImage, uploadImageAdmin)



#Define admin class - REPORTINPUT
class reportInputAdmin(admin.ModelAdmin):
     list_display = ('player_name', 'input_one',)

# Register the admin class with the associated model
admin.site.register(reportInput, reportInputAdmin)
