from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

# Create your views here.
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You logged in successfully.")
            return redirect('issues')
        else:
            messages.error(request,"Username or password is incorrect.")
            return render(request, 'accounts/login.html', {})
    else:
        return render(request, 'accounts/login.html', {})

def logout_view(request):
    logout(request)
    return redirect('login')