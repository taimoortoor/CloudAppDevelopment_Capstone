const {CloudantV1} = require('@ibm-cloud/cloudant');
const {IamAuthenticator} = require('ibm-cloud-sdk-core');

const COUCH_URL = "https://7e800cf5-b1ca-42c0-a086-0f972ad89906-bluemix.cloudantnosqldb.appdomain.cloud";
const IAM_API_KEY = "81kdYMLFWmGdUTWq-c1u1E7eRCZfNsS6GDbHzxKYsEDk";

function main(params) {
    // console.log(params);
    return new Promise(function (resolve, reject) {
        const authenticator = new IamAuthenticator({ apikey: IAM_API_KEY })
        const cloudant = CloudantV1.newInstance({
            authenticator: authenticator
        });
        cloudant.setServiceUrl(COUCH_URL);
        if (params.state) {
            // return dealership with this state 
            cloudant.postFind({db:'dealerships',selector:{st:params.state}})
            .then((result)=>{
              let code = 200;
              if (result.result.docs.length == 0) {
                  code = 404;
              }
              resolve({
                  statusCode: code,
                  headers: { 'Content-Type': 'application/json' },
                  body: result.result.docs
              });
            }).catch((err)=>{
              reject(err);
            })
        } else if (params.dealerId) {
            id = parseInt(params.dealerId)
            // return dealership with this id 
            cloudant.postFind({
              db: 'dealerships',
              selector: {
                id: parseInt(params.dealerId)
              }
            })
            .then((result)=>{
              // console.log(result.result.docs);
              let code = 200;
              if (result.result.docs.length == 0) {
                  code = 404;
              }
              resolve({
                  statusCode: code,
                  headers: { 'Content-Type': 'application/json' },
                  body: result.result.docs
              });
            }).catch((err)=>{
              reject(err);
            })
        } else {
            // return all documents 
            cloudant.postAllDocs({ db: 'dealerships', includeDocs: true })            
            .then((result)=>{
              // console.log(result.result.rows);
              let code = 200;
              if (result.result.rows.length == 0) {
                  code = 404;
              }
              resolve({
                  statusCode: code,
                  headers: { 'Content-Type': 'application/json' },
                  body: result.result.rows
              });
            }).catch((err)=>{
              reject(err);
            })
      }
    }
    )}