import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.core.config import Settings, get_settings

settings: Settings = get_settings()


def send_email(*, email_to: str, subject: str, message: str) -> bool:
    try:
        msg = MIMEMultipart()
        message = message
        # create message object instance
        msg = MIMEMultipart()
        message = message
        # setup the parameters of the message
        password = settings.SMTP_PASSWORD
        msg["From"] = settings.SMTP_USER
        msg["To"] = email_to
        msg["Subject"] = subject
        # add in the message body
        msg.attach(message)
        # create server
        server = smtplib.SMTP(f"{settings.SMTP_HOST}:{settings.SMTP_PORT}")
        server.starttls()
        # Login Credentials for sending the mail
        server.login(msg["From"], password)
        # send the message via the server.
        server.sendmail(msg["From"], msg["To"], msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(e)
        return False

def send_code_email(*, email_to: str, code: str):
    with open("./app/email_templates/send_code.html") as f:
        template_str = f.read()
    subject = "Security Code"
    message = MIMEText(template_str.format(code=code), 'html')
    send_email(email_to = email_to, subject = subject, message = message)


def send_new_account(*, email_to: str, name: str, username: str):
    with open("./app/email_templates/new_account.html") as f:
        template_str = f.read()
    subject = "Thanks for Create a new Account"
    message = MIMEText(template_str.format(name=name, username=username), 'html')
    send_email(email_to = email_to, subject = subject, message = message)
