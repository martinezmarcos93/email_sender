import os
import smtplib
from email.message import EmailMessage
import mimetypes
import schedule
import time

USER_ADRESS = os.environ.get('YOUR MAIL')
USER_PASSWORD = os.environ.get('YOUR PASS')


file_path = 'YOUR_FILE.pdf'


mime_type, _ = mimetypes.guess_type(file_path)

with open(file_path, 'rb') as f:
    file_data = f.read()
    file_name = os.path.basename(file_path)


emails_sent = 0
max_emails = 100

def send_email():
    global emails_sent

    with open('emails.txt', 'r') as f:
        email_list = f.read().split(', ')

    with smtplib.SMTP_SSL('smtp.outlook.com/gmail.com', 465) as smtp:
        smtp.login(USER_ADRESS, USER_PASSWORD)
        for email in email_list:
            if emails_sent >= max_emails:
                break  

            msg = EmailMessage()
            msg['Subject'] = "Python Developer"
            msg['From'] = USER_ADRESS
            msg.set_content('text')  
            msg.add_attachment(file_data, maintype=mime_type, filename=file_name)
            msg['To'] = email
            smtp.send_message(msg)
            emails_sent += 1


schedule.every(15).minutes.do(send_email)

while True:
    schedule.run_pending()
    time.sleep(1)  

