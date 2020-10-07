import sys
import os
import time
from time import gmtime, strftime, localtime

import numpy as np

import json
import csv

import zwg3m

# ===============================================================================
json_main = './main.json'
json_zwg3m = './zwg3m.json'

sta_ssid = None  # Station Mode SSID
sta_pw = None  # PassPhrase
aws_ep = None  # End Point = AWS Host URL
aws_pn = None  # Port Number
aws_tn = None  # Thing Name
aws_cid = None  # Client ID
aws_ac = None  # Auto Connection


# ===============================================================================
def main():
    global sta_ssid
    global sta_pw
    global aws_ep
    global aws_pn
    global aws_tn
    global aws_cid
    global aws_ac

    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    if os.path.isfile(json_main) == False:
        print("Error : Cannot find main.json")
        sys.exit(1)

    # --- JSON -------------------------------------------------------------------- 
    with open(json_main, mode='r') as jf_main:
        jf_main_data = json.load(jf_main)

    json_wifi = './' + jf_main_data["WIFI_SETTING"]
    json_aws = './' + jf_main_data["AWS_SETTING"]

    if not os.path.isfile(json_wifi):
        print("Error : Cannot find WIFI_SETTING in main.json")
        sys.exit(1)
    if not os.path.isfile(json_aws):
        print("Error : Cannot find AWS_SETTING in main.json")
        sys.exit(1)

    # --- WI-FI Setting ---------------------------------------------------------
    with open(json_wifi, mode='r', encoding='utf-8-sig') as jf_wifi:
        jf_wifi_data = json.load(jf_wifi)

    wifi_mode = jf_wifi_data["MODE"]
    wifi = jf_wifi_data[wifi_mode]
    sta_set = wifi["SET"]
    sta_ssid = wifi["SSID"]
    sta_pw = wifi["PW"]
    # print(sta_ssid, sta_pw)

    # --- AWS Setting -----------------------------------------------------------
    with open(json_aws, mode='r') as jf_aws:
        jf_aws_data = json.load(jf_aws)

    aws_ep = jf_aws_data["EndPoint"]
    aws_tn = jf_aws_data["ThingName"]
    aws_pn = jf_aws_data["Port"]
    aws_cid = jf_aws_data["ClientID"]
    aws_ac = jf_aws_data["Autoconn"]
    # print(aws_ep, aws_pn, aws_tn, aws_cid)

    # --- Connect to ZWG3M --------------------------------------------------------
    dev = zwg3m.zwg3m()
    pl = dev.getList()

    if len(pl) < 1:
        print("Error : Cannot find COM port")
        sys.exit(1)

    Port = None
    if os.path.isfile(json_zwg3m):
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

        data = {'Port': '{}'.format(pl[n][0])}
        jdata = json.dumps(data, indent=2)
        with open(json_zwg3m, mode='w') as jf:
            json.dump(jdata, jf, indent=2)
    else:
        dev.open(Port)

    dev.set_wifi(sta_set, sta_ssid, sta_pw)
    dev.set_aws(aws_ep, aws_pn, aws_tn, aws_cid, aws_ac)

    return


# ===============================================================================
if __name__ == "__main__":
    main()
