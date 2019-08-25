import smtplib
import ssl
import os
import datetime
from email.message import EmailMessage


def init():
   # Check environment vars
   good_to_go = True

   for env_var in ['MOBILE_USERNAME', 'MOBILE_PASSWORD', 'EMAIL_USERNAME', 'EMAIL_PASSWORD']:
      if os.environ[env_var] is None:
         print("[-] Initialization error - required environment variable not found: {}".format(env_var))
         good_to_go = False

   if not good_to_go:
      quit()


def email_notify(host):
   msg = EmailMessage()
   msg['Subject'] = 'New patient registration from mobile app'
   msg['From'] = os.environ['EMAIL_USERNAME']
   msg['To'] = "fortitudoinc@gmail.com"

   msg.set_content(
   """
   A patient has registered using the mobile app.

   Patient registered at {}

   Request received at {}
   """.format(host, datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
   )

   context = ssl.create_default_context()

   with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
      server.login(os.environ['EMAIL_USERNAME'], os.environ['EMAIL_PASSWORD'])

      server.send_message(msg)
      server.close()