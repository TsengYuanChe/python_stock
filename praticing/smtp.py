import sys
sys.path.append('/Users/tseng/Desktop/程式交易')
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from AES_Encryption.encrype_process import *
def send_mail(mail_list:list, subject:str, body:str, mode:str, file_path:list, file_name:list):
    msg = MIMEMultipart()
    user_id = 'adam880501@gmail.com'
    password = 'xuei svsj vybf mtpp'
    msg['From'] = user_id
    msg['To'] = ",".join(mail_list)
    msg['Subject'] = subject
    if mode =='html':
        msg.attach(MIMEText(body, mode))
    else:
        msg.attach(MIMEText(body))
    if file_path==None:
        pass
    else:
        for x in range(len(file_path)):
            with open(file_path[x], 'rb') as opened:
                openedfile = opened.read()
            attachedfile = MIMEApplication(openedfile)
            attachedfile.add_header('content-disposition', 'attachment', filename= file_name[x])
            msg.attach(attachedfile)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(user_id, password)
    text = msg.as_string()
    server.sendmail(user_id, mail_list, text)
    server.quit()

mail_list = ['adam880614@gmail.com']
subject = 'testtest'
body = 'test'
file_path = [r"/Users/tseng/Desktop/程式交易/test_fig.png"]
file_name = ["test.fig.png"]
send_mail(mail_list, subject, body, 'text', file_path, file_name)