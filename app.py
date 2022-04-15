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

app = Flask(__name__)

#smtp setting
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'xyz@gmail.com'
app.config['MAIL_PASSWORD'] = 'app password'
#app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = True
mail=Mail(app)

#common stuff
email_code = None

#data need for sending
self_email = None
public_key_self, private_key_self = rsa.newkeys(2048)
self_url = None

#data needed for receiving
other_email = None
other_url = None
other_public_key = None
auth = 'False'

#list of messages (send/recv) chat
messages = []

#ports
port_A = None
port_B = None

#the user starts the application
@app.route("/",methods=['GET','POST'])
def user_start():
    if request.method=='GET':
        print(request.url)
        global self_url
        self_url = request.url
        return render_template('start_page.html')
    elif request.method=='POST':
        #store email
        global self_email
        self_email = request.form.get('email-input')
        print(self_email)
        if other_public_key:
            return redirect(url_for('accept_conn'))
        return redirect(url_for('user_connect'))

#user tries to connect to the remote application
@app.route("/connect/",methods=['GET','POST'])
def user_connect():
    if request.method=='GET':
        return render_template('connect.html')
    elif request.method=='POST':
        #get the form data
        global other_email,other_url,email_code,self_email,self_url
        other_email = request.form.get('email-input')
        other_url = request.form.get('url-input')
        print(other_email,other_url)
        #send the email(code)
        mail_title = 'code for verification'
        msg = Message(mail_title, sender = app.config['MAIL_USERNAME'], recipients = [other_email])
        email_code = generate_code(10)
        msg.body = f'{email_code} {self_email} {self_url}'
        print(other_email)
        mail.send(msg)
        #send the post request with the public key system 
        key_str = pickle.dumps(public_key_self)
        ret = share_key(other_url,key_str)
        #other_public_key = pickle.loads(ret.text)
        return redirect(url_for('chat_ui'))

#the endpoint for sender to receive public key
@app.route("/sender/recv/",methods=['GET','POST'])
def recv_key_sender():
    if request.method=='POST':
        global other_public_key
        key_str = request.data
        public_key = pickle.loads(key_str)
        other_public_key = public_key
        return pickle.dumps(public_key_self)

#the endpoint to recv connection request (from the sender)
@app.route("/connection/recv/",methods=['GET','POST'])
def recv_conn():
    if request.method=='POST':
        global other_public_key
        key_str = request.data
        public_key = pickle.loads(key_str)
        other_public_key = public_key
        global other_url
        other_url = 'http://' + request.remote_addr + f':{port_B}'
        print("the remote address is ",other_url)

        #send the public key back
        key_str = pickle.dumps(public_key_self)
        share_key_back(other_url,key_str)
        return "successful handshake"

#receiving user completes teh authentication after adding the code
@app.route("/connection/accept/",methods=['GET','POST'])
def accept_conn():
    if request.method=='GET':
        return render_template('accept.html')
    elif request.method=='POST':
        #get the code
        global email_code,other_url
        email_code = request.form.get('code-input')
        print(other_url)
        print(email_code)
        #send the code (encode with the others public key)
        #send the public key
        return redirect(url_for('chat_ui'))

#url for chat ui + js(the user has to type refresh)
@app.route('/chat/')
def chat_ui():
    global messages
    return render_template('chat_ui.html',messages=messages)

#user sends the encrypted message(to other users recv endpoint)
@app.route("/send/",methods=['POST'])
def send_msg():
    global messages,other_url
    msg_text = request.form.get('text')
    msg_user = 'self-message'
    msg = {'user':msg_user,'text':msg_text}
    messages.append(msg)
    #send to the  other user
    #1.) stage 1 encryption
    encoded = cryptocode.encrypt(msg_text,email_code)
    print("the encoded text is ================>",encoded)
    #2.) stage 2 encryption
    enc_msg = rsa.encrypt(encoded.encode(),other_public_key) #only the one with private key can decode
    send_message(other_url,enc_msg)
    return "send message"

#user receives the encrypted message (from other user send endpoint)
@app.route("/recv/",methods=['POST'])
def recv_msg():
    global messages,email_code
    print("the email code is=================>",email_code)
    msg_text = request.data
    #decode the text (stage 2)
    msg_dec= rsa.decrypt(msg_text,private_key_self).decode()
    #decode teh text (stage 1)
    decoded = cryptocode.decrypt(msg_dec, email_code)
    print("the decoded text is===>",decoded) 
    msg_user = 'other-message'
    msg = {'user':msg_user,'text':decoded}
    messages.append(msg)
    return "send message"

if __name__=="__main__":
    import sys
    port_A = int(sys.argv[1])
    port_B = int(sys.argv[2])
    app.run(host="127.0.0.1",port=port_A,debug=True)
