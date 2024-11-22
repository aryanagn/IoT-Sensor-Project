from django.template import loader
from django.shortcuts import render, redirect
from django.http import HttpResponse

def sensingGang(request):
    return render(request, "homePage/homePage.html")

def homePage(request):
    return redirect('homePage')