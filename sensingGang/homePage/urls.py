from django.urls import path
from . import views

urlpatterns = [
    path('', views.homePage, name='homePage'),
    path('button/', views.button_view, name='button'),
]