def create_report(candidate_id, user_id, user_role_id, status, customer, project, sub_project, region, center, center_type, file_name):
    '''from datetime import datetime
    start_time = datetime.now()
    
        start_date = '2019-11-01'
        end_date = '2019-12-30'
        coursename=''
        centername=''
        customername=''
    ##########################################
    conn_str = (
            r'Driver={SQL Server};'
            r'Server=LNJAGDISH;'
            r'Database=NEO_APR_1;'    #  NEO_MAR_31  NEO_MAR_15  #MCLG_LIVE_MAR03
            r'Trusted_Connection=yes;'
            )
    '''
    
    try:
        import pandas as pd
        import pypyodbc as pyodbc
        import xlsxwriter
        from Database import config
    except:
        return({'Description':'Module Error', 'Status':False})

    try:
        name_withpath = config.neo_report_file_path + file_name
        
        writer = pd.ExcelWriter(name_withpath, engine='xlsxwriter')
        workbook  = writer.book

        header_format = workbook.add_format({
            'bold': True,
            #'text_wrap': True,
            'valign': 'center',
            'fg_color': '#D7E4BC',
            'border': 1})

        cnxn=pyodbc.connect(config.conn_str) #
        curs = cnxn.cursor()
        sql = 'exec [candidate_details].[sp_get_candidate_download_list_new] ?, ?, ?, ?, ?, ?, ?, ?, ?, ?'
        values = (candidate_id, customer, project, sub_project, region, center, center_type, status, user_id, user_role_id)
        curs.execute(sql,(values))

        columns = [column[0].title() for column in curs.description] 
        data = curs.fetchall()
        data = list(map(lambda x:list(x), data))
        #print(len(data))
        df = pd.DataFrame(data)
        df.to_excel(writer, index=None, header=None ,startrow=1 ,sheet_name='Candidate-data') 

        worksheet = writer.sheets['Candidate-data']

        for col_num, value in enumerate(columns):
            worksheet.write(0, col_num, value, header_format)

                        
        writer.save()
        curs.close()
        cnxn.close()
        return({'Description':'created excel', 'Status':True, 'filename':file_name})
        
    except Exception as e:
        curs.close()
        cnxn.close()
        return({'Description':'Error creating excel'+str(e), 'Status':False, 'Error':str(e)})
    ##########################################
    
