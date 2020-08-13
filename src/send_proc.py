# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client
import os 

# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
account_sid = os.environ.get("TWILIO_SID")
auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
client = Client(account_sid, auth_token)

message = client.messages.create(
                              body='Welcome from the 2071 Chore Bot you filthy fuck',
                              from_='+17692248010',
                              to='+18454440118'
                          )
