"""
Before executing this script install these packages below
pip install selenium
"""
from selenium.webdriver.firefox.options import Options
from email.message import EmailMessage
from selenium import webdriver
from time import sleep
import smtplib
import datetime

import time
import os

# email details
sender_email = ""
receiver_email = ""
password = ""

# twilio authentication


# log file location
file_path = "log.txt"

# global variables
sent_today = False
found_word = False
error = 0

message = EmailMessage()
message['From'] = sender_email
message['To'] = receiver_email
message['Subject'] = "The exam's checker bot just started"
message.set_content("Hey, this email is just for letting you to know that the bot has just started.")
with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
    smtp.starttls()
    smtp.login(sender_email, password)
    smtp.send_message(message)


def email(subject, content):
    # Open the file in binary mode
        with open(file_path, 'rb') as file:
            # Read the file data
            file_data = file.read()

            # Create a message object
            message = EmailMessage()

            # Set the sender, recipient, and subject
            message['From'] = sender_email
            message['To'] = receiver_email
            message['Subject'] = subject

            # Set the message content
            message.set_content(content)


            # Add the file attachment
            message.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=os.path.basename(file_path))

            # Create a SMTP connection
            with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
                # Start the TLS encryption
                smtp.starttls()

                # Login to the sender's email account
                smtp.login(sender_email, password)

                # Send the message
                smtp.send_message(message)

            with open(file_path, 'a', encoding='utf-8') as f:
                message = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " : " + "File sent successfully"
                print(message)
                f.write(message + '\n')

def RunFirefox():
    # create a Firefox webdriver instance
    with open(file_path, 'a', encoding='utf-8') as f:
        message = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " : Creating Firefox webdriver instance" + '\n'
        print(message)
        f.write(message)
    options = Options()
    options.headless = True
    global driver
    driver = webdriver.Firefox(options=options)

RunFirefox()

while found_word == False:
    
    try:
        # Clear cache and cookies
        message = time.strftime("\n" + "%Y-%m-%d %H:%M:%S", time.localtime()) + " : " + "Clearing all cookies and cache"
        print(message)
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(message + '\n')
        driver.delete_all_cookies()

        # load the Twitter page
        message = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " : " + "Loading the Twitter page"
        print(message)
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(message + '\n')
        driver.get("https://twitter.com/BadrJLIL")
        sleep(5)

        # retrieve the full HTML code of the page
        message = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " : " + "Retrieving tweets from the page"
        print(message)
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(message + '\n')
        tweets = driver.execute_script("""
            let tweetElems = document.querySelectorAll('[data-testid="tweet"]');
            let tweets = [];
            for (let tweetElem of tweetElems) {
                let tweet = [];
                tweet = tweetElem.querySelector('div[lang]').textContent;
                tweets.push(tweet);
            }
            return tweets;
        """)

        # check the word "pool" or "piscine"
        for tweet in tweets:
            if "exam" in tweet.lower() or "test" in tweet.lower() :
                found_word = True
                with open(file_path, 'a', encoding='utf-8') as f:
                    message = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " : " + "The word exam or test is found"
                    print(message)
                    f.write(message + "\n")
                
                """
                responseData = (
                    {
                        "from": "My bot",
                        "to": "212641845649",
                        "text": "I think the exam is now launhed, hurry up and do the exam, the tweet content:\n" + tweet + "\n",
                    }
                )
                

                if responseData["messages"][0]["status"] == "0":
                    with open(file_path, 'a', encoding='utf-8') as f:
                        message = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " : " + "SMS sent successfully."
                        print(message)
                        f.write(message + '\n')
                else:
                    with open(file_path, 'a', encoding='utf-8') as f:
                        message = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " : " + f"SMS failed with error: {responseData['messages'][0]['error-text']}"
                        print(message)
                        f.write(message + "\n")

                """
                                   
                email("Exam is launched now", "I think the exam is now launched, hurry up and get your place, the tweet content:\n" + tweet + "\n")
                
                break
                break
        if found_word == False :
            with open(file_path, 'a', encoding='utf-8') as f:
                message = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " : " + "The word exam or test not found"
                print(message)
                f.write(message + "\n")
            # wait for 5 minutes before restart
            message = '\n' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " : " + "Restaring in 5 minutes"
            print(message)
            with open(file_path, 'a', encoding='utf-8') as f:
                f.write(message + '\n')   
            time.sleep(300) # 300 seconds = 5 minutes

        if error > 1 :
            # create email message
            message = f"Subject: the bot is now working fine\n\nDon't worry, the bot is back working now"

            # send email
            message = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " : " + "Sending an email to report the recovery of the bot."
            print(message)
            with open(file_path, 'a', encoding='utf-8') as f:
                f.write(message + '\n')
            email("the bot is now working fine", "Don't worry, the bot is back working now, review the attached log file")
        error = 0


    except Exception as e:
        if str(e).__contains__("Message: Failed to decode response from marionette"):
            RunFirefox()
        else:
            with open(file_path, 'a', encoding='utf-8') as f:
                message = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " : " + f"An exception occurred: {e}"
                print(message)
                f.write(message + "\n")
                error += 1
                
            if error == 2 :
                # send email
                message = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " : " + "Sending an email to report the breakdown of the bot."
                print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " : " + "Sending an email to report the breakdown of the bot.")
                with open(file_path, 'a', encoding='utf-8') as f:
                    f.write(message + '\n')
                    email("the bot is corrupted", "A problem occurred to the bot, check the attached log file and try to fix the bot as soon as possible.")
            elif error == 3 :
                break

            # wait for 15 minutes
            message = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " : " + "Waiting 15 min because an error occurred"
            print(message)
            with open(file_path, 'a', encoding='utf-8') as f:
                f.write(message + '\n')
            time.sleep(900) # 900 seconds = 15 minutes

    # Get the current time
    now = datetime.datetime.now()

    # Check if the current time is after 00:00
    if now.hour >= 00 and now.hour < 22 and sent_today == True:
        message = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " : " + "New report"
        print(message)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(message + '\n')
        sent_today = False
    # Check if the current time is after 22:00
    if now.hour >= 22 and sent_today == False:
        message = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " : " + "Sending today's report"
        print(message)
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write('\n ' + message + '\n')
        email("the Bot today's report", "Hello,\nPlease find in the attached file today's report of the bot.")
        sent_today = True
