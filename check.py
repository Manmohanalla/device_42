import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import base64

def email(message):
	
	sub = 'Hi NIKHIL'
	fromaddr = "sendmanmohan@gmail.com"
	toaddr = "nikhilmulik2002@gmail.com"
	msg = MIMEMultipart()
	msg['From'] = fromaddr
	msg['To'] = toaddr
	msg['Subject'] = sub
	 
	body = message
	msg.attach(MIMEText(body, 'plain'))
	 
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	password = base64.b64decode("Y2FzdGxlMjA0MCMj")
	server.login(fromaddr, password)
	text = msg.as_string()
	server.sendmail(fromaddr, toaddr, text)
	server.quit()

email('hi this is a email from my third party API')