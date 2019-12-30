from django.urls import path
from . import views

urlpatterns = [
    path('rotateimage', views.rotateimage, name='rotateimage'),
]
