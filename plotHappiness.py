#!/usr/bin/env python

import matplotlib
# Since I'm in the terminal, and testing over ssh, use the Agg backend of matplotlib
matplotlib.use('Agg')

from twilio.rest import Client
from imgurpython import ImgurClient

import os
import datetime
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.dates import  DateFormatter

live = False

# Check we have  adirectory to put graphs in
if not os.path.exists('graphs'):
    os.makedirs('graphs')

# For lookups later
monthNames = np.array(['', 'January', 'Febuary', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October' 'November', 'December'])

# Current month and year
now = datetime.datetime.now()
current_month = now.month
current_year  = now.year


# Read in the data from the file, numbers.txt
stored_data = {}
with open('happy.txt', 'r') as f:
    for line in f:
        line = line.split(',')
        number    = line[0].strip()
        timestamp = datetime.datetime.strptime(line[1].strip(), "%Y-%m-%d %H:%M:%S.%f")
        score     = int(line[2])

        if number not in stored_data.keys():
            # Create a new entry for the new number
            stored_data[number] = []

        # Store the data
        stored_data[number].append([timestamp, score])

# Get the junk texts
junk_texts = {}
with open('junk.txt', 'r') as f:
    for line in f:
        line = line.split(',')
        number    = line[0].strip()
        timestamp = datetime.datetime.strptime(line[1].strip(), "%Y-%m-%d %H:%M:%S.%f")
        text      = ','.join(line[2:])

        if number not in junk_texts.keys():
            # Create a new entry for the new number
            junk_texts[number] = []

        # Store the data
        junk_texts[number].append([timestamp, text])


# Convert our data to numpy arrays
for number in stored_data.keys():
    stored_data[number] = np.array(stored_data[number])

# List of the graphs we make
created_files = {}

# Plot the scores of each number
for number, data in stored_data.iteritems():
    dates = []
    scores = []

    for i,j in data:
        if i.month == current_month:
            dates.append(i)
            scores.append(j)

    dates = matplotlib.dates.date2num(dates)

    fig, ax = plt.subplots()
    ax.plot_date(dates, scores,
        markeredgecolor='red', markerfacecolor='red' , marker='o',
        linestyle='--', color='blue', linewidth=1)

    ax.xaxis.set_major_formatter( DateFormatter('%d') )
    ax.spines['right'].set_color('none')
    ax.spines['left'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.set_ylim(0, 5.5)
    ax.set_title('%s for %s %s' % (number, monthNames[current_month], current_year))
    ax.set_xlabel("Day")
    ax.set_ylabel("Score")
    plt.tight_layout()

    oname = 'graphs/%s-%s-%s' % (number, monthNames[current_month], current_year)
    created_files[number] = oname
    plt.savefig(oname)


# Imgur client setup
f = open('im_auth.txt', 'r')
auth = [i.strip() for i in f.readlines()]
f.close()
im_client_id = auth[0]
im_client_secret = auth[1]
im_client = ImgurClient(im_client_id, im_client_secret)

# Twilio client setup
f = open('twi_auth.txt', 'r')
auth = [i.strip() for i in f.readlines()]
account_sid = auth[0]
auth_token = auth[1]
twi_client = Client(account_sid, auth_token)

if live:
    print("We are live!")
    nums = stored_data.keys()
else:
    print("Testing Version")
    nums = ['+447730031507']

for num in nums:
    image_path = created_files[num]+'.png'

    their_texts = junk_texts[num]
    description = ''
    for date,text in their_texts:
        description += date.strftime('%d %b, %Y ') + ('- %s\n' % text)

    # Setup the configuration for the upload
    config = {
        'album': None,
        'name': 'Happybot Upload',
        'description': description,
        'title': 'Your scores last month'
        }

    image = im_client.upload_from_path(image_path, config=config, anon=False)

    imagelink = ("Here is your happiness graph for %s!\n%s" % 
        (monthNames[current_month], image['link']))

    message = twi_client.messages.create(
                              body=imagelink,
                              from_="+441782454191",
                              to=str(num)
                          )
    print("Sent %s their happiness chart, at %s" % (num, image['link']))