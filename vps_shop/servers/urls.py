from tkinter.font import names

from django.urls import path, include
from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('about/', about, name='about'),
    path('vps/', vps_collection, name='vps_collection'),
    path('vps/<int:uid>', vps_target, name='vps_target')
]