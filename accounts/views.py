from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from .models import CustomUser
from django.views.decorators.csrf import csrf_exempt

def user_dashboard(request):
    user = request.user

    context = {
        'user_info': user,
    }
    return render(request, 'accounts/user_dashboard.html',context)

def signup(request):
    if request.method == 'POST':
        # Extract data from POST request using IDs
        full_name = request.POST.get('fullname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # validate the data
        if not full_name or not email or not password:
            messages.error(request, 'All fields are required.')
            return redirect('signup')
        
        # Check if the email already exists
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "A user with that email already exists.")
            print("Error: A user with that email already exists.\n\n")
            return redirect('signup')

        try:
            # Create a new user
            user = CustomUser.objects.create_user(username=full_name, email=email, password=password)
            user.is_verified = False  # Assuming you have an email verification process
            user.save()

            messages.success(request, "Registration successful. Please verify your email.")
            
            current_site = get_current_site(request)
            verification_link = f"http://{current_site.domain}/accounts/verify/{urlsafe_base64_encode(force_bytes(user.pk))}/{default_token_generator.make_token(user)}"
            
            send_verification_email(user,verification_link)
            return redirect('login')
        except Exception as e:
            # Log the exception and show an error message
            print(f"Error creating user: {e}")
            messages.error(request, "An error occurred while creating the account. Please try again.")
            return redirect('signup')
    elif request.method == 'GET':
        return render(request, 'accounts/sign-up.html') 


