import os
import requests
from flask import request
from flask import Flask
from util import email_notify, init

app = Flask(__name__)


openmrs_host = 'http://refapp:8080/'
idgen_path = 'openmrs/module/idgen/generateIdentifier.form?source=1&username={}&password={}'.format(os.environ['MOBILE_USERNAME'], os.environ['MOBILE_PASSWORD'])
registeration_path ='openmrs/ws/rest/v1/patient'

@app.route('/fetch')
def hello_world():
   response = requests.get(openmrs_host + idgen_path)
   return response.text, response.status_code

@app.route('/register',methods=['POST'])
def register_patient():
   print(request.get_json(force=True))
   response = requests.post(
      openmrs_host + registeration_path,
      auth=(os.environ['MOBILE_USERNAME'], os.environ['MOBILE_PASSWORD']), 
      json=request.get_json(force=True)
   )
   
   if response.status_code == 201:
      email_notify(request.host)

   return response.text, response.status_code


if __name__ == '__main__':
   init()
   app.run(host='0.0.0.0', port=3000)
