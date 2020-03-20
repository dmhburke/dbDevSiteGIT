from django.contrib import admin

# Register your models here.
from catalog.models import uploadImage, reportInput, restaurantRecord, transactionRecord, masterRecord

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

#===VIRTUAL COCKTAIL===

#Define admin class - create restaurant record
class restaurantRecordAdmin(admin.ModelAdmin):
     list_display = ('restaurant_name', 'venmo_details', 'contact_email')

# Register the admin class with the associated model
admin.site.register(restaurantRecord, restaurantRecordAdmin)

#Define admin class - create restaurant record
class transactionRecordAdmin(admin.ModelAdmin):
     list_display = ('date', 'restaurant_name', 'number_input', 'amount')

# Register the admin class with the associated model
admin.site.register(transactionRecord, transactionRecordAdmin)

class masterRecordAdmin(admin.ModelAdmin):
     list_display = ('restaurant_name', 'total_number', 'total_amount')

# Register the admin class with the associated model
admin.site.register(masterRecord, masterRecordAdmin)
