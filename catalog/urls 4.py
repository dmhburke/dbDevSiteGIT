from django.urls import path
from . import views

urlpatterns = [
    # ROTATE SELFIE IMAGES
    path('rotateimage', views.rotateimage, name='rotateimage'),

    #PLAY AUDIO FILES
    # - define synthesize_speech and define what to say
    path('pollyset', views.pollyset, name='pollyset'),
    # - page for playing audio
    path('pollyplay', views.pollyplay, name='pollyplay'),
]
