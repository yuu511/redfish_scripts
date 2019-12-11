import json
import requests

import redfish_commonlib

def power_switch(redfish_instance,payload):
  redfish_path = '/redfish/v1/Systems/1/Actions/ComputerSystem.Reset' 
  full_url = redfish_commonlib.append_to_url(redfish_instance["IP"],redfish_path)
  redfish_commonlib.renew_if_expired(redfish_instance)
  token = redfish_commonlib.extract_xauth_token(redfish_instance)
  head = {'X-Auth-Token':token}
  test = requests.post(full_url,headers=head, data=payload,verify=False)
  print (test)

def poweron(redfish_instance):
  payload = {
    "ResetType":"On"
  }
  return power_switch(redfish_instance,json.dumps(payload))

def poweroff(redfish_instance):
  payload = {
    "ResetType":"GracefulShutdown"
  }
  return power_switch(redfish_instance,json.dumps(payload))
