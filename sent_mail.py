import smtplib
import json 
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders
from Database import *
from Database import config

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
    except Exception as e:
        print(e)
        return {'status':False,'description':'Unable to sent email'}

def certification_stage_change_mail(NewStageId,emailTo,emailToName,EmailCC,Batch_Code,files):
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
        msg['Cc'] = EmailCC + ',neo.helpdesk@labournet.in'
        msg['Subject'] = "LN NEO - "+str(Batch_Code)+" Certificates " + str(stage_name)
        html_msg= config.html_email_msg_certification_stage_change
        html_msg = html_msg.format(emailToName,Batch_Code,stage_name,EmailCC)
        msg.attach(MIMEText(html_msg, 'html'))
        if files != '':
            for path in [files]:
                part = MIMEText('application', "octet-stream")
                with open(path, 'rb') as file:
                    part.set_payload(file.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition',
                                'attachment; filename="{}"'.format(Path(path).name))
                msg.attach(part)
        res = server.sendmail(msg['From'], [msg['To']] + EmailCC.split(",") + ['neo.helpdesk@labournet.in'] , msg.as_string())
        server.quit()

        return {'status':True,'description':'Email sent'}
    except Exception as e:
        print(e)
        return {'status':False,'description':'Unable to sent email'}
def ShikshaEnrolmentMail(candidate_name,enrolment_id,course,email_id,mobile):
    #print(NewStageId,emailTo,emailToName,EmailCC,Batch_Code)
    try:
        server = smtplib.SMTP('smtp.office365.com','587')
        #server = smtplib.SMTP(host='smtp.office365.com')
        #server.connect('smtp.office365.com','587')
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login("do-not-reply@labournet.in","Donotreply@123")
        dell_logo=config.dell_logo_path
        files=config.dell_attachment_path

        msg = MIMEMultipart()
        
        msg['From'] = "do-not-reply@labournet.in"
        msg['To'] = email_id
        msg['Subject'] = "DELL CSR [LabourNet Academy] Confirmation of Account Creation"
        html_msg='''
                        <div>
            <p style="font-size:12pt;font-family:Times New Roman,serif;margin:0;">Dear <b>{},</b><br>
            <br>
            Congratulations on being enrolled in the DELL CSR learning program to help you build a successful career. An account has been created for you at the LabourNet Academy, from where you could access the <b>{}</b> course material.
            <br><br>
        
            This is an <u>8-week learning program</u> providing you access to extensive learning material, engaging with peers, participate in weekly quizzes, win prizes and much more. 
            <br>
            <u>Read complete course information in PDF attached</u>.
            <br><br>
            Kindly click on the below mentioned URL and login into your account to access the course material. 
            <br><br>
            URL  &emsp; &emsp; &emsp;  &emsp; &ensp;&nbsp;        : &emsp;  <b>https://shiksha.ai/</b>
            <br>
            USERNAME  &emsp; &emsp;    : &emsp; <b>{}</b>
            <br>
            PASSWORD   &emsp; &emsp;    : &emsp;  <b>Pass#123 </b>
            <br>
            </p>
            </div>
            <br>

            <div align="left" style="font-size:12pt;font-family:Times New Roman,serif;text-align:left;margin:0;">
           

            <p style="font-size:12pt;font-family:Times New Roman,serif;margin:0;">
            <b>  Best Regards,  </b>
            <br>
            Dell Team
            <br>
            <img src="{}"  width="80" height="80" style="float:left">
            </p>
            
            <br>
            </div>
            
        '''   
        #<img src="{}"  width="42" height="42" style="float:left"> 
            
        html_msg = html_msg.format(candidate_name,course,email_id,dell_logo)
        msg.attach(MIMEText(html_msg, 'html'))
        if files != '':
            for path in [files]:
                part = MIMEText('application', "octet-stream")
                with open(path, 'rb') as file:
                    part.set_payload(file.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition',
                                'attachment; filename="{}"'.format(Path(path).name))
                msg.attach(part)
        res = server.sendmail(msg['From'], msg['To'] , msg.as_string())
        server.quit()

        return {'status':True,'description':'Email sent'}
    except Exception as e:
        #print('exc='+str(e))
        return {'status':False,'description':'Unable to sent email '+ str(e)}

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
            part = MIMEText('application', "octet-stream")
            with open(path, 'rb') as file:
                part.set_payload(file.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition',
                            'attachment; filename="{}"'.format(Path(path).name))
            msg.attach(part)
        res = server.sendmail(msg['From'], [msg['To']] + ccList , msg.as_string())
        server.quit()

        return {'status':True,'description':'Email sent'}
    except Exception as e:
        print(e)
        return {'status':False,'description':e}