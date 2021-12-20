import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from textblob import TextBlob
import nltk



# --------------------------EMAIL AUTOMATATION----------------------

def notification(row):
    if row < 0.3:
        send_email()


def send_email():
    sender = 'insert sender email'
    receiver = 'insert receiver email'

    message = """From: C.Safe Team <insert sender email>
    To: To Person <insert receiver email>
    Subject: Crypto Warning about Bitcoin

    Due to a recent negative news piece about Bitcoin, we suggest you monitor your coin
    as a drop in its price is highly likely.
    """

    try:
        session = smtplib.SMTP('smtp.gmail.com', 587)
        session.ehlo()
        session.starttls()
        session.ehlo()
        session.login(sender, '')
        session.sendmail(sender, receiver, message)
        session.quit()
        print("Successfully sent email")

    except smtplib.SMTPException:
        print("Error: unable to send email")


bitcoin_sentiments['polarity'].apply(notification)