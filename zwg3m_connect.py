import sys
import os
import time
from time import gmtime, strftime, localtime

import numpy as np

import json
import csv

import zero_touch_provisioning
import zwg3m

json_zwg3m = './zwg3m.json'

#===============================================================================
def zwg3m_connect(self):

  global reset_type
  #--- Connect to ZWG3M --------------------------------------------------------
  dev = zwg3m.zwg3m()
  pl = dev.getList()
  ztp = zero_touch_provisioning.Application
  if len(pl)<1:
    print("Error : Cannot find COM port")
    sys.exit(1)

  os.chdir(os.path.dirname(os.path.realpath(__file__)))

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
  #print('\n')
  #print("0 : Device/Signer CA certificate Erased")
  #print("1 : Device certificate Erased")
  #print("2 : Signer CA certificate Erased")
  #print('\n')
  #type = input("Select Type:   ")
  #dev.reset_cetificate(type)
  ztp.ztp_connect(self, dev)
#===============================================================================
if __name__ == "__main__":
  #main()
  zwg3m_connect()
