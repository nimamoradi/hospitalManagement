#!/usr/bin/python
# -*- coding: utf-8 -*-

import getpass

import smtplib
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
import os


def mail(to, subject, text, attach=None):
    try:
        gmail_user = "no.reply.hospitalmgmt@gmail.com"
        gmail_pwd = "wpoekgdTnjvd155"
        msg = MIMEMultipart()
        msg['From'] = gmail_user
        msg['To'] = to
        msg['Subject'] = subject
        msg.attach(MIMEText(text))
        if attach:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(open(attach, 'rb').read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(attach))
            msg.attach(part)
        mailServer = smtplib.SMTP("smtp.gmail.com", 587)
        mailServer.ehlo()
        mailServer.starttls()
        mailServer.ehlo()
        mailServer.login(gmail_user, gmail_pwd)
        mailServer.sendmail(gmail_user, to, msg.as_string())
        print ("email sent" + str(to))
        mailServer.close()

    except smtplib.SMTPAuthenticationError as e:
        print ("email not sent")
        print ("SMTPAuthenticationError: mail server Username and Password not accepted." )

    except smtplib.SMTPRecipientsRefused as e:
        raise smtplib.SMTPRecipientsRefused("Bad Recipient")

    except Exception as e:
        print (type(e).__name__ ),
        print (e)
