import smtplib
import json 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from Database import *

def forget_password(email, password, name):
    try:
        server = smtplib.SMTP('smtp.office365.com','587')
        #server = smtplib.SMTP(host='smtp.office365.com')
        #server.connect('smtp.office365.com','587')
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login("do-not-reply@labournet.in","Donotreply@123")

        msg = MIMEMultipart()

        msg['From'] = "do-not-reply@labournet.in"
        msg['To'] = email
        msg['Subject'] = "[NEO] Reg: Your Request For Forgot Password"

        html_msg= config.html_email_msg
        html_msg = html_msg.format(name,password)

        msg.attach(MIMEText(html_msg, 'html'))

        res = server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.quit()

        return {'status':True,'description':'Email sent'}
    except:
        return {'status':False,'description':'Unable to sent email'}

def UAP_Batch_Creation_MAIL(RequestId,SDMSBatchId,requested_date):
    try:
        server = smtplib.SMTP('smtp.office365.com','587')
        #server = smtplib.SMTP(host='smtp.office365.com')
        #server.connect('smtp.office365.com','587')
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login("do-not-reply@labournet.in","Donotreply@123")

        msg = MIMEMultipart()

        msg['From'] = "do-not-reply@labournet.in"
        msg['To'] = config.NAVRITI_SPOC_EMAIL
        msg['Cc'] = ','.join(config.NAVRITI_ASSESSMENT_EMAIL_CC)
        msg['Subject'] = "LN NEO - An Assessment Has Been Scheduled For Batch - "+str(SDMSBatchId)

        html_msg= config.html_email_msg_uap_batch_creation
        html_msg = html_msg.format('Navriti Assessment Team',RequestId,SDMSBatchId,requested_date)

        msg.attach(MIMEText(html_msg, 'html'))
        res = server.sendmail(msg['From'], [msg['To']] + config.NAVRITI_ASSESSMENT_EMAIL_CC , msg.as_string())
        server.quit()

        return {'status':True,'description':'Email sent'}
    except:
        return {'status':False,'description':'Unable to sent email'}
