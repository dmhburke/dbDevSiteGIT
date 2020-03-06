from django.urls import path
from . import views

urlpatterns = [
    path('rotateimage', views.rotateimage, name='rotateimage'),

    #test golf report`
    path('pollyset', views.pollyset, name='pollyset'),

    path('pollytest', views.pollytest, name='pollytest'),
]
