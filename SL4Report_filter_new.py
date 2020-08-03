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
            sql = 'exec [reports].[sp_sl4_trainee_report] ?, ?, ?, ?, ?'
            values = (from_date, to_date, Customers, user_id, user_role_id)
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
            sql = 'exec [reports].sp_sl4_trainee_assesment_report ?, ?, ?, ?, ?'
            values = (from_date, to_date, Customers, user_id, user_role_id)
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
            sql = 'exec [reports].sp_sl4_trainee_placement_report ?, ?, ?, ?, ?'
            values = (from_date, to_date, Customers, user_id, user_role_id)
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
