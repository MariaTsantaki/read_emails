#!/usr/bin/python

import poplib
import email
import os
import string
import imaplib
import argparse

parser = argparse.ArgumentParser(description='Insert basic data to download emails')
parser.add_argument('id', help='username')
parser.add_argument('password', help='password')
parser.add_argument('server', help='mail server')
parser.add_argument('folder', help='Specify folder, e.g. Inbox')
args = parser.parse_args()

mailServer = str(args.server)
emailID = str(args.id)
emailPass = str(args.password)
Folder = str(args.folder)

#Maybe not the most pythonic way. Based on comments on stackoverflow.

def get_first_text_block(raw_email, i):
    email_message_instance = email.message_from_string(raw_email)
    maintype = email_message_instance.get_content_maintype()
    output = open('email_%d' %i,'w') 
    if maintype == 'multipart':
        for part in email_message_instance.get_payload():
            if part.get_content_maintype() == 'text':
                body = part.get_payload()
    elif maintype == 'text':
        body = email_message_instance.get_payload()
    output.write(body)
    output.close()
    return 

conn= imaplib.IMAP4_SSL(mailServer)
conn.login(emailID, emailPass)
conn.select(Folder)
result, data = conn.search(None, "ALL")
ids = data[0] # data is a list.

id_list = ids.split() # ids is a space separated string
print "Number of emails in folder: %s " % len(id_list)

for i, num in enumerate(data[0].split()):
    result, data = conn.fetch(num, '(RFC822)')
    get_first_text_block(data[0][1], i)
