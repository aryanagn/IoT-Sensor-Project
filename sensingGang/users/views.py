from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


# Create your views here.
def home(request):
    return render(request,"users/home.html")

def signup(request):
    #verifying post request method
    if request.method == "POST":
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        confirmPassword = request.POST['confirmPassword']
        
        # Error checking for account creation
        errors = []
        if len(username) == 0 or len(firstname) == 0 or len(lastname) == 0 or len(email) == 0 or len(password) == 0:
            errors.append("Fields cannot be empty")
            
        elif User.objects.filter(username=username):
            errors.append("Username already in use")
           
        elif User.objects.filter(email=email).exists():
            errors.append("Email already in use")
            
        elif password != confirmPassword:
            errors.append("Passwords do not match")
        
        elif not username.isalnum():
            errors.append("Username must be Alpha-Numeric")
        
        if errors:
            for error in errors:
                messages.error(request, error)
            return redirect('signup')
        else:
            # creating user object and saving it
            user = User.objects.create_user(username, email, password)
            user.first_name = firstname
            user.last_name = lastname
            user.save()

            # message for successful account creation
            messages.success(request, "Your Account has been successfully created.")
            return redirect('signin')

    return render(request, "users/signup.html")

def signin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username or password is incorrect")
            return redirect('signin')   
    
    return render(request, "users/signin.html")
def signout(request):
    logout(request)
    return redirect('home')

