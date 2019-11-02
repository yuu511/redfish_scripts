#!/usr/bin/python3

import os
import sys
import urllib.parse
import requests
import json
import configparser
from getpass import getpass

# todo: actually verify correctness of .ini files
def verify_ini_opts(config_parser,config_path):
  config_parser.read(config_path)
  return config_parser

def load_config_defaults(config_parser,config_path):
  config_parser.set('default','SessionTimeout','60')
  # config_parser['default'] = { 'SessionTimeout' : '60' } 
  with open(config_path, 'w') as configfile:
    config_parser.write(configfile)
  return config_parser

def look_for_config_file(directory):
  config_path = os.path.join(directory,'config.ini')
  cparse = configparser.ConfigParser()
  if (os.path.exists(config_path)):
    return verify_ini_opts(cparse,config_path)
  else:
    return load_config_defaults(cparse,config_path)

def prompt_username_password():
  USERNAME = input("username: ")
  PASSWORD = getpass("password: ")
  credentials_blob['UserName'] = USERNAME
  credentials_blob['PassWord'] = PASSWORD
  return credentials_blob

def load_credentials_if_exist(opts):
  # you may store your credentials in a json file.
  # the script will look under 'credential_path' section of [default]
  if opts.has_option('default','credential_path'):
    jsonpath = opts.get('default','credential_path')
    if not (os.path.exists(jsonpath)):
      print ("Check path in config.ini. Reverting to manual password input:")
      return prompt_username_password()
    else: 
      rawjson = json.load(open(jsonpath)) 
      if 'UserName' not in rawjson or 'Password' not in rawjson:
        print ("UserName or Password not found in json file, Reverting to manual password input")
        return prompt_username_password()
      credentials_blob = {}
      credentials_blob['UserName'] = rawjson['UserName']
      credentials_blob['Password'] = rawjson['Password']
      return credentials_blob
  else:
    return prompt_username_password()

def mkdir_if_empty(basedir,subdir):
  checkdir = os.path.join(basedir,subdir)
  if not os.path.exists(checkdir):
    os.mkdir(checkdir)
  return checkdir

def default_dirs_init(directory):
  mkdir_if_empty(directory,"JSON")
  mkdir_if_empty(directory,"CURL_LOGS")

def get_file_dir():
  FILE_PATH = os.path.abspath(__file__)
  DIR_NAME = os.path.dirname(FILE_PATH)
  return DIR_NAME

def create_session(IP,credentials_blob):
  payload = json.dumps(credentials_blob)
  redfish_path='/redfish/v1/SessionService/Sessions'
  full_url = 'https://' + IP + redfish_path
  uname = credentials_blob['UserName']
  pw = credentials_blob['Password']
  status = requests.post(full_url,auth=(uname,pw),verify=False)
  print (status.content)
  return status

def initialize_and_create_session(IP):
  root = get_file_dir()
  default_dirs_init(root)
  cfgfile = look_for_config_file(root)
  credentials_blob = load_credentials_if_exist(cfgfile)
  create_session(IP,credentials_blob)

def main(argv):
  if (len(sys.argv) != 2):
    print ("USAGE: " + os.path.basename(__file__) + " [IP] \n")
    exit(1)

  IP = sys.argv[1]
  initialize_and_create_session(IP)
  
if __name__ == "__main__":
  main(sys.argv[1:])
