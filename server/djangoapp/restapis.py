import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions

def get_request(url, api_key=None, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    if api_key:
        try:
            print("option 1")
            response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
                                                auth=HTTPBasicAuth('apikey', api_key))
        except:
            # If any error occurs
            print("Network exception occurred")

    else:
        try:
            print("option 2")
            response = requests.get(url, headers={'Content-Type': 'application/json'},params=kwargs)                        
        except:
            # If any error occurs
            print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)

cf = {
    "URL":"https://eu-de.functions.appdomain.cloud/api/v1/web/ba16a567-bf8b-4e08-8345-2742a032caf3",
    "API_KEY":"z5e8crJchrTM27tZiF0NuoJUUw8mLV9n02etE4DCk4jN",
}

def analyze_review_sentiments(review):
    url = "https://api.eu-de.natural-language-understanding.watson.cloud.ibm.com/instances/ff802d08-d639-4102-9662-a2f9066cdf9d"
    api_key = "0Vn7Cko4h6f8hUhyo84bDN2Tigi1GFTdvOj1CZHZGilf"


    authenticator = IAMAuthenticator(api_key)
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2022-04-07',
        authenticator=authenticator)

    natural_language_understanding.set_service_url(url)
    try: 
        response = natural_language_understanding.analyze(
            text=review,
            features=Features(
                entities=EntitiesOptions(emotion=True, sentiment=True, limit=2),
                keywords=KeywordsOptions(emotion=True, sentiment=True,
                                        limit=2))).get_result()
        
        #response = json.dumps(response, indent=2)
        print(response["keywords"][0]["sentiment"]["label"])
        #response = json.load(response)
        result = response["keywords"][0]["sentiment"]["label"]
        
    except:
        result = "No sentiment could be discovered"
    #json_data = json.loads(response.results)
    #print(json_data)
    return result

# Create a get_dealers_from_cf method to get dealers from a cloud function
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        #dealers = json_result["body"]
        # For each dealer object
        for dealer_doc in json_result:
            # Get its content in `doc` object
            #dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"], state=dealer_doc["state"])
            results.append(dealer_obj)

    return results
"""
def get_dealers_from_cf(params={},**kwargs):
    response = requests.get(cf["URL"]+"/dealership-package/get-dealership", params=params, headers={'Content-Type': 'application/json'},
                                 auth=HTTPBasicAuth('apikey', cf["API_KEY"]))
    return {"result": response.json()}
# - Parse JSON results into a CarDealer object list
"""

# Create a  method to get reviews by dealer id from a cloud function
def get_dealer_reviews_from_cf(url, dealerId):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, dealership=dealerId)
    print(json_result)
    if json_result:
        # Get the row list in JSON as dealers
        #dealers = json_result["body"]
        # For each dealer object
        for review_doc in json_result:
            # Get its content in `doc` object
            #dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            review_obj = DealerReview(car_make = review_doc["car_make"], car_model = review_doc["car_model"], car_year = review_doc["car_year"],
                dealership= review_doc["dealership"], id =review_doc["id"], name = review_doc["name"], purchase = review_doc["purchase"],
                purchase_date = review_doc["purchase_date"], review = review_doc["review"], sentiment="")
            review_obj.sentiment = analyze_review_sentiments(review_obj.review)
            results.append(review_obj)

    return results
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list

def get_dealer_by_id_from_cf(url, dealerId):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, id=dealerId)
    if json_result:
        # Get the row list in JSON as dealers
        #dealers = json_result["body"]
        # For each dealer object
        for dealer_doc in json_result:
            # Get its content in `doc` object
            #dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"], state=dealer_doc["state"])
            results.append(dealer_obj)

    return results
    

def post_review(payload, kwargs):
    response = requests.post(cf["URL"]+"/djangoapp/get-reviews", params=kwargs, json={'review': payload})
    return {"result": response.json()}


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative



