from django import forms
from django.core.exceptions import ValidationError

from catalog.choices import *

from catalog.models import uploadImage, reportInput, addRestaurant

class uploadImageForm(forms.ModelForm):
    uploadImage = forms.ImageField(required=True)

    class Meta:
        model = uploadImage
        fields = ('uploadImage',) #change back to uploadImage


from django.forms import ModelChoiceField

class UserModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
         return obj.player_name

class PollyForm(forms.Form):
    pollyVoice = forms.ChoiceField(choices=POLLYVOICES, required=True)
    playerInput = UserModelChoiceField(queryset=reportInput.objects.all(), required=False)

    def polly_voice_input(self,request):
        pollyVoiceSelect = self.cleaned_data['pollyVoice']
        return pollyVoiceSelect

    def player_input(self,request):
        playerSelect = self.cleaned_data['playerInput']
        return playerSelect

# === VIRTUAL COCKTAIL ===
from django import forms
from catalog.models import transactionRecord

YES_NO = (
("NO", "No"),
("YES", "Yes"),
)

class AddRestaurantForm(forms.ModelForm):
    restaurant_name = forms.CharField(required=True)
    is_yours = forms.ChoiceField(choices=YES_NO, required=False)
    phone_number = forms.CharField(required=True)
    email_address = forms.CharField(required=True)
    instagram_handle = forms.CharField(required=False)

    class Meta:
        model = addRestaurant
        fields = ('restaurant_name', 'is_yours', 'phone_number', 'email_address', 'instagram_handle',)


class OrderForm(forms.ModelForm):
    number_input = forms.IntegerField(label='', required=False)

    class Meta:
        model = transactionRecord
        fields = ('number_input',)


class RestaurantSearchForm(forms.Form):
    find_restaurant = forms.CharField(required=False)

    def search_input(self,request):
        restaurantSelect = self.cleaned_data['find_restaurant']
        return restaurantSelect
