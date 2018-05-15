#!/usr/bin/env python

from umbrella import umbrella_today
from twilio.rest import Client

account_sid = 'AC7c41820378f127e30a8fc7aef50bd417'
auth_token = '64cd73675b8ce7bbbd87b218b68ae51d'
client = Client(account_sid, auth_token)

if umbrella_today():
    print("It's going to rain today. Messaging...")

    message = client.messages.create(
	body = 'It is going to rain today',
        from_ = '+441782454191',
        to = '+447730031507'
	)

else:
    print("It's not going to rain today.")


