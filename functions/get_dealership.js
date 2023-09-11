const {CloudantV1} = require('@ibm-cloud/cloudant');
const {IamAuthenticator} = require('ibm-cloud-sdk-core');

const COUCH_URL = "https://71f0e457-5637-459c-aa20-4bc14b12b27c-bluemix.cloudantnosqldb.appdomain.cloud";
const IAM_API_KEY = "Kz8ISOe7LOYJkYWm5F7OnqJySEaBCcwZeFhfiGXHFxUA";

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