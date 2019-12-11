import os

import ini_parser
import establish_redfish
import redfish_commonlib
import redfish_power

def mkdir_if_empty(basedir,subdir):
  checkdir = os.path.join(basedir,subdir)
  if not os.path.exists(checkdir):
    os.mkdir(checkdir)
  return checkdir

def default_dirs_init(directory):
  mkdir_if_empty(directory,"JSON")
  mkdir_if_empty(directory,"REQUEST_LOGS")

def get_file_dir():
  FILE_PATH = os.path.abspath(__file__)
  DIR_NAME = os.path.dirname(FILE_PATH)
  return DIR_NAME

def start_instance(IP):
  instance = {}

  instance["IP"] = IP

  root = get_file_dir()
  default_dirs_init(root)
  default_config_path = os.path.join(root,'config.ini')
  config_settings = ini_parser.get_settings(default_config_path)
  instance["config_settings"] = config_settings

  session = establish_redfish.initialize_and_create_session(IP,config_settings)
  instance["session"] = session

  return instance

def power_on_system(redfish_instance):
  redfish_power.poweron(redfish_instance)
