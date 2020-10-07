import sys
import os
import time
from time import gmtime, strftime, localtime

import numpy as np

import json
import csv

import zero_touch_provisioning
import zwg3m

#AT+PROV=3,C=KR|O=ICTK|CN=www.ictk.com,20010101000000,20301231235959

#===============================================================================
json_prov = './prov.json'
json_zwg3m = './zwg3m.json'

sta_ssid = None # Station Mode SSID
sta_pw = None # PassPhrase
aws_ep = None # End Point = AWS Host URL
aws_pn = None # Port Number
aws_tn = None # Thing Name
aws_cid = None # Client ID

cert_sn = None
cert_cn = None
cert_not_before = None
cert_not_after = None

#===============================================================================
def zwg3m_provisioning(self):

  global cert_sn
  global cert_cn
  global cert_not_before
  global cert_not_after

  os.chdir(os.path.dirname(os.path.realpath(__file__)))

  if os.path.isfile(json_prov) == False:
    print("Error : Cannot find update.json")
    sys.exit(1)

  #--- JSON --------------------------------------------------------------------
  with open(json_prov, mode='r') as jf_prov:
    jf_prov_data = json.load(jf_prov)
  
  cert_sn = jf_prov_data["SN"]
  cert_cn = jf_prov_data["CN"]
  cert_not_before = jf_prov_data["NOT_BEFORE"]
  cert_not_after = jf_prov_data["NOT_AFTER"]

  #--- Connect to ZWG3M --------------------------------------------------------
  dev = zwg3m.zwg3m()
  pl = dev.getList()
  ztp = zero_touch_provisioning.Application

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

  #print('\n')
  #print("0 : Manual Configuration")
  #print("1 : Auto Configuration")
  #print('\n')
  #type = input("Select Type:   ")

  #dev.provisioning(type,cert_sn,cert_cn,cert_not_before,cert_not_after)
  ztp.ztp_provisioning(self, dev, "1", cert_sn, cert_cn, cert_not_before, cert_not_after)
  return


#===============================================================================
if __name__ == "__main__":
  zwg3m_provisioning()
  #main()
