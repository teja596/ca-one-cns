'''
the system works on p2p communication without third party interaction.
removal of third party ensures extra level of security in the chat.
'''

from crypt import methods
from flask import Flask,request,render_template,redirect,url_for
import rsa
import pickle
from flask_mail import Mail,Message
import cryptocode
import json
from utility import generate_code,share_key,send_message,share_key_back

