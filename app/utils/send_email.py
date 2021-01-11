import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Union

from app.core.config import Settings, get_settings

settings: Settings = get_settings()


def send_email(*, email_to: str, subject: str, message: Union[str, MIMEText]) -> bool:
    try:
        msg = MIMEMultipart()
        # create message object instance
        msg = MIMEMultipart()
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
    message = MIMEText(template_str.format(code=code), "html")
    flag = send_email(email_to=email_to, subject=subject, message=message)
    return flag


def send_new_account(*, email_to: str, name: str, username: str):
    with open("./app/email_templates/new_account.html") as f:
        template_str = f.read()
    subject = "Thanks for Create a new Account"
    message = MIMEText(
        template_str.format(
            name=name,
            username=username,
            password="Ask for the password to the assistant",
        ),
        "html",
    )
    flag = send_email(email_to=email_to, subject=subject, message=message)
    return flag


def send_assigned_vehicle(*, email_to: str,  plate: str, brand: str, model: str, color: str, vehicle_type: str):
    with open("./app/email_templates/assigned_vehicle.html") as f:
        template_str = f.read()
    subject = "A vehicle has been assigned"
    message = MIMEText(
        template_str.format(            
            plate=plate,
            brand=brand,
            model=model,
            color=color,
            vehicle_type=vehicle_type
        ),
        "html",
    )
    flag = send_email(email_to=email_to, subject=subject, message=message)
    return flag

    
def send_updated_personal_information(*, email_to: str):
    with open("./app/email_templates/updated_personal_information.html") as f:
        template_str = f.read()
    subject = "Update Personal Information"
    message = MIMEText(
        template_str.format(),"html",
    )
    flag = send_email(email_to=email_to, subject=subject, message=message)
    return flag


    
def send_reparation_detail(*, email_to: str,  description: str, cost: float):
    
    with open("./app/email_templates/reparation_detail.html") as f:
        template_str = f.read()
    subject = "New Reparation Detail"
    message = MIMEText(
        template_str.format(
            description=description, 
            cost=cost
        ),
        "html",
    )
    flag = send_email(email_to=email_to, subject=subject, message=message)
    return flag


def send_new_owner(*, email_to: str, identity_card: str, name: str, surname: str, phone: str):
    with open("./app/email_templates/new_owner.html") as f:
        template_str = f.read()
    subject = "New account created successfully"
    message = MIMEText(
        template_str.format(
            identity_card=identity_card,
            name=name,
            surname=surname,
            phone=phone,
            email=email_to
        ),
        "html",
    )
    flag = send_email(email_to=email_to, subject=subject, message=message)
    return flag

    
def send_updated_vehicle(*, email_to: str):
    with open("./app/email_templates/updated_vehicle.html") as f:
        template_str = f.read()
    subject = "Update Vehicle Information"
    message = MIMEText(
        template_str.format(),"html",
    )
    flag = send_email(email_to=email_to, subject=subject, message=message)
    return flag
