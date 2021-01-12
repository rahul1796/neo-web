def create_report(from_date, to_date, Customers,projects,sub_projects, user_id, user_role_id, report_name):
    '''
    from datetime import datetime
    start_time = datetime.now()
        start_date = '2019-11-01'
        end_date = '2019-12-30'
        coursename=''
        centername=''
        customername=''
    '''
    #print(start_date, end_date, customername, sub_project, coursename, name)
    try:
        import pandas as pd
        import pypyodbc as pyodbc
        import xlsxwriter,re,os
        import threading
        from Database import config
    except:
        return({'Description':'Module Error', 'Status':False})

    try:
        conn_str = config.conn_str
        name_withpath = config.neo_report_file_path + 'report file/'+ report_name
        project_type=1
        writer = pd.ExcelWriter(name_withpath, engine='xlsxwriter')
        workbook  = writer.book
        if sub_projects != '':
            cnxn=pyodbc.connect(conn_str)
            curs = cnxn.cursor()            
            quer = "select mobilization_type from masters.tbl_sub_projects where sub_project_id="+str(sub_projects)
            curs.execute(quer)
            data=curs.fetchall()
            data = 0 if data==[] else data[0][0]
            project_type=int(data)
           
        header_format = workbook.add_format({
            'bold': True,
            'text_wrap': True,
            'valign': 'center',
            'fg_color': '#D7E4BC',
            'border': 1})
        second_header_format = workbook.add_format({
            'bold': True,
            'text_wrap': True,
            'valign': 'center',
            'fg_color': '#e9f789',
            'border': 1})
        light_header_format = workbook.add_format({
            'bold': False,
            'text_wrap': True,
            'valign': 'center',
            'fg_color': '#74dc96',
            'border': 1})

        def trainee_fxn():
            cnxn=pyodbc.connect(conn_str)
            curs = cnxn.cursor()
            sql = 'exec [reports].[sp_sl4_trainee_report] ?, ?, ?, ?, ?,?,?'
            values = (from_date, to_date, Customers,projects,sub_projects, user_id, user_role_id)
            curs.execute(sql,(values))
            data = curs.fetchall()
            data = list(map(lambda x:list(x), data))
            df = pd.DataFrame(data)

            header = ['Training partner details','Trainee Details (Pre-Joining)','Contact details','Trainee disability details','Pre-training details','Course details']
            header_size = [3,22,33,35,39,47]
            multirowheader = [6,7,42,43,46,47]
            third_row = ['First name/Middle name/Surname','DD-MMM-YYYY','in days','in hours','DD-MMM-YYYY','DD-MMM-YYYY']

            first_columns = ['PartnerName','CentreID','Center name','Centre address','Unique trainee ID','Salutation','Name of trainee',
            'Date of birth','Gender','Marital status','Religion','Caste category','Highest education level','Currently pursuing full-time education',
            'Technical education','Guardian type','Name of parent/ spouse/guardian','Guardian contact number','No. of family members in current household',
            'Family economic status (Ration Card)','Major source of household income','Trainee annual income before joining course','Annual household income',
            'Type of identification','Aadhar number','PAN number','Voter ID number','Trainee mobile number','Trainee alternate number','Trainee email ID','Trainee address',
            'District','State','PIN code','Type of disability','PWD certificate','Mobilisation technique','Pre-joining counselling','Pre-training job experience',
            'Trainee current employment status','Course name','Sector','Course duration','Course duration','Skill instructor/Trainer name',
            'Batch code','Batch start date','Batch end date']
            df.to_excel(writer, index=None, header=None, startrow=3 ,sheet_name='Trainee(Candidate)Detail')
            worksheet = writer.sheets['Trainee(Candidate)Detail']

            j=0
            for i in range(len(header)):
                worksheet.merge_range(0, j, 0, header_size[i], header[i], header_format)
                j=header_size[i]+1
            j=0
            for col_num, value in enumerate(first_columns):
                if col_num not in multirowheader:
                    worksheet.merge_range(1, col_num, 2, col_num, value, second_header_format)
                else:
                    worksheet.write(1, col_num, value, second_header_format)
                    worksheet.write(2, col_num, third_row[j], light_header_format)
                    j+=1
            
        def trainee_assesment_fxn():
            cnxn=pyodbc.connect(conn_str)
            curs = cnxn.cursor()
            sql = 'exec [reports].sp_sl4_trainee_assesment_report ?, ?, ?, ?, ?,?,?'
            values = (from_date, to_date, Customers,projects,sub_projects, user_id, user_role_id)
            curs.execute(sql,(values))
            data = curs.fetchall()
            data = list(map(lambda x:list(x), data))
            df = pd.DataFrame(data)

            header = ['Course details','Training process','Training output']
            header_size = [13,19,27]
            multirowheader = [8,9,12,13,23,25]
            third_row = ['in days','in hours','DD-MMM-YYYY','DD-MMM-YYYY','DD-MMM-YYYY','DD-MMM-YYYY']

            first_columns=['Partner name','Center ID','Center name','Unique trainee ID','Name of trainee','Gender','Course name','Sector','Course duration','Course duration',
            'Skill instructor/ Trainer name','Batch code','Batch start date','Batch end date','Number of hours Trade related classroom training completed','Number of hours of lab based training completed',
            'Number of hours of life skill training completed','Industry visit attended','OJT attended','Guest lecture attended','Training status','Attendance (%)','Final assessment conducted',
            'Date of course passing','Certified','Date of issuance of certificate','Certificate name or award','Grade/%/Pass/Fail','Incentive/Stipend provided','If yes, Amount provided']
            df.to_excel(writer, index=None, header=None, startrow=1 ,sheet_name='Training Detail')

            worksheet = writer.sheets['Training Detail']
            
            for i in [0,1,2,3,4,5,28,29]:
                worksheet.merge_range(0, i, 2, i, first_columns[i], second_header_format)

            j=6
            for i in range(len(header)):
                worksheet.merge_range(0, j, 0, header_size[i], header[i], header_format)
                j=header_size[i]+1
            
            j=0
            for i in range(6,28):
                if i not in multirowheader:
                    worksheet.merge_range(1, i, 2, i, first_columns[i], second_header_format)
                else:
                    worksheet.write(1, i, first_columns[i], second_header_format)
                    worksheet.write(2, i, third_row[j], light_header_format)
                    j+=1
            
        def trainee_placemnet_fxn():
            cnxn=pyodbc.connect(conn_str)
            curs = cnxn.cursor()
            sql = 'exec [reports].sp_sl4_trainee_placement_report ?, ?, ?, ?, ?,?,?'
            values = (from_date, to_date, Customers,projects,sub_projects, user_id, user_role_id)
            curs.execute(sql,(values))
            data = curs.fetchall()
            data = list(map(lambda x:list(x), data))
            df = pd.DataFrame(data)

            header = ['Placement Details','Post-placement Tracking 3 months','Post-placement Tracking 6 months']
            header_size = [22,35,48]
            multirowheader = [12,21,24,33,37,46]
            third_row = ['DD-MMM-YYYY','INR','DD-MMM-YYYY','INR','DD-MMM-YYYY','INR']

            first_columns=['Partner Name','Center ID','Center name','Unique trainee ID','Name of trainee','Gender','Course name','Sector','Batch code','Training status','Pre-placement counselling completion','Placement status',
            'Date of placement DD-MMM-YYYY','Placement sector/ Trade','Employment method','Employer name/Self-employed','Name of point person from the company/employer','Contact no. of point person',
            'Employer email ID','Location of employment','Designation of trainee','Monthly Salary (INR)','Annual Salary (WE)/Earning (SE)','Status after 3 months','Tracking date (DD/MM/YYYY)',
            'Second placement offered','If unemployed, reason','Second employment method','Employer name/Self-employed','Name of point person from the company/employer','Contact no. of point person',
            'Employer contact email ID','Location of employment','Monthly Salary (INR)','Annual Salary (WE)/Earning (SE)','Trainee updated contact number','Status after 6 months','Tracking date (DD/MM/YYYY)',
            'Third placement offered','If unemployed,  reason','Method of employment','Employer name/Self-employed','Name of point person from the company/employer','Contact no. of point person',
            'Employer contact email ID','Location of employment','Monthly Salary (INR)','Annual Salary (WE)/Earning (SE)','Trainee updated contact number']
            df.to_excel(writer, index=None, header=None, startrow=1 ,sheet_name='Placement Detail')

            worksheet = writer.sheets['Placement Detail']
            for i in range(10):
                worksheet.merge_range(0, i, 2, i, first_columns[i], second_header_format)

            j=10
            for i in range(len(header)):
                worksheet.merge_range(0, j, 0, header_size[i], header[i], header_format)
                j=header_size[i]+1
            
            j=0
            for i in range(10,len(first_columns)):
                if i not in multirowheader:
                    worksheet.merge_range(1, i, 2, i, first_columns[i], second_header_format)
                else:
                    worksheet.write(1, i, first_columns[i], second_header_format)
                    worksheet.write(2, i, third_row[j], light_header_format)
                    j+=1


        def trainee_dell_tracker_fxn():
            cnxn=pyodbc.connect(conn_str)
            curs = cnxn.cursor()
            sql = 'exec [reports].sp_dell_tracker_report ?, ?, ?, ?, ?,?,?'
            values = (from_date, to_date, Customers,projects,sub_projects, user_id, user_role_id)
            curs.execute(sql,(values))
            columns = [column[0].title() for column in curs.description]
            data = curs.fetchall()
            data = list(map(lambda x:list(x), data))
            df = pd.DataFrame(data, columns=columns)
            df.fillna('')
            column  = ['Sub_Project_Name', 'Cer_Target', 'Cer_Actual', 'Candidate_Data_0_1', 'Candidate_Data_2', 'Candidate_Data_3', 'Candidate_Data_4', 'Total_Assesment', 'Total_Present', 'Total_Certified']
            df = df[column]
            header = ['Sub Project', 'Certification_Target', 'Course Assigned on LMS', '0% Course Completion', '(1%-30%) Course Completion', '50% Course Completion', '100% Course Completion', 'Final Assessment Scheduled', 'Present', 'Pass']

            df.to_excel(writer, index=None, header=None, startrow=1 ,sheet_name='Summary')

            worksheet = writer.sheets['Summary']
            for col_num, value in enumerate(header):
                worksheet.write(0, col_num, value, header_format)
        
        def trainee_dell_tracker2_fxn():
            cnxn=pyodbc.connect(conn_str)
            curs = cnxn.cursor()
            sql = 'exec [reports].sp_dell_tracker2_report ?, ?, ?, ?, ?,?,?'
            values = (from_date, to_date, Customers,projects,sub_projects, user_id, user_role_id)
            curs.execute(sql,(values))
            columns = [column[0].title() for column in curs.description]
            data = curs.fetchall()
            data = list(map(lambda x:list(x), data))
            df = pd.DataFrame(data, columns=columns)
            df = df.fillna('')

            #df.loc[:,'Aadhar_Image_Name'] = df.loc[:,'Aadhar_Image_Name'].map(lambda x: x if (x=='') else '=HYPERLINK("' + config.Base_URL+'/GetDocumentForExcel_S3_certiplate?image_name=' + x + '","View Image")')
            df['Aadhar_First_Side'] = df.loc[:,'Aadhar_Image_Name'].map(lambda x: '' if (x.split(',')[0]=='') else '=HYPERLINK("' + config.Base_URL+'/GetDocumentForExcel_S3_certiplate?image_name=' + x.split(',')[0] +'","View Image")')
            df['Aadhar_Second_Side'] = df.loc[:,'Aadhar_Image_Name'].map(lambda x: '' if len(x.split(','))<=1 else '=HYPERLINK("' + config.Base_URL +'/GetDocumentForExcel_S3_certiplate?image_name=' + x.split(',')[1] +'","View Image")')
            df.loc[:,'Candidate_Photo'] = df.loc[:,'Candidate_Photo'].map(lambda x: x if (x=='') else '=HYPERLINK("' + config.Base_URL+'/GetDocumentForExcel_S3_certiplate?image_name=' + x + '","View Image")')
            df.loc[:,'Educational Marksheet'] = df.loc[:,'Educational Marksheet'].map(lambda x: x if (x=='') else '=HYPERLINK("' + config.Base_URL+'/GetDocumentForExcel_S3_certiplate?image_name=' + x + '","View Image")')


            column = ['Created_On', 'Partner_Name', 'Email', 'Name', 'Present_District', 'State_Name', 'Email_Id', 'Date_Of_Birth', 'Age', 'Primary_Contact_No', 'Whatsapp_Number',
            'Educational Marksheet', 'Aadhar_First_Side','Aadhar_Second_Side', 'Candidate_Photo', 'Aadhar_No', 'Course_Name', 'Disability_Status', 'Aspirational District', 'Gender', 'Shiksha_Sync_Status', 
            'Created_On2', 'Course_Duration_Days', 'Actual_Course_Duration_Days', 'Course_Status', 'Total_Activity', 'Completed_Activity', 'Per', 'Last_Logged_In', 'Half_Completion', 
            'Full_Completion', 'Course_End_Date', 'Certification_Status', 'Certificatio_Date', 'Certificate_Status', 'Acknowledge_Received']
            
            df = df[column]

            header = ['Mobilization Date', 'Mobilized BY (LN/NAV)', 'Mobilized By', 'Candidate Name', 'Candidate_District', 'State', 'Email id', 'DOB', 'Age', 'Mobile Number', 'Whatsapp Number', 
            'Educational Mark Sheet', 'Aadhar_First_Side','Aadhar_Second_Side', 'Candidate Image', 'Aadhaar Number', 'Assigned Course', 'PwD Status (Yes/No)', 'Aspirational District', 'Gender', 'Course Assigned Status (LMS)',
            'Course Assigned Date', 'Max Time to complete Course', 'Actual No of days', 'Course Start Status', 'Total No. of sub modules', 'No. of sub modules Completed', '% of Completion', 'Last Login Date', '50 % Course Completed Status',
            'Course Completed Status', 'Course Completion Date', 'Certification Status', 'Certification Date', 'Certificate Status', 'Acknowledge Received']

            df.to_excel(writer, index=None, header=None, startrow=1 ,sheet_name='Daily Tracker Report')

            worksheet = writer.sheets['Daily Tracker Report']
            for col_num, value in enumerate(header):
                worksheet.write(0, col_num, value, header_format)
        
        if sub_projects=='':

            if  set(config.dell_type_customer.split(',')) >= set(Customers.split(',')):
                #print('dell')
                t4 = threading.Thread(target=trainee_dell_tracker_fxn)
                t5 = threading.Thread(target=trainee_dell_tracker2_fxn)

                t4.start()
                t5.start()
                
                t4.join()
                t5.join()
                
            else:
            #print('others')
                t1 = threading.Thread(target=trainee_fxn) 
                t2 = threading.Thread(target=trainee_assesment_fxn)
                t3 = threading.Thread(target=trainee_placemnet_fxn)

                t1.start()
                t2.start()
                t3.start()

                t1.join() 
                t2.join()
                t3.join()
        else:
            if project_type==4:
                t4 = threading.Thread(target=trainee_dell_tracker_fxn)
                t5 = threading.Thread(target=trainee_dell_tracker2_fxn)

                t4.start()
                t5.start()
                
                t4.join()
                t5.join()
            else:
                t1 = threading.Thread(target=trainee_fxn) 
                t2 = threading.Thread(target=trainee_assesment_fxn)
                t3 = threading.Thread(target=trainee_placemnet_fxn)

                t1.start()
                t2.start()
                t3.start()

                t1.join() 
                t2.join()
                t3.join()
        
        writer.save()
        os.chmod(name_withpath, 0o777)
            
        return({'Description':'created excel', 'Status':True, 'filename':report_name})
        
    except Exception as e:
        print('EXCp:'+str(e))
        return({'Description':'Error creating excel', 'Status':False, 'Error':str(e)})
