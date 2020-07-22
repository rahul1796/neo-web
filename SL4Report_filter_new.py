def create_report(from_date, to_date, Customers, user_id, user_role_id, report_name):
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
        import xlsxwriter
        import threading
        from Database import config
    except:
        return({'Description':'Module Error', 'Status':False})

    try:
        conn_str = config.conn_str
        name_withpath = config.neo_report_file_path + 'report file/'+ report_name
        
        writer = pd.ExcelWriter(name_withpath, engine='xlsxwriter')
        workbook  = writer.book

        header_format = workbook.add_format({
            'bold': True,
            'text_wrap': True,
            'valign': 'center',
            'fg_color': '#D7E4BC',
            'border': 1})

        def trainee_fxn():
            cnxn=pyodbc.connect(conn_str)
            curs = cnxn.cursor()
            sql = 'exec [reports].[sp_sl4_trainee_report] ?, ?, ?, ?, ?'
            values = (from_date, to_date, Customers, user_id, user_role_id)
            curs.execute(sql,(values))
            data = curs.fetchall()
            data = list(map(lambda x:list(x), data))
            df = pd.DataFrame(data)
            
            first_columns = ['PartnerName','CentreID','Centre address','Unique trainee ID','Salutation','Name of trainee(First name/Middle name/Surname)',
            'Date of birth	DD-MMM-YYYY','Gender','Marital status','Religion','Caste category','Highest education level','Currently pursuing full-time education',
            'Technical education','Guardian type','Name of parent/ spouse/guardian','Guardian contact number','No. of family members in current household',
            'Family economic status (Ration Card)','Major source of household income','Trainee annual income before joining course','Annual household income',
            'Type of identification','Aadhar number','PAN number','Voter ID number','Trainee mobile number','Trainee alternate number','Trainee email ID','Trainee address',
            'District','State','PIN code','Type of disability','PWD certificate','Mobilisation technique','Pre-joining counselling','Pre-training job experience',
            'Trainee current employment status','Course name','Sector','Course duration(in days)','Course duration(in hours)','Skill instructor/Trainer name',
            'Batch start date DD-MMM-YYYY','Batch end date DD-MMM-YYYY']
            df.to_excel(writer, index=None, header=None, startrow=1 ,sheet_name='Trainee(Candidate)Detail')
            worksheet = writer.sheets['Trainee(Candidate)Detail']
            
            for col_num, value in enumerate(first_columns):
                worksheet.write(0, col_num, value, header_format)
            
        def trainee_assesment_fxn():
            cnxn=pyodbc.connect(conn_str)
            curs = cnxn.cursor()
            sql = 'exec [reports].sp_sl4_trainee_assesment_report ?, ?, ?, ?, ?'
            values = (from_date, to_date, Customers, user_id, user_role_id)
            curs.execute(sql,(values))
            data = curs.fetchall()
            data = list(map(lambda x:list(x), data))
            df = pd.DataFrame(data)
            
            first_columns=['Partner name','Center ID','Unique trainee ID','Name of trainee','Gender','Course name','Sector','Course duration(in days)','Course duration(in hours)',
            'Skill instructor/ Trainer name','Batch start date DD-MMM-YYYY','Batch end date DD-MMM-YYYY','Number of hours Trade related classroom training completed','Number of hours of lab based training completed',
            'Number of hours of life skill training completed','Industry visit attended','OJT attended','Guest lecture attended','Training status','Attendance (%)','Final assessment conducted',
            'Date of course passing (DD-MM-YYYY)','Certified','Date of issuance of certificate (DD-MM-YYYY)','Certificate name or award','Grade/%/Pass/Fail','Incentive/Stipend provided','If yes, Amount provided (INR)']
            df.to_excel(writer, index=None, header=None, startrow=1 ,sheet_name='Training Detail')

            worksheet = writer.sheets['Training Detail']
            for col_num, value in enumerate(first_columns):
                worksheet.write(0, col_num, value, header_format)
            
        def trainee_placemnet_fxn():
            cnxn=pyodbc.connect(conn_str)
            curs = cnxn.cursor()
            sql = 'exec [reports].sp_sl4_trainee_placement_report ?, ?, ?, ?, ?'
            values = (from_date, to_date, Customers, user_id, user_role_id)
            curs.execute(sql,(values))
            data = curs.fetchall()
            data = list(map(lambda x:list(x), data))
            df = pd.DataFrame(data)

            first_columns=['Partner Name','Center ID','Unique trainee ID','Name of trainee','Gender','Course name','Sector','Training status','Pre-placement counselling completion','Placement status',
            'Date of placement DD-MMM-YYYY','Placement sector/ Trade','Employment method','Employer name/Self-employed','Name of point person from the company/employer','Contact no. of point person',
            'Employer email ID','Location of employment','Designation of trainee','Monthly Salary (INR)','Annual Salary (WE)/Earning (SE)','Status after 3 months','Tracking date (DD/MM/YYYY)',
            'Second placement offered','If unemployed, reason','Second employment method','Employer name/Self-employed','Name of point person from the company/employer','Contact no. of point person',
            'Employer contact email ID','Location of employment','Monthly Salary (INR)','Annual Salary (WE)/Earning (SE)','Trainee updated contact number','Status after 6 months','Tracking date (DD/MM/YYYY)',
            'Third placement offered','If unemployed,  reason','Method of employment','Employer name/Self-employed','Name of point person from the company/employer','Contact no. of point person',
            'Employer contact email ID','Location of employment','Monthly Salary (INR)','Annual Salary (WE)/Earning (SE)','Trainee updated contact number']
            df.to_excel(writer, index=None, header=None, startrow=1 ,sheet_name='Placement Detail')

            worksheet = writer.sheets['Placement Detail']
            for col_num, value in enumerate(first_columns):
                worksheet.write(0, col_num, value, header_format)
        
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
        return({'Description':'created excel', 'Status':True, 'filename':report_name})
        
    except Exception as e:
        return({'Description':'Error creating excel', 'Status':False, 'Error':str(e)})
