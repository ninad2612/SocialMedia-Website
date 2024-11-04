from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Profile

def register_page(request):
    if request.method == "POST":
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        username = request.POST.get('username')
        password = request.POST.get('password')
        bio = request.POST.get('bio')
        dob = request.POST.get('dob')
        profile_picture = request.FILES.get('profile_picture')

        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username Taken")
            return redirect('/register/')  # Redirect back to registration

        # Create a new user
        user = User(
            username=username,
            first_name=firstname,
            last_name=lastname,
        )
        user.set_password(password)  # Hash the password
        user.save()

        # Create the associated Profile
        Profile.objects.create(
            user=user,
            bio=bio,
            dob=dob,
            profile_picture=profile_picture
        )

        messages.success(request, "Registration successful! You can now log in.")
        return redirect('/login/')  # Redirect to login page after successful registration

    return render(request, 'register.html')

# accounts/views.py
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages

def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  # Log the user in
            return redirect('/home/')  # Redirect to home page
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('/login/')  # Redirect back to login if authentication fails

    return render(request, 'login.html')

from django.contrib.auth import logout

def logout_page(request):
    logout(request)  # Log the user out
    return redirect('/login/')


