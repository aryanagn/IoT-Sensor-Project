# from django.shortcuts import render, redirect
# from django.http import HttpResponse
# from django.contrib.auth.models import User
# from django.contrib.auth import authenticate, login, logout
# from django.contrib import messages

# # Create your views here.
# def home(request):
#     return render(request,"users/home.html")

# def signup(request):
#     #verifying post request method
#     if request.method == "POST":
#         username = request.POST['username']
#         firstname = request.POST['firstname']
#         lastname = request.POST['lastname']
#         email = request.POST['email']
#         password = request.POST['password']
#         confirmPassword = request.POST['confirmPassword']
        
#         # Error checking for account creation
#         errors = []
#         if len(username) == 0 or len(firstname) == 0 or len(lastname) == 0 or len(email) == 0 or len(password) == 0:
#             errors.append("Fields cannot be empty")
            
#         elif User.objects.filter(username=username):
#             errors.append("Username already in use")
           
#         elif User.objects.filter(email=email).exists():
#             errors.append("Email already in use")
            
#         elif password != confirmPassword:
#             errors.append("Passwords do not match")
        
#         elif not username.isalnum():
#             errors.append("Username must be Alpha-Numeric")
        
#         if errors:
#             for error in errors:
#                 messages.error(request, error)
#             return redirect('signup')
#         else:
#             # creating user object and saving it
#             user = User.objects.create_user(username, email, password)
#             user.first_name = firstname
#             user.last_name = lastname
#             user.save()

#             # message for successful account creation
#             messages.success(request, "Your Account has been successfully created.")
#             return redirect('signin')

#     return render(request, "users/signup.html")

# def signin(request):
#     if request.method == "POST":
#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         user = authenticate(request, username=username, password=password)
        
#         if user is not None:
#             login(request, user)
#             return redirect('home')
#         else:
#             messages.error(request, "Username or password is incorrect")
#             return redirect('signin')   
    
#     return render(request, "users/signin.html")
# def signout(request):
#     logout(request)
#     return redirect('home')


# Passage by 1Password integration backend
from passageidentity import Passage
from django.http import JsonResponse
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
import json

PASSAGE_APP_ID = "YOUR_APP_ID"  # Replace with your actual Passage App ID
PASSAGE_API_KEY = "YOUR_API_KEY"  # Replace with your actual Passage API Key
# Ensure you replace the above with your actual Passage credentials, I took them out due to security reasons.

# Correct initialization: use variables, not string literals
passage = Passage(app_id=PASSAGE_APP_ID, api_key=PASSAGE_API_KEY)

@csrf_exempt
def passage_auth_callback(request):
    if request.method == "POST":
        auth_token = request.POST.get("auth_token")
        if not auth_token:
            return JsonResponse({"status": "error", "message": "No auth token provided"})

        try:
            # Authenticate the token
            user_id = passage.auth.validate_jwt(auth_token)
            
            if user_id:
                # Get user information from Passage
                user_info = passage.user.get(user_id)
                
                # Extract email from user info
                email = user_info.email if hasattr(user_info, 'email') else None
                if not email:
                    return JsonResponse({"status": "error", "message": "No email found in user info"})
                
                # Get or create a corresponding Django user
                user, created = User.objects.get_or_create(
                    username=email,
                    defaults={
                        'email': email,
                        'first_name': getattr(user_info, 'first_name', ''),
                        'last_name': getattr(user_info, 'last_name', ''),
                    }
                )
                
                # Log in user via Django session
                login(request, user)
                return JsonResponse({"status": "success", "user": user.username})
            else:
                return JsonResponse({"status": "error", "message": "Invalid token"})
        except Exception as e:
            print(f"Passage auth error: {str(e)}")  # For debugging
            return JsonResponse({"status": "error", "message": f"Authentication failed: {str(e)}"})
    
    return JsonResponse({"status": "error", "message": "Invalid request method"})

# Views for templates

def home(request):
    return render(request,"users/home.html")

def signup(request):
    return render(request, "users/signup.html")

def signin(request):
    return render(request, "users/signin.html")

def signout(request):
    logout(request)
    return redirect('homePage')