from django import forms
from django.core.exceptions import ValidationError

from catalog.models import uploadImage

class uploadImageForm(forms.ModelForm):
    uploadImage = forms.ImageField(required=True)

    class Meta:
        model = uploadImage
        fields = ('uploadImage',) #change back to uploadImage
