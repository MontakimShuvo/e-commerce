from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from accounts.forms import CustomUserRegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

from accounts.utils import send_verification_email
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import  urlsafe_base64_decode
from accounts.models import CustomUser

@login_required
def user_dashboard(request):
    user = request.user

    if request.method == 'POST':
        # Update user profile
        user.email = request.POST.get('email',user.email)
        user.mobile = request.POST.get('mobile', user.mobile)
        user.address_line_1 = request.POST.get('address_line_1', user.address_line_1)
        user.address_line_2 = request.POST.get('address_line_2', user.address_line_2)
        user.city = request.POST.get('city', user.city)
        user.state = request.POST.get('state', user.state)
        user.country = request.POST.get('country', user.country)
        user.save()
        
        return redirect('profile')
    
    context = { 'user_info': user }
    return render(request, 'accounts/profile.html', context)

def signup(request):
    if request.method == 'POST':
        print("request.POST", request.POST)
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_user = authenticate(
                request,
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password1']
            )
            print("auth_user", auth_user)
            if auth_user is not None:
                login(request, auth_user)
                messages.success(request, 'Account created successfully!')
                return redirect('user_dashboard')
            else:
                print("Authentication failed for user:", user.email)
        else:
            print("form.errors", form.errors)
    else:
        form = CustomUserRegistrationForm()
    
    return render(request, 'accounts/sign-up.html')


def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have Successfully logged in.')
            return redirect('profile')
        else:
            messages.error(request, 'Invalid email or password.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'accounts/login.html',{ 'form': form })

@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'You have Successfully logged out.')
    return redirect('login')

def verify_email(request, uidb64, token):
    try:
        pk = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser.objects.get(pk=pk)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_verified = True
        user.save()
        messages.success(request, 'Your email has been verified. You can now log in.')
        return redirect('login')
    else:
        messages.error(request, 'Invalid verification link.')
        return redirect('signup')
