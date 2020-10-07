import sys
import os
import time
from time import gmtime, strftime, localtime

import numpy as np

import json
import csv

import zwg3m

#===============================================================================
json_update = './update.json'
json_zwg3m = './zwg3m.json'

sta_ssid = None # Station Mode SSID
sta_pw = None # PassPhrase
aws_ep = None # End Point = AWS Host URL
aws_pn = None # Port Number
aws_tn = None # Thing Name
aws_cid = None # Client ID

mqtt_act = None
mqtt_key = None
mqtt_type = None
mqtt_val = None

#===============================================================================
def main():

  global mqtt_act
  global mqtt_key
  global mqtt_type
  global mqtt_val

  os.chdir(os.path.dirname(os.path.realpath(__file__)))

  if os.path.isfile(json_update) == False:
    print("Error : Cannot find update.json")
    sys.exit(1)

  #--- JSON --------------------------------------------------------------------
  with open(json_update, mode='r') as jf_update:
    jf_update_data = json.load(jf_update)
  
  mqtt_key = jf_update_data["KEY"]
  mqtt_type = jf_update_data["TYPE"]

  #--- Connect to ZWG3M --------------------------------------------------------
  dev = zwg3m.zwg3m()
  pl = dev.getList()
  
  if len(pl)<1:
    print("Error : Cannot find COM port")
    sys.exit(1)


  Port = None
  if os.path.isfile(json_zwg3m) == True:
    with open(json_zwg3m, mode='r') as jf:
      Port = json.loads(json.load(jf))['Port']

      if Port in [x[0] for x in pl]:
        pass
      else:
        Port = None

  if Port == None:
    for n in range(len(pl)):
      print('{}: {}'.format(n, pl[n]))
    print('\n')
    n = int(input('Select Port:  '))
    dev.open(pl[n][0])

    data = {'Port':'{}'.format(pl[n][0])}
    jdata = json.dumps(data, indent=2)
    with open(json_zwg3m, mode='w') as jf:
      json.dump(jdata, jf, indent=2)
  else:
    dev.open(Port)


  dev.delta(mqtt_key,mqtt_type)
  dev.wait_sub()

  return


#===============================================================================
if __name__ == "__main__":
  main()
