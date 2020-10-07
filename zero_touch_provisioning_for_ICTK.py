import base64
import binascii
import json
import os
import threading
import time
import tkinter
from queue import Queue
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
import tkinter as tk
import tkinter.ttk as ttk
import serial

import zwg3m
import zwg3m_configuration
import zwg3m_certi
from tkinter import simpledialog

#===============================================================================
import zwg3m_provisioning
import zwg3m_publish
import zwg3m_reset_certificate
import zwg3m_subscribe


#===============================================================================
json_zwg3m = './zwg3m.json'
def func(event):             # func 함수 작성
    print('enter pressed!')   # 임시로 문자열만 출력.

def connect_zwg3m(self):
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
            self.txtComment.insert(END, "{}: {}\n".format(n, pl[n]))
            self.txtComment.update()
            self.txtComment.see(END)
            #print('{}: {}'.format(n, pl[n]))
        #print('\n')
        self.txtComment.insert(END, "\n")
        self.txtComment.update()
        self.txtComment.see(END)
        self.op1 = StringVar()
        result = IntVar()
        result.set(0)
        self.txtComment.insert(END, "Select Port : ")
        self.txtComment.update()
        self.txtComment.see(END)

        self.input = Entry(self.frame3, textvariable=self.op1)
        self.input.bind('<Return>', func)
        self.input.pack(side=LEFT)

        #n = int(input('Select Port:  '))
        #n = int(op1.get())
        #dev.open(pl[n][0])

        #data = {'Port': '{}'.format(pl[n][0])}
        #jdata = json.dumps(data, indent=2)
        #with open(json_zwg3m, mode='w') as jf:
         #   json.dump(jdata, jf, indent=2)
    else:
        dev.open(Port)

    return dev

def ztp_log_print(self, txt):
    self.txtComment.insert(END, txt)


def g3_cmd(self, dev, packet, comment):
    Application.ztp_g3_cmd(self, dev, packet, comment)

def prov(self, dev):
    while True:
        data = dev.sp.readline()
        time.sleep(0.01)
        if ("EVENT:DEVICE CERTIFICATE REGISTERED\n".encode() == data):
            break

    self.txtComment.insert(END, "\n OK")
    self.txtComment.update()
    self.txtComment.see(END)

    self.txtComment.insert(END, "\n AWS Connection")
    self.txtComment.update()
    self.txtComment.see(END)

    # --- Connection -------------------------------------------------------------
    data = "AT+AWS_CONN=".encode() + '1'.encode() + '\n'.encode()
    dev.sp.write(data)
    time.sleep(0.01)

    data = dev.sp.readline()
    #print('Text %s' % data)
    if ("SUCCEED\n".encode() == data):
        self.txtComment.insert(END, "\n OK")
        self.txtComment.update()
        self.txtComment.see(END)
    else:
        self.txtComment.insert(END, "\n Fail")
        self.txtComment.update()
        self.txtComment.see(END)

    self.txtComment.insert(END, "\n ++++++++ Provisioning END+++++++++\n")
    self.txtComment.update()
    self.txtComment.see(END)

class MyFrame(Frame):
    # noinspection PyUnresolvedReferences

    def __init__(self, master):
        Frame.__init__(self, master)
        log_data = "테스트"
        self.entry_value = StringVar(self.master, value='')
        self.master = master
        self.master.title("Zero Touch Provisioning")
        self.F = Frame(master)
        self.F1 = Frame(master)
        self.F.pack(fill=BOTH, expand=True)
        self.F1.pack(fill=BOTH, expand=True)
        self.pack(fill=BOTH, expand=True)

        # Item
        lblComment = Label(self.F, text="Function", width=10)
        lblComment.pack(side=LEFT, padx=10, pady=10)

        # Configuration
        btnOK = Button(self.F, text="Configuration", command=self.button_configuration)
        btnOK.pack(side=LEFT, padx=10, pady=10)

        # Cert
        btnOK = Button(self.F, text="Cert", command=self.button_cert)
        btnOK.pack(side=LEFT, padx=30, pady=10)

        btnOK = Button(self.F, text="Provisioning", command=self.button_prov)
        btnOK.pack(side=LEFT, padx=30, pady=10)

        # Item
        lblComment = Label(self.F1, text="", width=10)
        lblComment.pack(side=LEFT, padx=10, pady=10)

        # Subscribe
        btnOK = Button(self.F1, text="Subscribe", command=self.button_sub)
        btnOK.pack(side=LEFT, padx=10, pady=10)

        # Publish
        btnOK = Button(self.F1, text="Publish", command=self.button_pub)
        btnOK.pack(side=LEFT, padx=30, pady=10)

        # Reset
        btnOK = Button(self.F1, text="Erase", command=self.button_reset)
        btnOK.pack(side=LEFT, padx=30, pady=10)

        # log
        self.frame3 = Frame(self)
        self.frame3.pack(fill=BOTH, expand=True)
        lblComment = Label(self.frame3, text="Result", width=10)
        lblComment.pack(side=LEFT, anchor=N, padx=10, pady=10)

        self.txtComment = Text(self.frame3)
        self.txtComment.pack(fill=X, pady=10, padx=10)

        self.txtComment.insert(END, "Test Result\n")
        self.txtComment.update()
        #connect_zwg3m(self)

    def button_configuration(self):
        self.txtComment.delete(1.0, END)
        self.txtComment.update()
        self.txtComment.insert(END, "\n +++++++++ Configuration START+++++++++\n")
        self.txtComment.update()
        self.txtComment.see(END)
        zwg3m_configuration.zwg3m_configuration(self)
        self.txtComment.insert(END, "\n ++++++++ Configuration END+++++++++\n")
        self.txtComment.update()
        self.txtComment.see(END)

    def button_cert(self):
        self.txtComment.delete(1.0, END)
        self.txtComment.insert(END, "\n +++++++++ Cert Writing START+++++++++\n")
        self.txtComment.update()
        self.txtComment.see(END)
        zwg3m_certi.zwg3m_certi(self)
        self.txtComment.insert(END, "\n ++++++++ Cert Writing END+++++++++\n")
        self.txtComment.update()
        self.txtComment.see(END)

    def button_prov(self):
        self.txtComment.delete(1.0, END)
        self.txtComment.insert(END, "\n +++++++++ Provisioning START+++++++++\n")
        self.txtComment.update()
        self.txtComment.see(END)
        zwg3m_provisioning.zwg3m_provisioning(self)
        #self.txtComment.insert(END, "\n ++++++++ Provisioning END+++++++++\n")
        #self.txtComment.update()
        #self.txtComment.see(END)

    def button_sub(self):
        self.txtComment.delete(1.0, END)
        self.txtComment.insert(END, "\n +++++++++ Subscribe START+++++++++\n")
        self.txtComment.update()
        self.txtComment.see(END)
        zwg3m_subscribe.zwg3m_subscribe(self)
        self.txtComment.insert(END, "\n ++++++++ Subscribe END+++++++++\n")
        self.txtComment.update()
        self.txtComment.see(END)

    def button_pub(self):
        self.txtComment.delete(1.0, END)
        self.txtComment.insert(END, "\n +++++++++ Publish START+++++++++\n")
        self.txtComment.update()
        self.txtComment.see(END)
        zwg3m_publish.zwg3m_publish(self)
        self.txtComment.insert(END, "\n ++++++++ Publish END+++++++++\n")
        self.txtComment.update()
        self.txtComment.see(END)

    def button_reset(self):
        self.txtComment.delete(1.0, END)
        self.txtComment.insert(END, "\n +++++++++ Reset START+++++++++\n")
        self.txtComment.update()
        self.txtComment.see(END)
        zwg3m_reset_certificate.zwg3m_reset_certificate(self)
        self.txtComment.insert(END, "\n ++++++++ Reset END+++++++++\n")
        self.txtComment.update()
        self.txtComment.see(END)

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Hello World\n(click me)"
        self.hi_there["command"] = self.say_hi
        self.hi_there.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")

    def say_hi(self):
        print("hi there, everyone!")

    def set_text(self, text):
        self.entry_value.set(text)

    def ztp_set_wifi(self, dev, set, ssid, pw):
        self.txtComment.insert(END, "\n wifi : " + ssid + " " + pw)
        self.txtComment.update()
        # --- Wi-Fi - SSID ----------------------------------------------------------
        if set == "U":
            ussid = (ssid).encode("UTF-8")
            print(ussid)
            essid = binascii.hexlify(ussid)
            print(essid)
            data = "AT+WIFI_SSID_STA_U=".encode() + essid + '\n'.encode()
            print(data)
        else:
            data = "AT+WIFI_SSID_STA=".encode() + ssid.encode() + '\n'.encode()

        dev.sp.write(data)
        #time.sleep(0.01)

        data = dev.sp.readline()
        if "SUCCEED\n".encode() == data:
            self.txtComment.insert(END, "\n STA SSID : OK")
            self.txtComment.update()
        else:
            self.txtComment.insert(END, "\n STA SSID : Fail")
            self.txtComment.update()
        data = dev.sp.readline()

        # --- Wi-Fi - PassPhrase ----------------------------------------------------
        data = "AT+WIFI_PW_STA=".encode() + pw.encode() + '\n'.encode()
        dev.sp.write(data)
        #time.sleep(0.01)

        data = dev.sp.readline()
        if "SUCCEED\n".encode() == data:
            self.txtComment.insert(END, "\n STA PASSWORD : OK")
            self.txtComment.update()
        else:
            self.txtComment.insert(END, "\n STA PASSWORD : Fail")
            self.txtComment.update()
        data = dev.sp.readline()

    # -----------------------------------------------------------------------------
    def ztp_set_aws(self, dev, ep, pn, tn, cid, ac):
        self.txtComment.insert(END, "\n AWS Setting Value")
        self.txtComment.update()
        self.txtComment.see(END)
        self.txtComment.insert(END, "\n End Point :" + ep)
        self.txtComment.update()
        self.txtComment.see(END)
        self.txtComment.insert(END, "\n Port Number:" + str(pn))
        self.txtComment.update()
        self.txtComment.see(END)
        self.txtComment.insert(END, "\n Thing Name:" + tn)
        self.txtComment.update()
        self.txtComment.see(END)
        self.txtComment.insert(END, "\n Caller ID:"+ cid)
        self.txtComment.update()
        self.txtComment.see(END)
        # --- End Point -------------------------------------------------------------
        data = "AT+AWS_EP=".encode() + ep.encode() + '\n'.encode()
        dev.sp.write(data)
        time.sleep(0.01)

        data = dev.sp.readline()
        if "SUCCEED\n".encode() == data:
            self.txtComment.insert(END, "\n End Point : OK")
            self.txtComment.update()
            self.txtComment.see(END)
        else:
            self.txtComment.insert(END, "\n End Point : Fail")
            self.txtComment.update()
            self.txtComment.see(END)
        data = dev.sp.readline()

        # --- Port Number -----------------------------------------------------------
        data = "AT+AWS_PN=".encode() + str(pn).encode() + '\n'.encode()
        dev.sp.write(data)
        time.sleep(0.01)

        data = dev.sp.readline()
        if ("SUCCEED\n".encode() == data):
            self.txtComment.insert(END, "\n Port Number : OK")
            self.txtComment.update()
            self.txtComment.see(END)
        else:
            self.txtComment.insert(END, "\n Port Number : Fail")
            self.txtComment.update()
            self.txtComment.see(END)
        data = dev.sp.readline()

        # --- Thing Name ------------------------------------------------------------
        data = "AT+AWS_TN=".encode() + tn.encode() + '\n'.encode()
        dev.sp.write(data)
        time.sleep(0.01)

        data = dev.sp.readline()
        if ("SUCCEED\n".encode() == data):
            self.txtComment.insert(END, "\n Thing Name : OK")
            self.txtComment.update()
            self.txtComment.see(END)
        else:
            self.txtComment.insert(END, "\n Thing Name : Fail")
            self.txtComment.update()
            self.txtComment.see(END)
        data = dev.sp.readline()

        # --- Client ID -------------------------------------------------------------
        data = "AT+AWS_CID=".encode() + cid.encode() + '\n'.encode()
        dev.sp.write(data)
        time.sleep(0.01)

        data = dev.sp.readline()
        if ("SUCCEED\n".encode() == data):
            self.txtComment.insert(END, "\n Caller ID : OK")
            self.txtComment.update()
            self.txtComment.see(END)
        else:
            self.txtComment.insert(END, "\n Caller ID : Fail")
            self.txtComment.update()
            self.txtComment.see(END)
        data = dev.sp.readline()

        # --- Auto Connection -------------------------------------------------------------
        # data = "AT+AWS_AC=".encode() + ac.encode() + '\n'.encode()
        # self.sp.write(data)
        # time.sleep(0.01)

        # data = self.sp.readline()
        # if("SUCCEED\n".encode() == data):
        # print("OK")
        # else:
        # print("Fail")
        # data = self.sp.readline()

        # -----------------------------------------------------------------------------
        # -----------------------------------------------------------------------------
    def ztp_g3_cmd(self, dev, pkt, dp):

        data = 'AT+G3={}\n'.format(pkt).encode()
        # print(data)

        dev.sp.write(data)
        time.sleep(0.2)

        # data = self.sp.readline()

        data = dev.sp.read(1)
        n = dev.sp.inWaiting()
        data = data + dev.sp.readline()

        #print(dp)
        self.txtComment.insert(END, dp)
        self.txtComment.update()
        self.txtComment.see(END)
        if ("\n3630\n".encode() == data):
            self.txtComment.insert(END, "\nError : wrong password")
            sys.exit(1)

        time.sleep(1.0)

    # -----------------------------------------------------------------------------
    def ztp_printf(self, txt):
        self.txtComment.insert(END, txt)
        self.txtComment.update()
        self.txtComment.see(END)
    # -----------------------------------------------------------------------------
    def ztp_provisioning(self, dev, type, sn, cn, not_before, not_after):

        # --- provisioning -----------------------------------------------------------
        # print('Text %s'type.encode())
        #if (type == '1'):
        data = "AT+PROV=".encode() + type.encode() + '\n'.encode()
        self.txtComment.insert(END, "\n ZTP With Auto Configuration")
        self.txtComment.update()
        self.txtComment.see(END)
        #else:
        #    data = "AT+PROV=".encode() + type.encode() + ','.encode() + sn.encode() + ','.encode() + cn.encode() + ','.encode() + not_before.encode() + ','.encode() + not_after.encode() + '\n'.encode()
        #    print("manual")

        dev.sp.write(data)
        time.sleep(0.01)

        data = dev.sp.readline()
        self.txtComment.insert(END, "\n Key Generation")
        self.txtComment.update()
        self.txtComment.see(END)
        if ("KEY GENERATION SUCCESS\n".encode() == data):
            self.txtComment.insert(END, "\n OK\n ")
            self.txtComment.update()
            self.txtComment.see(END)
        elif ("ALREADY CLIENT CERTIFICATE REGISTERED\n".encode() == data):
            self.txtComment.insert(END, "\n Already Client Certificate Registered\n ")
            self.txtComment.update()
            self.txtComment.see(END)
        else:
            self.txtComment.insert(END, "\n Fail\n ")
            self.txtComment.update()
            self.txtComment.see(END)

        data = dev.sp.readline()
        time.sleep(0.01)

        data = dev.sp.readline()
        self.txtComment.insert(END, "\n Device Certificate Generate")
        self.txtComment.update()
        self.txtComment.see(END)

        if ("CETIFICATE GENERATION\n".encode() == data):
            self.txtComment.insert(END, "\n OK\n ")
            self.txtComment.update()
            self.txtComment.see(END)
        else:
            self.txtComment.insert(END, "\n Fail\n ")
            self.txtComment.update()
            self.txtComment.see(END)

        data = dev.sp.readline()
        time.sleep(0.01)

        data = dev.sp.readline()
        self.txtComment.insert(END, "\n Device Certificate Save")
        self.txtComment.update()
        self.txtComment.see(END)
        if ("DEVICE CERTIFICATE SAVE\n".encode() == data):
            self.txtComment.insert(END, "\n OK\n ")
            self.txtComment.update()
            self.txtComment.see(END)
        else:
            self.txtComment.insert(END, "\n Fail\n ")
            self.txtComment.update()
            self.txtComment.see(END)

        data = dev.sp.readline()
        time.sleep(0.05)

        data = dev.sp.readline()
        time.sleep(0.05)

        self.txtComment.insert(END, "\n Device Certificate Register")
        self.txtComment.update()
        self.txtComment.see(END)

        t = threading.Thread(target=prov, args=(self, dev,))
        t.start()
        t.join(2)
        #while True:
        #    data = dev.sp.readline()
        #    time.sleep(0.01)
        #    # print('Text %s'%data)
        #    if ("EVENT:DEVICE CERTIFICATE REGISTERED\n".encode() == data):
        #        break

        #self.txtComment.insert(END, "\n OK")
        #self.txtComment.update()
        #self.txtComment.see(END)

        #self.txtComment.insert(END, "\n AWS Connection")
        #self.txtComment.update()
        #self.txtComment.see(END)

        # --- Connection -------------------------------------------------------------

        #data = "AT+AWS_CONN=".encode() + '1'.encode() + '\n'.encode()
        #dev.sp.write(data)
        #time.sleep(0.01)

        #data = dev.sp.readline()
        #print('Text %s' % data)
        #if ("SUCCEED\n".encode() == data):
        #    self.txtComment.insert(END, "\n OK")
        #    self.txtComment.update()
        #    self.txtComment.see(END)
        #else:
        #    self.txtComment.insert(END, "\n Fail")
        #    self.txtComment.update()
        #    self.txtComment.see(END)
    # -----------------------------------------------------------------------------
    def ztp_subscribe(self, dev, topic, qos):

        # --- AWS Subscribe -----------------------------------------------------------
        data = "AT+AWS_SUB=".encode() + topic.encode() + ','.encode() + str(qos).encode() + '\n'.encode()
        dev.sp.write(data)
        time.sleep(0.01)

        data = dev.sp.readline()
        if ("SUCCEED\n".encode() == data):
            self.txtComment.insert(END, "\n OK")
            self.txtComment.update()
            self.txtComment.see(END)
        else:
            self.txtComment.insert(END, "\n Fail")
            self.txtComment.update()
            self.txtComment.see(END)

        time.sleep(0.01)

        data = dev.sp.readline()
        time.sleep(0.01)

        data = dev.sp.readline()
        if ("EVENT:SUB OK\n".encode() == data):
            self.txtComment.insert(END, "\n OK")
            self.txtComment.update()
            self.txtComment.see(END)
        else:
            self.txtComment.insert(END, "\n Fail")
            self.txtComment.update()
            self.txtComment.see(END)
    # -----------------------------------------------------------------------------
    def ztp_wait_sub(self, dev):
        while (True):
            data = dev.sp.readline()
            time.sleep(0.01)
            if data is not None:
                self.txtComment.insert(END, "\n "+str(data))
                self.txtComment.update()
                self.txtComment.see(END)
                break
    # -----------------------------------------------------------------------------

    def ztp_reset_cetificate(self, dev, reset_type):
        # --- reset certificate -----------------------------------------------------------
        data = "AT+PROV_RESET=".encode() + reset_type.encode() + '\n'.encode()
        dev.sp.write(data)
        time.sleep(0.01)

        data = dev.sp.readline()
        self.txtComment.insert(END, "\n Device Certificate Reset")
        self.txtComment.update()
        self.txtComment.see(END)
        self.txtComment.insert(END, "\n OK\n")
        self.txtComment.update()
        self.txtComment.see(END)
    # -----------------------------------------------------------------------------

    # -----------------------------------------------------------------------------
    def ztp_publish(self, dev, topic, qos, payload):

        # --- AWS Publish -----------------------------------------------------------
        data = "AT+AWS_PUB=".encode() + topic.encode() + ','.encode() + str(
            qos).encode() + ','.encode() + payload.encode() + '\n'.encode()
        dev.sp.write(data)
        time.sleep(0.01)

        data = dev.sp.readline()
        if ("SUCCEED\n".encode() == data):
            self.txtComment.insert(END, "\n OK\n")
            self.txtComment.update()
            self.txtComment.see(END)
        else:
            self.txtComment.insert(END, "\n Fail\n")
            self.txtComment.update()
            self.txtComment.see(END)

        data = dev.sp.readline()
        time.sleep(0.01)

        data = dev.sp.readline()
        if ("EVENT:PUB OK\n".encode() == data):
            self.txtComment.insert(END, "\n OK\n")
            self.txtComment.update()
            self.txtComment.see(END)
        else:
            self.txtComment.insert(END, "\n Fail\n")
            self.txtComment.update()
            self.txtComment.see(END)


def main():
    root = Tk()
    root.geometry("500x400+10+10")
    app = MyFrame(root)
    root.mainloop()

if __name__ == '__main__':
    # root = tk.Tk()
    # app = tkinter.simpledialog.SimpleDialog(root)
    # app = Application(master=root)
    # app.go()
    main()
