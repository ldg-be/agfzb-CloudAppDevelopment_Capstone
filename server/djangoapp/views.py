from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .restapis import get_dealers_from_cf, get_dealer_by_id_from_cf, post_review, get_dealer_reviews_from_cf
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.
# Create an `about` view to render a static about page
def about(request):
    return render(request, 'djangoapp/about.html')


# Create a `contact` view to return a static contact page
def contact(request):
    return render(request, 'djangoapp/contact.html')

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/login.html', context)
    else:
        return render(request, 'djangoapp/login.html', context)


# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')
    

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    #context = get_dealers_from_cf()
    #print(context)
    if request.method == "GET":
        url = "https://eu-de.functions.appdomain.cloud/api/v1/web/ba16a567-bf8b-4e08-8345-2742a032caf3/dealership-package/get-dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        context["dealerships"] = dealerships
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        #return HttpResponse(dealer_names)
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        context = {"dealership": dealer_id}
        #dealerId = request.GET['dealerId']
        url = "https://eu-de.functions.appdomain.cloud/api/v1/web/ba16a567-bf8b-4e08-8345-2742a032caf3/djangoapp/get-reviews"
        reviews = get_dealer_reviews_from_cf(url, dealerId=dealer_id)
        context["reviews"] = reviews
        review_names = ' '.join([review.sentiment for review in reviews])
        # Return a list of reviewers names
        #return HttpResponse(review_names)
        return render(request, 'djangoapp/dealer_details.html', context)
    elif request.method == "POST":
        post_review({
            'dealership': int(request.POST['dealership']),
            'id': int(request.POST['id']),
            "name": "Upkar Lidder",
            "review": "Great service!",
            "purchase": false,
            "another": "field",
            "purchase_date": "02/16/2021",
            "car_make": "Audi",
            "car_model": "Car",
            "car_year": 2021
        })
        return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    context = {'dealer_id': dealer_id}
    #check if authenticated
    user = request.user
    print(user)
    if not user.is_authenticated:
        print("user is not authenticated")
        return render(request, 'djangoapp/index.html', context)
    
    if request.method == "GET":
        return render(request, 'djangoapp/add_review.html', context)
    
    elif request.method == 'POST':
        url = "https://eu-de.functions.appdomain.cloud/api/v1/web/ba16a567-bf8b-4e08-8345-2742a032caf3/djangoapp/get-reviews"
        review = {
            'dealership': dealer_id,
            "name": str(user),
            "review": request.POST["review"],
            "another": "field",
            "purchase_date": "02/16/2021",
            "car_make": "Audi",
            "car_model": "Car",
            "car_year": 2021
        }
        review["time"] = datetime.utcnow().isoformat()
        #review["review"] = "This is a great car dealer"
        print(review)
        message = post_review(url, review)
        return render(request, 'djangoapp/index.html', context)


