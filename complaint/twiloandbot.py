# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client

# Set environment variables for your credentials
# Read more at http://twil.io/secure

account_sid = "AC0467eead6081aeae94fc838e272f6a31"
auth_token = "894727009248433dcaa68d44b3e3d8d1"
client = Client(account_sid, auth_token)

call = client.calls.create(
  url="http://demo.twilio.com/docs/voice.xml",
  to="+919677637299",
  from_="+16593000710"
)

print(call.sid)