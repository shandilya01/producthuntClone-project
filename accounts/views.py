from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
# Create your views here.

def signup(request):
    if request.method == 'POST':
        # if user wants to add something to the database
        if request.POST['password1']==request.POST['password2']:
            try:
                user = User.objects.get(username = request.POST['username']);
                return render(request, 'accounts/signup.html', {'error': 'Username already there'});
            except User.DoesNotExist:
                user = User.objects.create_user(request.POST['username'], password = request.POST['password1']);
                # creating a new User in databse if the pre-conditions hold true
                # and redirecting to the hime page
                auth.login(request, user);
                return redirect('home');
        else:
            return render(request, 'accounts/signup.html', {'error': 'Passwords dont match'});

    else:
        # if user wants something from the database using a 'GET' request.
        return render(request, 'accounts/signup.html');


def login(request):
    if request.method == 'POST':
        # login the user
        user = auth.authenticate(username = request.POST['username'] , password = request.POST['password']);
        if user is not None:
            auth.login(request, user);
            return redirect('home');
        else:
            return render(request, 'accounts/login.html', {'error': 'Account Does Not Exist'});
    else:
        return render(request, 'accounts/login.html');

def logout(request):
    if request.method == 'POST':
        auth.logout(request);
        return redirect('home');
