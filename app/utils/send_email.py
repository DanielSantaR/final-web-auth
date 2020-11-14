# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText


# def send_email(*, email_to, subject, message):
#     msg = MIMEMultipart()
#     message = message
#     # create message object instance
#     msg = MIMEMultipart()
#     message = message
#     # setup the parameters of the message
#     password = SMTP_PASSWORD
#     msg["From"] = SMTP_USER
#     msg["To"] = emailTo
#     msg["Subject"] = subject
#     # add in the message body
#     msg.attach(MIMEText(message, "plain"))
#     # create server
#     server = smtplib.SMTP(SMTP_HOST + ": " + SMTP_PORT)
#     server.starttls()
#     # Login Credentials for sending the mail
#     server.login(msg["From"], password)
#     # send the message via the server.
#     server.sendmail(msg["From"], msg["To"], msg.as_string())
#     server.quit()
