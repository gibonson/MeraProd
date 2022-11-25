import smtplib, ssl
from email.mime.text import MIMEText
from configparser import ConfigParser



def emailSender():
    config = ConfigParser()
    config.read("config/config_email.ini")
    print(config.sections())
    print(list(config['EMAIL']))


    sender = config['EMAIL']['user_name']
    receiver = config['EMAIL']['default_recipient']
    user = config['EMAIL']['user_name']
    password = config['EMAIL']['password']
    context = ssl.create_default_context()

    msg = MIMEText('notificacion example')

    msg['Subject'] = 'Test mail'
    msg['From'] = sender
    msg['To'] = receiver

    with smtplib.SMTP_SSL("s5.cyber-folks.pl", 465, context=context) as server:

        server.login(user, password)
        server.sendmail(sender, receiver, msg.as_string())
        print("mail successfully sent")