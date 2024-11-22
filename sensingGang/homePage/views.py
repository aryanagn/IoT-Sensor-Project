from django.shortcuts import render, redirect
from django.http import HttpResponse
from subscribe.views import show_data, generate_data

def homePage(request):
    # set context with call to show_data function from subscribe.views
    context = show_data(request)
    return render(request, "homePage/homePageTemplate.html", context)

def button_view(request):
    # generate "live" data
    generate_data()
    
    # set context with call to show_data function from subscribe.views
    context = show_data(request)
    return render(request, 'homePage/homePageTemplate.html', context)
