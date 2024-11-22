from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('sensorList', views.sensorList, name='sensorList'),
    path('sensorRemove', views.sensorRemove, name='sensorRemove'),    
    path('subscribeForm', views.subscribeForm, name='subscribeForm'),
    path('unsubscribeForm', views.unsubscribeForm, name='unsubscribeForm'),
]
