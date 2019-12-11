import os
import json
import configparser
from getpass import getpass

def prompt_username_password():
  USERNAME = input("username: ")
  PASSWORD = getpass("password: ")
  credentials_blob = {}
  credentials_blob['UserName'] = USERNAME
  credentials_blob['Password'] = PASSWORD
  return credentials_blob

# todo: actually verify correctness of .ini files
def load_file_settings(config_parser,config_path):
  config_parser.read(config_path)
  return config_parser

def load_default_settings(config_parser,config_path):
  config_parser.set('default','SessionTimeout','60')
  with open(config_path, 'w') as configfile:
    config_parser.write(configfile)
  return config_parser

def get_settings(config_path):
  cparse = configparser.ConfigParser()
  if (os.path.exists(config_path)):
    return load_file_settings(cparse,config_path)
  else:
    return load_default_settings(cparse,config_path)

def load_credentials(config):
  # you may store your credentials in a json file.
  # the script will look under 'credential_path' section of [default]
  if config.has_option('default','credential_path'):
    jsonpath = config.get('default','credential_path')
    if (os.path.isfile(jsonpath)):
      try: 
        rawjson = json.load(open(jsonpath)) 
      except ValueError as e:
        print ("Path provided is not a correctly formatted json file!"
               "Reverting to manual password input")
        return prompt_username_password()

      if 'UserName' not in rawjson or 'Password' not in rawjson:
        print ("UserName or Password not found in json file,"
               "Reverting to manual password input")
        return prompt_username_password()

      credentials_blob = {}
      credentials_blob['UserName'] = rawjson['UserName']
      credentials_blob['Password'] = rawjson['password']
      return credentials_blob
    else:
      print ("credential_path is not a file or does not exist,"
             "Reverting to manual password input")
      return prompt_username_password()
  else:
    print ("No credential_path option found in config file:"
           "Reverting to manual password input")
    return prompt_username_password()
