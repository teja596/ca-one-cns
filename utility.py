
'''
contains helper functions to perform basic ops.
send/recv http requests.
send/recv email.
'''
import json
import string
import random
import requests

def generate_code(N):
    res = ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k = N))
    return res

#share public key to the recv
def share_key(url,data):
    url =  url + '/connection/recv/'
    x = requests.post(url,data=data,headers={'Content-Type': 'application/octet-stream'})
    return x

def share_key_back(url,data):
    url =  url + '/sender/recv/'
    x = requests.post(url,data=data,headers={'Content-Type': 'application/octet-stream'})
    return x

def send_message(url,msg_text):
    print('the url for the receiver is',url)
    url =  url + '/recv/'
    x = requests.post(url,data=msg_text,headers={'Content-Type': 'application/octet-stream'})
    return x

if __name__=='__main__':
    #print(generate_code(10))
    #share_key('http://0.0.0.0:5000/','mock data')
    send_msg('http://0.0.0.0:5000/','test message 2')
