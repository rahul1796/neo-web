def create_report(batch_id, user_id, user_role_id, status, customer, project, sub_project, region, center, center_type,BU,BatchCodes, Planned_actual, StartFromDate, StartToDate, EndFromDate, EndToDate, file_name):
    # from candidate report 
    try:
        import pandas as pd
        import pypyodbc as pyodbc
        import xlsxwriter
        from Database import config
    except:
        return({'Description':'Module Error', 'Status':False})

    try:
        name_withpath = config.neo_report_file_path + 'report file/'+ file_name
        
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
        sql = 'exec [batches].[sp_get_batch_list_updatd] ?, ?, ?, ?, ?, ?, ?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?, ?, ?, ?, ?, ?'

        values = (batch_id,0,1000000,'','','',user_id,user_role_id, status, customer, project, sub_project, region, center, center_type, BU,'',BatchCodes, Planned_actual, StartFromDate, StartToDate, EndFromDate, EndToDate) #
        curs.execute(sql,(values))
        columns = [column[0].title() for column in curs.description]
        
        data = curs.fetchall()
        data = list(map(lambda x:list(x), data))
        #print(len(data))
        df = pd.DataFrame(data, columns=columns)
        df = df.fillna('')
        df.loc[:,'Center_Manager_Email'] = df.loc[:,'Center_Manager_Email'].map(lambda x: x if ((x=='NR') or (x=='NA') or (x=='')) else (','.join(set(x.split(',')))))
        df = df[['Batch_Id','Batch_Name','Batch_Code','Planned_Batch_Code','Candidate_Count','Product_Name','Center_Name',
        'Center_Location','Center_State','Ojt_Start_Date','Ojt_End_Date','Course_Name','Customer_Name',
        'Contract_Name','Project_Name','Sub_Project_Name','Trainer_Email', 'Center_Manager_Email', 'Start_Date', 'End_Date','Status',
        'Assessment_Date','Result_Uploaded_Date']]
        columns = ['Batch_Id','Batch_External_Code','Batch_Code','Planned_Batch_Code','Candidate_Count','Product_Name','Center_Name',
        'Center_Location','Center_State','OJT_Start_Date','OJT_End_Date','Course_Name','Customer_Name',
        'Contract_Name','Project_Name','Sub_Project_Name','Trainer_Email', 'CM/PC Email', 'Start_Date', 'End_Date','Status',
        'Assessment_Date','Result_Uploaded_Date']
        df.to_excel(writer, index=None, header=None ,startrow=1 ,sheet_name='Batch_Report') 

        worksheet = writer.sheets['Batch_Report']

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
