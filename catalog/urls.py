from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    # ROTATE SELFIE IMAGES
    path('rotateimage', views.rotateimage, name='rotateimage'),
    #PLAY AUDIO FILES
    # - define synthesize_speech and define what to say
    path('pollyset', views.pollyset, name='pollyset'),
    # - page for playing audio
    path('pollyplay/<voice>', views.pollyplay, name='pollyplay'),
    # VIRTUAL COCKTAIL
    # - homepage
    path('cocktailhomepage', views.cocktailhomepage, name='cocktailhomepage'),
    # - restaurantDetail
    path('restaurantdetail/<restaurant_name>', views.restaurantdetail, name='restaurantdetail'),
    # - payment confirm
    path('paymentconfirm', views.paymentconfirm, name='paymentconfirm'),
    # - add restaurant
    path('submitrestaurant', views.submitrestaurant, name='submitrestaurant')
]
