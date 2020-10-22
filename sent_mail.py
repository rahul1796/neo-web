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

def certification_stage_change_mail(NewStageId,emailTo,emailToName,EmailCC,Batch_Code):
    #print(NewStageId,emailTo,emailToName,EmailCC,Batch_Code)
    try:
        server = smtplib.SMTP('smtp.office365.com','587')
        #server = smtplib.SMTP(host='smtp.office365.com')
        #server.connect('smtp.office365.com','587')
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login("do-not-reply@labournet.in","Donotreply@123")

        msg = MIMEMultipart()
        stage_name=''
        if NewStageId==1:
            stage_name='Requested For Printing'
        if NewStageId==2:
            stage_name='Sent For Printing'
        if NewStageId==3:
            stage_name='Sent To Center'
        if NewStageId==4:
            stage_name='Received By Center'
        if NewStageId==5:
            stage_name='Planned For Distribution'
        if NewStageId==6:
            stage_name='Distributed'
        msg['From'] = "do-not-reply@labournet.in"
        msg['To'] = emailTo
        msg['Cc'] = EmailCC
        msg['Subject'] = "LN NEO - "+str(Batch_Code)+" Certificates " + str(stage_name)
        html_msg= config.html_email_msg_certification_stage_change
        html_msg = html_msg.format(emailToName,Batch_Code,stage_name,EmailCC)
        msg.attach(MIMEText(html_msg, 'html'))
        for path in [files]:
            part = MIMEBase('application', "octet-stream")
            with open(path, 'rb') as file:
                part.set_payload(file.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition',
                            'attachment; filename="{}"'.format(Path(path).name))
        #msg.attach(part)
        
        #print(msg['From'], [msg['To']] + EmailCC.split(",") , msg.as_string())
        res = server.sendmail(msg['From'], [msg['To']] + EmailCC.split(",") , msg.as_string())
        server.quit()

        return {'status':True,'description':'Email sent'}
    except:
        return {'status':False,'description':'Unable to sent email'}

def UAP_Batch_Creation_MAIL(RequestId,SDMSBatchId,requested_date,center_name,course_name,customer_name,cm_emails,files):
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
        msg['Cc'] = ','.join(config.NAVRITI_ASSESSMENT_EMAIL_CC) +',' +str(cm_emails)
        ccList= [msg['Cc']]
        ccList = list(dict.fromkeys(ccList))
        msg['Subject'] = "LN NEO - An Assessment Has Been Scheduled For Batch - "+str(SDMSBatchId)

        html_msg= config.html_email_msg_uap_batch_creation
        html_msg = html_msg.format('Navriti Assessment Team',RequestId,SDMSBatchId,center_name,course_name,customer_name,requested_date)

        msg.attach(MIMEText(html_msg, 'html'))

        for path in [files]:
            part = MIMEBase('application', "octet-stream")
            with open(path, 'rb') as file:
                part.set_payload(file.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition',
                            'attachment; filename="{}"'.format(Path(path).name))
        #msg.attach(part)
        #print(msg['From'], [msg['To']] + ccList , msg.as_string())
        res = server.sendmail(msg['From'], [msg['To']] + ccList , msg.as_string())
        server.quit()

        return {'status':True,'description':'Email sent'}
    except:
        return {'status':False,'description':'Unable to sent email'}
