# Import smtplib and email modules
import smtplib
from email.message import EmailMessage
import time
import logging
import json

def send_email(msg_content, msg_subject, msg_mail_from, msg_mail_to):   
    logging.info('Sending Message')

    msg = EmailMessage()
    msg.set_content(msg_content)
    msg['Subject'] = msg_subject
    msg['From'] = msg_mail_from
    msg['To'] = msg_mail_to
    
    # Send the message via our own SMTP server.
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    with open('include/credentials.json', 'r') as file:
        credentials = json.load(file)
    
    pwd = credentials[0]['pass']
    username = credentials[0]['username']

    # Authentication 
    try:
        s.login(username, pwd)  
        s.send_message(msg)
    except Exception as e: # skipcq: PYL-W0703
        logging.error(e)
    time.sleep(5)
    s.quit()
    logging.info('Email was correctly executed')


if __name__ == '__main__':

    logging.basicConfig(format='%(asctime)s: %(message)s', level=logging.INFO,
                        datefmt='%H:%M:%S')
    
    with open('include/credentials.json', 'r') as f:
        email_address = json.load(f)
    
    content = 'Test E-Mail from Module'
    subject = 'E-Mail Module Test'
    mail_from = 'Module Test'
    send_email(content,subject, mail_from, email_address[1]['email'])
