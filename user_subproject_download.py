def create_report(sub_project,project,region,customer,user_id,user_role_id,employee_status,sub_project_status,file_name):
    try:
        import pandas as pd
        import pypyodbc as pyodbc
        import xlsxwriter,os
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
        sql = 'exec [reports].[sp_get_user_sub_project_report_download] ?, ?, ?, ?, ?, ?, ?, ?'
        values = (customer,project,sub_project,region,user_id,user_role_id,employee_status,sub_project_status)
        curs.execute(sql,(values))
        
        columns = [column[0].title() for column in curs.description]
        data = curs.fetchall()
        data = list(map(lambda x:list(x), data))
        df = pd.DataFrame(data, columns=columns)
        df= df[['Employee_Code', 'Employee_Name','Employee_Email','Sub_Project_Code', 'Sub_Project_Name', 'Employee_Neo_Role', 'Employement_Type']]
        
        df.to_excel(writer, index=None, header=None ,startrow=1 ,sheet_name='user-subproject Report') 
        worksheet = writer.sheets['user-subproject Report']
        Column = ['Employee_Code', 'Employee_Name','Employee_Email','Sub_Project_Code', 'Sub_Project_Name', 'Employee_Neo_Role', 'Employement_Type']
        for col_num, value in enumerate(Column):
            worksheet.write(0, col_num, value, header_format)                 
        writer.save()
        os.chmod(name_withpath, 0o777)
        curs.close()
        cnxn.close()
        return({'Description':'created excel', 'Status':True, 'filename':file_name})
        
    except Exception as e:
        curs.close()
        cnxn.close()
        print(str(e))
        return({'Description':'Error creating excel'+str(e), 'Status':False, 'Error':str(e)})
    ##########################################
