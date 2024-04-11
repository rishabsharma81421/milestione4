from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,'base.html')

from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from .forms import UserRegisterForm
 
def register_user(request):
    if request.user.is_authenticated:
        return redirect("home")
 
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            password1 = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')
 
            # Check if email already exists
            if User.objects.filter(email=email).exists():
                messages.error(request, "Email is already registered.")
                return redirect('register')
 
            # Check if username already exists
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username is already taken.")
                return redirect('register')
 
            # Compare passwords
            if password1 != password2:
                messages.error(request, "Passwords do not match.")
                return redirect('register')
            
            # All validations passed, save the user
            user = form.save()
            messages.success(request, f'Account created for {username}!')
            login(request, user)
            return redirect('login_user')
        
        return render(request, 'test.html', {'form': form})
 
    else:
        form = UserRegisterForm()
    return render(request, 'test.html', {'form': form})
 
 
 
def login_user(request):
    if request.user.is_authenticated:
        return redirect("home")
 
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
 
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request,"Username doesn't exist")
 
        user = authenticate(request, username=username, password=password)
        if user is not None:
            print("user logged in ::::::::::::::::::::::::::::::;;")
            login(request, user)
            return redirect ('home')
        else:
             messages.error(request,"Username or Password is incorrect")
 
    return render(request , 'login.html')
 
def logout_user(request):
    logout(request)
    messages.error(request,"User successfully logged out ")
    return redirect('login_user')
 