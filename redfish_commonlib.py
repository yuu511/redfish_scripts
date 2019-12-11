import datetime
import time 

import establish_redfish

def append_to_url(IP,redfish_path):
  return 'https://' + IP + redfish_path

def extract_xauth_token(redfish_instance):
  return redfish_instance["session"].headers["X-Auth-Token"]

def expired(redfish_instance):
  raw_tstring = redfish_instance["session"].headers["Date"]
  request_completed = datetime.datetime.strptime(raw_tstring,'%a, %d %b %Y %H:%M:%S GMT')
  elapsed = datetime.datetime.now() - request_completed
  elapsed = elapsed.total_seconds()
  if ("SessionTimeout" in redfish_instance["config_settings"]["default"]):
   return elapsed > float(redfish_instance["config_settings"]["default"]["SessionTimeout"])  
  else:
   return elapsed > 60

def renew_if_expired(redfish_instance):
  if (expired(redfish_instance)):
    redfish_instance["session"] = establish_redfish.initialize_and_create_session\
    (redfish_instance["IP"],redfish_instance["config_settings"])
