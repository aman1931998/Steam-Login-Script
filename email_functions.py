# -*- coding: utf-8 -*-
"""
Created on Sat Apr 17 13:48:51 2021

@author: aman1
"""
import time
from datetime import datetime, timedelta
import imaplib
import email
# from email.header import decode_header
# import webbrowser, os
# import re
# import pickle
from config import max_fetch_login_code_attempts
'''
domain = 'mail.mgomailcs.xyz'
email_address = 'funny715alluring7187@mgomailcs.xyz'
email_password = 'SQL8kbHMSo'
'''

def establish_connection_to_mailserver(domain):
    try:
        imap = imaplib.IMAP4_SSL(domain, imaplib.IMAP4_SSL_PORT)
    except:
        raise Exception("Unable to establish connection with the mail server.")
    return imap


def imap_login_into_mail(imap, email_address, email_password):
    assert type(imap) == imaplib.IMAP4_SSL and '@' in email_address
    # Logging in
    output = imap.login(email_address, email_password)
    if output[0] == 'OK':
        return imap
    else:
        raise Exception("Unable to Log in.")

def imap_logout_of_mail(imap):
    output = imap.logout()
    if output[0] == 'BYE':
        return True
    else:
        raise Exception("Unable to Log out.")

def get_steam_code_from_mail(imap):  # add code to check latest mail (without unseen filter)
    # Selecting inbox
    rv, data = imap.select("INBOX", readonly = False)
    
    # Getting all unseen mails
    rv, data = imap.search(None, '(UNSEEN)')
    if data == [''] or data == [b'']:
        return "No new mail found."
    
    # getting ID of latest mail
    ids = data[0].split()
    latest_id = ids[-1]
    
    # Opening latest mail
    result, data = imap.fetch(latest_id, "(RFC822)")
    msg = email.message_from_bytes(data[0][1])  
    assert msg.is_multipart() == True
    # msg_items = msg.items()
    msg_date_time = msg['Date']
    msg_date_time = datetime.strptime(msg_date_time[:msg_date_time.rindex(' ')], "%a, %d %b %Y %H:%M:%S") + timedelta(hours = 12, minutes = 30)   # - timedelta(hours = int(msg_date_time[msg_date_time.rindex(' ') + 1:][2:3]))
    if datetime.now() - msg_date_time > timedelta(minutes = 5):
        return "No new mail received yet."
    msg_part = list(msg.walk())[0]
    msg_body = msg_part.get_payload()[0]
    msg_body_parts = msg_body.get_payload().split('\n')
    
    steam_guard_code = msg_body_parts[5][:-1]
    steam_guard_code_2 = msg_body_parts[6][:-1]
    try:
        if len(steam_guard_code) == 5:
            return steam_guard_code
        elif len(steam_guard_code_2) == 5:
            return steam_guard_code_2
        else:
            return "Found a possible steam guard code but not equal to 5 characters."
    except:
        return "Internal Error."

def get_login_code(email_address, email_password, domain):
    assert email_address != None and email_password != None and domain != None
    imap = establish_connection_to_mailserver(domain)
    imap = imap_login_into_mail(imap, email_address, email_password)
    attempt_count = 0
    while attempt_count < max_fetch_login_code_attempts:
        output_code = get_steam_code_from_mail(imap)
        if len(output_code) == 5:
            return str(output_code)
        else:
            print(output_code)
            time.sleep(1.2)
    return "Unable to fetch steam guard code."

