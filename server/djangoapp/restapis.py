import requests
import json
from .models import CarDealer
from requests.auth import HTTPBasicAuth

def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('apikey', api_key))
        status_code = response.status_code
        print("With status {} ".format(status_code))
        json_data = json.loads(response.text)
        return json_data
    except:
        # If any error occurs
        print("Network exception occurred")
    

def post_request(url, json_payload, **kwargs):
    '''
     Create a `post_request` to make HTTP POST requests
    '''
    print(kwargs)
    print("POST to {} ".format(url))
    print(json_payload)
    try:
        response = requests.post(url, json=json_payload, params=kwargs)
    except:
        print("Something went wrong")
        return response.status_code
    return response


def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)

    if json_result and "body" in json_result:

        # Get the list of dealerships from the response

        dealerships = json_result["body"]

        for dealer in dealerships:

            if "doc" in dealer and "address" in dealer["doc"]:
                dealer_doc = dealer
                # Create a CarDealer object with values from the dealer document

                dealer_obj = CarDealer(
                    address=dealer_doc.get("address"),
                    city=dealer_doc.get("city"),
                    id=dealer_doc.get("id"),
                    lat=dealer_doc.get("lat"),
                    long=dealer_doc.get("long"),
                    st=dealer_doc.get("st"),
                    zip=dealer_doc.get("zip")

                )
                results.append(dealer_obj)
    return results

def get_dealer_reviews_from_cf(url, dealer_id):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, dealerId=dealer_id)
    if json_result:
        # Get the row list in JSON as dealers
        reviews = json_result["data"]
        review_docs = reviews["docs"]
        for review_doc in review_docs: 
            review_obj = DealerReview(
                dealership=review_doc["dealership"],
                name=review_doc["name"],
                purchase=review_doc["purchase"],
                review=review_doc["review"])
            if "id" in review_doc:
                review_obj.id = review_doc["id"]
            if "purchase_date" in review_doc:
                review_obj.purchase_date = review_doc["purchase_date"]
            if "car_make" in review_doc:
                review_obj.car_make = review_doc["car_make"]
            if "car_model" in review_doc:
                review_obj.car_model = review_doc["car_model"]
            if "car_year" in review_doc:
                review_obj.car_year = review_doc["car_year"]

            review_obj.sentiment = analyze_review_sentiments(review_obj.review)
            results.append(review_obj)

    return results

def analyze_review_sentiments(text):
    api_key = ""
    url = ""
    texttoanalyze= text
    version = '2020-08-01'
    authenticator = IAMAuthenticator(api_key)
    nlu = NaturalLanguageUnderstandingV1(version='2020-08-01',authenticator=authenticator)
    nlu.set_service_url(url)
    response = nlu.analyze(text=text,
                    features= Features(sentiment= SentimentOptions())).get_result()
    print(json.dumps(response))
    sentiment_score = str(response["sentiment"]["document"]["score"])
    sentiment_label = response["sentiment"]["document"]["label"]
    print(sentiment_score)
    print(sentiment_label)
    sentimentresult = sentiment_label
    
    return 
