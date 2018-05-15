#!/usr/bin/env python
# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client
import os

# Your Account Sid and Auth Token from twilio.com/console
account_sid = "AC7c41820378f127e30a8fc7aef50bd417"
auth_token = '64cd73675b8ce7bbbd87b218b68ae51d'
client = Client(account_sid, auth_token)

print("Reminding...")

fname = "/home/pi/Python/SMS/numbers.txt"

numbers = []
if os.path.isfile(fname):
    with open(fname, 'r') as f:
        for line in f:
            if line != '':
                numbers.append(line.strip())
    print("I found the following numbers")
    print(numbers)
else:
    print("Numbers doesn't exist. Initialising...")
    numbers = ['+447730031507']
    with open(fname, 'a') as f:
        f.write(numbers[0]+'\n')


ask = "Are you having a good day?\n1: Worst day ever\n10: Best day ever"

for number in numbers:
    message = client.messages.create(
                              body=ask,
                              from_="+441782454191",
                              to=str(number)
                          )
    print("Sent a message to %s" % number)
