from email.mime.text import MIMEText
from email.header import Header
import smtplib


def send_email(text, subject="hints"):
    mail_host = "smtp.163.com"
    mail_user = "xxx@163.com"
    mail_pass = "xxx"

    sender = 'xxx@163.com'
    receivers = ['xxx@163.com']

    message = MIMEText(text, 'plain', 'utf-8')
    message['From'] = Header("system monitor", 'utf-8')
    message['To'] = Header("administrator", 'utf-8')
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP_SSL(mail_host, 465)
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print('send email successfully')
    except smtplib.SMTPException as e:
        print('Error: cann\'t send email', e)