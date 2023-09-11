import sys
from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

def main(dict):
    authenticator = IAMAuthenticator("Kz8ISOe7LOYJkYWm5F7OnqJySEaBCcwZeFhfiGXHFxUA")
    service = CloudantV1(authenticator=authenticator)
    service.set_service_url("https://71f0e457-5637-459c-aa20-4bc14b12b27c-bluemix.cloudantnosqldb.appdomain.cloud")
    response = service.post_document(db='reviews', document={'review': dict['review']}).get_result()
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