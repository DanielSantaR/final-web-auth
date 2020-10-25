from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

""" 
emailTo = "daniel.torresg@udea.edu.co"
subject = "Correo de Prueba con métodos"
message = "Este es un correo de prueba, entonces hay que mirar" """

""" SMTP_PASSWORD = "Mauricio8"
SMTP_USER = "automaticemail8@gmail.com"
SMTP_HOST = 'smtp.gmail.com'
SMTP_PORT = '587' """


def send_email(*, email_to, subject, message):
    msg = MIMEMultipart()
    message = message 
    # create message object instance
    msg = MIMEMultipart()
    message = message    
    # setup the parameters of the message
    password = SMTP_PASSWORD
    msg['From'] = SMTP_USER
    msg['To'] = emailTo
    msg['Subject'] = subject
    # add in the message body
    msg.attach(MIMEText(message, 'plain'))    
    #create server
    server = smtplib.SMTP(SMTP_HOST + ': ' + SMTP_PORT)    
    server.starttls()    
    # Login Credentials for sending the mail
    server.login(msg['From'], password)
    # send the message via the server.
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.quit()
