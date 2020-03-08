from django import forms
from django.core.exceptions import ValidationError

from catalog.choices import *

from catalog.models import uploadImage, reportInput

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
