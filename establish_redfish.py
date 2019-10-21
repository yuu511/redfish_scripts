#!/usr/bin/python3

import os
import sys
import requests
import pickle
import json
import configparser
from getpass import getpass

def mkdir_if_empty(basedir,subdir):
  checkdir = os.path.join(basedir,subdir)
  if not os.path.exists(checkdir):
    os.mkdir(checkdir)
  return checkdir

def get_file_dir():
  FILE_PATH = os.path.abspath(__file__)
  DIR_NAME = os.path.dirname(FILE_PATH)
  return DIR_NAME

def print_usage():
  print ("USAGE: " + os.path.basename(__file__) + " [IP] \n")

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

def load_ini_opts(config_path):
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
      credentials_blob['PassWord'] = rawjson['Password']
      return credentials_blob
  else:
    return prompt_username_password()


def main(argv):
  if (len(sys.argv) != 2):
    print_usage()
    exit(1)

  IP = sys.argv[1]
  CWD = get_file_dir()

  config_path = os.path.join(CWD,'config.ini')
  OPTIONS = load_ini_opts(config_path)

  JSON_DIR = mkdir_if_empty(CWD,"JSON")
  CURL_LOGS = mkdir_if_empty(CWD,"CURL_LOGS")
  
  credentials = load_credentials_if_exist(OPTIONS)

  
if __name__ == "__main__":
  main(sys.argv[1:])
