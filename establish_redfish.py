import requests
import json

import ini_parser
import redfish_commonlib

def create_session(IP,credentials_blob):
  redfish_path='/redfish/v1/SessionService/Sessions'
  full_url = redfish_commonlib.append_to_url(IP,redfish_path)
  payload = json.dumps(credentials_blob)

  status = requests.post(full_url,data=payload,verify=False)
  return status

def initialize_and_create_session(IP,config_settings):
  credentials_blob = ini_parser.load_credentials(config_settings)
  return create_session(IP,credentials_blob)
