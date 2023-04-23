import requests
import json
# import related models here
from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)

cf = {
    "URL":"https://eu-de.functions.appdomain.cloud/api/v1/web/ba16a567-bf8b-4e08-8345-2742a032caf3/dealership-package/get-dealership",
    "API_KEY":"z5e8crJchrTM27tZiF0NuoJUUw8mLV9n02etE4DCk4jN",
}

# Create a get_dealers_from_cf method to get dealers from a cloud function
def get_dealers_from_cf(**kwargs):
    response = requests.get(cf["URL"], headers={'Content-Type': 'application/json'},
                                 auth=HTTPBasicAuth('apikey', cf["API_KEY"]))
    return {"result": response.json()}
# - Parse JSON results into a CarDealer object list


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative



