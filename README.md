	setup the SMTP service and update the credentials in app.py
	(run both apps)
	A
1.	>>python app.py 5000 7000
1.	the first port number is the for the sender application
2.	the second port number is for the receiver application
2.	B
1.	>>python app.py 7000 5000
1.	the first port number is the for the sender application
2.	the second port number is for the receiver application
	A (initiate the connect)
1.	this application can run on any computer system as a flask-micro-service
1.	open the app on browser
1.	http://127.0.0.1:5000/
2.	The user A has to enter his email and press ubmit
3.	the user has to enter the email and URL of the receiver
4.	an email with the code is sent to B’s email address
5.	the user is taken to the chat UI
	B (accepts the connection)
1.	open the app in browser
1.	http://127.0.0.1:7000/
2.	enter the  email id of B, press submit.
3.	Then he gets the UI to enter the code
1.	the user has to open his email account and copy the code
2.	enter the code in the input , press submit
4.	he will be taken to the chat UI
	both can chat
1.	A can type the message
1.	press send
2.	B has to refresh the page to see the received message

