import sys
from ibm_cloud_sdk_core import ApiException
from ibmcloudant.cloudant_v1 import CloudantV1, Document
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

def main(dict):
    authenticator = IAMAuthenticator("Kz8ISOe7LOYJkYWm5F7OnqJySEaBCcwZeFhfiGXHFxUA")
    service = CloudantV1(authenticator=authenticator)
    service.set_service_url("https://71f0e457-5637-459c-aa20-4bc14b12b27c-bluemix.cloudantnosqldb.appdomain.cloud")

    dealer_id = dict.get("dealerId", "")
    if dealer_id == "":
        response = service.post_all_docs(
            db='reviews',
            include_docs = True
            # limit = 10
        ).get_result()
    else:
        response = service.post_find(
            db='reviews',
            selector={'dealership': {'$eq': int(dict["dealerId"])}},
        ).get_result()

    try:
        result= {
        'headers': {'Content-Type':'application/json'},
        'body': {'data':response}
        }
        return result
    except:
        return {
        'statusCode': 404,
        'message': 'Something went wrong'
        }