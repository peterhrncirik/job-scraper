import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

def notify(jobs, to_email=os.getenv('TO'), server=os.getenv('SERVER'), port=os.getenv('PORT'), from_email=os.getenv('FROM'), password=os.getenv('PASSWORD')):

    print(f'With love from {from_email} to {to_email}')

    # The message
    subject = 'Jobs you might like'
    text = "\r\n".join(jobs)
    msg = EmailMessage()
    msg.set_content(text)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    # Communication
    server  = smtplib.SMTP_SSL(server, port)
    server.login(from_email, password)
    server.send_message(msg)
    server.quit()
