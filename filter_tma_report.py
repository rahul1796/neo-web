def create_report(start_date, end_date, customername, centername, coursename, name):
    '''from datetime import datetime
    start_time = datetime.now()
    
        start_date = '2019-11-01'
        end_date = '2019-12-30'
        coursename=''
        centername=''
        customername=''
    ##########################################
    '''
    try:
        import pandas as pd
        import pypyodbc as pyodbc
        import xlsxwriter
        import threading
        from Database import config
    except:
        return({'Description':'Module Error', 'Status':False})

    try:
        base_url = 'http://neolive.southindia.cloudapp.azure.com:27072/'
        log_image = 'data/log_images/'
        attendance_image = 'data/attendance_images/'
        attendance_url = base_url + attendance_image
        log_url = base_url + log_image
        conn_str = config.conn_str

        name_withpath = config.neo_report_file_path + name
        
        writer = pd.ExcelWriter(name_withpath, engine='xlsxwriter')
        workbook  = writer.book

        header_format = workbook.add_format({
            'bold': True,
            'text_wrap': True,
            'valign': 'center',
            'fg_color': '#D7E4BC',
            'border': 1})


        def stage_log_fxn():
            stagelog_default_column = ['LOG DATE', 'TRAINER NAME', 'TRAINER EMAIL',  'BATCH CODE', 'BATCH START DATE',
                          'BATCH END DATE', 'CUSTOMER NAME', 'CENTER NAME', 'CENTER TYPE', 'DISTRICT', 'STATE' , 'REGION',
                          'BUSSINESS UNIT', 'COURSE CODE', 'COURSE NAME', 'SESSION NAME']
            second_row = ['LOG DATE TIME', 'LOG IMAGE', 'LOG LOCATION', 'LOG DATE TIME', 'LOG IMAGE', 'LOG LOCATION',
                      'LOG DATE TIME', 'LOG IMAGE', 'LOG LOCATION', 'LOG DATE TIME', 'LOG IMAGE', 'LOG LOCATION']
            first_row = ['SESSION START', 'ONGOING SESSION', 'MARK ATTENDANCE', 'SESSION COMPLETED']

            cnxn=pyodbc.connect(conn_str)
            curs = cnxn.cursor()
            sql = 'exec [masters].[sp_stagelog_tmareport] ?, ?, ?, ?, ?'
            values = (start_date, end_date, customername, centername, coursename)
            curs.execute(sql,(values))
            
            data = curs.fetchall()
            data = list(map(lambda x:list(x), data))
            df = pd.DataFrame(data)
            df.iloc[:,17] = df.iloc[:,17].map(lambda x: x if ((x=='NR') or (x=='NA')) else '=HYPERLINK("' + log_url + x + '","View Image")')
            df.iloc[:,18] = df.iloc[:,18].map(lambda x: x if ((x=='NR') or (x=='NA')) else '=HYPERLINK("' + x + '","View Location")')
            df.iloc[:,20] = df.iloc[:,20].map(lambda x: x if ((x=='NR') or (x=='NA')) else '=HYPERLINK("' + log_url + x + '","View Image")')
            df.iloc[:,21] = df.iloc[:,21].map(lambda x: x if ((x=='NR') or (x=='NA')) else '=HYPERLINK("' + x + '","View Location")')
            df.iloc[:,23] = df.iloc[:,23].map(lambda x: x if ((x=='NR') or (x=='NA')) else '=HYPERLINK("' + log_url + x + '","View Image")')
            df.iloc[:,24] = df.iloc[:,24].map(lambda x: x if ((x=='NR') or (x=='NA')) else '=HYPERLINK("' + x + '","View Location")')
            df.iloc[:,26] = df.iloc[:,26].map(lambda x: x if ((x=='NR') or (x=='NA')) else '=HYPERLINK("' + log_url + x + '","View Image")')
            df.iloc[:,27] = df.iloc[:,27].map(lambda x: x if ((x=='NR') or (x=='NA')) else '=HYPERLINK("' + x + '","View Location")')
            #17,18,20,21

            
            df.to_excel(writer, index=None, header=None, startrow=2 ,sheet_name='Stage-Log')

            worksheet = writer.sheets['Stage-Log']
            for col_num, value in enumerate(stagelog_default_column):
                worksheet.merge_range(0, col_num, 1, col_num, value, header_format)

            # Write the column headers with the defined format.
            for col_num, value in enumerate(second_row):
                worksheet.write(1, 16+col_num, value, header_format)

            for col_num, value in enumerate(first_row):
                worksheet.merge_range(0, 16+col_num*3, 0, 18+col_num*3, value, header_format)

            
        def group_images_fxn():
            groupimage_default_column = ['LOG DATE', 'TRAINER NAME', 'TRAINER EMAIL', 'BATCH CODE', 'BATCH START DATE',
                                     'BATCH END DATE', 'CUSTOMER NAME', 'CENTER NAME', 'CENTER TYPE', 'DISTRICT', 'STATE' , 'REGION', 'BUSSINESS UNIT',
                                     'COURSE CODE', 'COURSE NAME', 'SESSION NAME', 'SESSION GROUP IMAGE', 'REMARKS']

            cnxn=pyodbc.connect(conn_str)
            curs = cnxn.cursor()
            sql = 'exec [masters].[sp_groupimage_tmareport] ?, ?, ?, ?, ?'
            values = (start_date, end_date, customername, centername, coursename)
            curs.execute(sql,(values))
            
            data = curs.fetchall()
            data = list(map(lambda x:list(x), data))
            df = pd.DataFrame(data)
            df.columns = groupimage_default_column
            df['SESSION GROUP IMAGE'] = df.loc[:,'SESSION GROUP IMAGE'].map(lambda x: x if ((x=='NR') or (x=='NA')) else '=HYPERLINK("' + attendance_url + x + '","View Image")')
            
            df.to_excel(writer, index=None, header=None, startrow=1 ,sheet_name='Session-Group-Images')

            worksheet = writer.sheets['Session-Group-Images']
            for col_num, value in enumerate(groupimage_default_column):
                worksheet.write(0, col_num, value, header_format)
            

            
        def candidate_attendance_fxn():
            attendance_default_column = ['ATTENDANCE DATE', 'TRAINER NAME', 'TRAINER EMAIL', 'BATCH CODE', 'BATCH START DATE',
                          'BATCH END DATE', 'CUSTOMER NAME', 'CENTER NAME', 'CENTER TYPE', 'DISTRICT', 'STATE' , 'REGION', 'BUSSINESS UNIT',
                          'COURSE CODE', 'COURSE NAME', 'SESSION NAME', 'CANDIDATE NAME', 'ENROLLMENT ID', 'ATTENDANCE',
                          'ATTENDANCE IMAGE']
            
            cnxn=pyodbc.connect(conn_str)
            curs = cnxn.cursor()
            sql = 'exec [masters].[sp_candidate_tmareport] ?, ?, ?, ?, ?'
            values = (start_date, end_date, customername, centername, coursename)
            curs.execute(sql,(values))
            
            data = curs.fetchall()
            data = list(map(lambda x:list(x), data))
            df = pd.DataFrame(data)
            df.columns = attendance_default_column
            df['ATTENDANCE IMAGE'] = df.loc[:,'ATTENDANCE IMAGE'].map(lambda x: x if ((x=='NR') or (x=='NA')) else '=HYPERLINK("' + attendance_url + x + '","View Image")')

            
            df.to_excel(writer, index=None, header=None, startrow=1 ,sheet_name='Candidate-Attendance')

            worksheet = writer.sheets['Candidate-Attendance']
            for col_num, value in enumerate(attendance_default_column):
                worksheet.write(0, col_num, value, header_format)
            

            

        t1 = threading.Thread(target=stage_log_fxn) 
        t2 = threading.Thread(target=group_images_fxn)
        t3 = threading.Thread(target=candidate_attendance_fxn)

        t1.start()
        t2.start()
        t3.start()

        t1.join() 
        t2.join()
        t3.join()              
                        
        writer.save()
        
        return({'Description':'created excel', 'Status':True, 'filename':name})
        
    except Exception as e:
        return({'Description':'Error creating excel', 'Status':False, 'Error':str(e)})
    ##########################################
    
