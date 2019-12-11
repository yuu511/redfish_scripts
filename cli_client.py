#!/usr/bin/python3
import sys
import os
import time

import redfish_frontend

def main(IP): 
  instance = redfish_frontend.start_instance(sys.argv[1])
  redfish_frontend.redfish_power.poweroff(instance)

if __name__ == "__main__":
  if (len(sys.argv) != 2):
    print ("USAGE: " + os.path.basename(__file__) + " [IP] \n")
    exit(1)
  main(sys.argv[1])
