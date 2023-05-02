import sys
from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

def main(dict):
    authenticator = IAMAuthenticator("81kdYMLFWmGdUTWq-c1u1E7eRCZfNsS6GDbHzxKYsEDk")
    service = CloudantV1(authenticator=authenticator)
    service.set_service_url("https://7e800cf5-b1ca-42c0-a086-0f972ad89906-bluemix.cloudantnosqldb.appdomain.cloud")
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