import smtplib
from email.mime.text import MIMEText
from email.header import Header

sender = '2541307967@qq.com'
receivers = ['zchen88@stevens.edu']

message = MIMEText('mail test', 'plain', 'utf-8')
message['From'] = Header("test", 'utf-8')
message['To'] =  Header("test", 'utf-8')

subject = 'mail test'
message['Subject'] = Header(subject, 'utf-8')

try:
    smtpObj = smtplib.SMTP('localhost')
    smtpObj.sendmail(sender, receivers, message.as_string())
    print ("666")
except smtplib.SMTPException:
        print ("Error: 777") 

