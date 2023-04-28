from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
from . import restapis
from . import models

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.
def home(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/index.html', context )

# Create an `about` view to render a static about page
def about(request):
    '''Displays company's mission and responsibilities'''
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/about.html', context)

# Create a `contact` view to return a static contact page
def contact(request):
    """Displays contact info to potential clients"""
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    '''Authenicates users' login requests'''
    context = {}
    # Handles POST request
    if request.method == "POST":
        # Get username and password from request.POST dictionary
        username = request.POST['username']
        password = request.POST['psw']
        # Try to check if provide credential can be authenticated
        user = authenticate(username=username, password=password)
        if user is not None:
            # If user is valid, call login method to login current user
            login(request, user)
            return redirect('/djangoapp/')
        # user is presence
        else:
            # If not, return to login page again
            return render(request, 'djangoapp/user_login.html', context)
    # serves get requests
    else:
        return render(request, 'djangoapp/user_login.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    '''logout users if authenticated and return to home page.'''
    # Get the user object based on session id in request
    print("Log out the user `{}`".format(request.user.username))
    # Logout user in the request
    logout(request)
    # Redirect user back to course list view
    return redirect('/djangoapp/')

    # Create a `registration_request` view to handle sign up request
def registration_request(request):
    '''Collect users' info for signup purposes only.'''
    context = {}
    # If it is a GET request, just render the registration page
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    # If it is a POST request
    elif request.method == 'POST':
        # Get user information from request.POST
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            # Check if user already exists
            User.objects.get(username=username)
            user_exist = True
        except:
            # If not, simply log this as a new user
            logger.debug("{} is new user".format(username))
        # If it is a new user
        if not user_exist:
            # Create user in auth_user table
            user = User.objects.create_user(username=username, first_name=first_name, 
                                            last_name=last_name, password=password)
            # Login the user and redirect to course list page
            login(request, user)
            return redirect('/djangoapp/')
        else:
            return render(request, 'djangoapp/registration.html', context)

