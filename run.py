# /usr/bin/env python
# Download the twilio-python library from twilio.com/docs/libraries/python
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import os.path
import os
import datetime

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def happybot():
    '''This bot will store how happy I tell it I am. I'll use the data to
        track my (and perhaps others') happiness over time.

        This function will store the information in a file, happy.txt, in
        its home directory.

    There are a few commands. If a new number texts 'add', the bot
    will add them to the reminders list.

    Personal commands:
    - add <Number> - adds <number> to numbers.txt to remind them
    - 
        '''

    # Start our response
    resp = MessagingResponse()

    # Gather data
    number = request.form['From']
    message_text = request.form['Body']
    datestamp = datetime.datetime.utcnow()
    command = message_text.lower().strip()

    # Report the console that we got a message
    print("\n%s just sent me the message '%s'\n" % (number, message_text))

    if command == 'help':
        helpmessage = "You have a few commands:\n"
        helpmessage += "add: Adds the number you texted from. I may remove this periodically, if too many people sign up.\n"
        helpmessage += "remove: Removes you from the reminders list. You will still be able to text your happiness levels, though!\n"
        helpmessage += "deliver: I can fetch you your plot for this month so far.\n"
        helpmessage += "\nAlso, you can text me something about why you're feeling how you are, and I'll remind you about that when I deliver your data back!\n"
        helpmessage += "\nSince this is starting to get a few more people in it, you should know your data is kept private, and if it ever gets used for anything other than what it is now, you will be asked first.\n"
        resp.message(helpmessage)
        return str(resp)

    # If the text asks for it, add them to thee list to remind
    if command == 'add':
        # Detect any change
        flag = 1
        with open('numbers.txt', 'r') as f:
            for line in f:
                if line.strip() == number:
                    flag = 0
        # If they're not already in there, add them
        if flag:
            with open('numbers.txt', 'a') as f:
                f.write(number+'\n')
            resp.message('Added you to the reminders list!')
        else:
            resp.message("You're already on the reminder list!")

        return str(resp)

    if command == 'remove':
        print("Removing %s from the mailing list" % number)
        f = open('numbers.txt', 'r')
        numbers = f.readlines()
        f.close()
        with open('numbers.txt', 'w') as f:
            for num in numbers:
                if num != number+'\n':
                    f.write(num)
        resp.message("Removed you from the mailing list")
        return str(resp)

    if number == '+447730031507':
        # Get the command I sent it
        command = message_text.split(' ')[0].lower()
        arguments = None
        # If I asked for any arguments, get them
        if len(message_text.split(' ')) > 0:
            arguments = message_text.lower().split(' ')[1:]

        # Report to the console what we got
        print("Command: %s\nArgument(s): %s" % (command, arguments))

        # Parse commands
        if command == 'poo':
            print("James is taking a shit")
            with open("shits.txt", 'a') as f:
                data = "%s, %s\n" % (number, datestamp)
                f.write(data)
            return str(request.form)

        # List the numbers on the reminder roster
        if command == 'list':
            print("Listing the numbers I remind to text me...")
            numbers = []
            with open('numbers.txt', 'r') as f:
                for line in f:
                    numbers.append(line)
            numbers_list = ''.join(numbers)

            resp.message("The following people are on the reminders list:\n" + numbers_list)
            return str(resp)

        if command == 'deliver':
            import plotCurrentHappiness

        # Add a number to the schedule
        if command == 'add':
            if arguments==None:
                resp.message("Sorry, I didn't get a number...")
                return str(resp)
            with open('numbers.txt', 'a') as f:
                new_number = arguments[0]
                if list(new_number)[0] == '0':
                    new_number = list(new_number)
                    new_number[0] = '+44'
                new_number = ''.join(new_number)
            print("Adding %s to the mailing list" % new_number)
            f.write(new_number+'\n')
            return str(resp)

    # Prep the rejection message in case we get an invalid response
    reject = '%s is not between 1 and 10. Try again' % message_text

    # Check we got an integer
    try:
        message_text = int(message_text)

        # Check that the file happy.txt exists. If it doesn't, create it.
        fname = 'happy.txt'
        if not os.path.isfile(fname):
            print("\nThe file, happy.txt, does not exist. Creating it now...\n")
            open(fname, 'a').close()

    except:
        # If they dont respond with a number, reject it and exit.
        print('Bad message:\n"%s"' % message_text)
        resp.message("That wasn't a number, but I'll log it and remind you of that in your next summary.\nI added a help function! Text 'help' to get it!")
        message_text = message_text.replace(',', '')
        # Store the bad message in a junk file. I might do something with this, perhaps for streamlining
        data = "%s, %s, '%s'\n" % (number, datestamp, message_text)
        with open('junk.txt', 'a') as f:
            f.write(data)
        return str(resp)

    if message_text > 10 or message_text < 0:
        resp.message(reject)
        return str(resp)

    # Append the file with the data. Format:
    #  <User>, <datestamp>, <Score>
    data = "%s, %s, %s\n" % (number, datestamp, message_text)
    with open(fname, 'a') as f:
        f.write(data)

    return str(resp)

if __name__ == "__main__":
    app.run(debug=False)
