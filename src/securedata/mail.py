import smtplib
import imaplib
from urllib.parse import unquote
import ssl
import sys
import pwd
import os
import traceback
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from securedata import securedata

userDir = pwd.getpwuid( os.getuid() )[ 0 ]

# Parameters
port = 465
smtp_server = "smtp.gmail.com"
smtp_server_imap = "imap.gmail.com"
username = securedata.getItem("email", "from")
password = securedata.getItem("email", "from_pw")

"""
Sends email from Gmail account described above
"""
def send(subject, body, signature="<br><br>Thanks,<br>Raspberry Pi", to=securedata.getItem("email", "to"), from_name=securedata.getItem("email", "from_name") or "Raspberry Pi"):    
    
    from_name = from_name + f" <{username}>"

    # Handle multiple emails
    if ',' in to:
        send(subject, body, signature, to.replace(to.split(',')[0]+ ',', ''), from_name)
        to = to.split(',')[0]

    # Parse
    body += unquote(signature)
    message = MIMEMultipart()
    message["Subject"] = unquote(subject)
    message["From"] = from_name
    message["To"] = to
    message.attach(MIMEText(unquote(body), "html"))

    # Send Email
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(username, password)
        server.sendmail(message["From"], message["To"], message.as_string())
        securedata.log(f"Sent Email to {to} as {message['From']}: {subject}")

"""
Returns raw, possibly-encoded emails from the Inbox of the Gmail account described above
"""
def check():
    try:
        mail = imaplib.IMAP4_SSL(smtp_server_imap)
        mail.login(username,password)
        mail.select('inbox')

        data = mail.search(None, 'ALL')
        mail_ids = data[1]
        id_list = mail_ids[0].split()
        latest_email_id = str(int(id_list[-1]))

        return mail.fetch(latest_email_id, '(RFC822)' )
                    

    except Exception as e:
        traceback.print_exc() 
        securedata.log(f"Ran into a problem checking mail:{str(e).strip()}", level="error")
   
# By default, mail.send:     
if len(sys.argv) == 3 and sys.argv[0].endswith('mail.py'):
    send(sys.argv[1], sys.argv[2])
    securedata.log(f"Sent Email: {sys.argv[1]}")

if __name__ == "__main__":
	if len(sys.argv) == 1:
    		print(f"sys.argv usage: send <subject>, <body>")