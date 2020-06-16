def create_report(user_id, user_role_id, Role, Date, file_name):
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
        sql = 'exec [reports].[sp_get_mobilization_report_data] ?, ?, ?, ?'
        values = (user_id, user_role_id, Role, Date)
        
        curs.execute(sql,(values))
        columns = [column[0].title() for column in curs.description]
        
        data = curs.fetchall()
        data = list(map(lambda x:list(x), data))

        df = pd.DataFrame(data, columns=columns)
        #print(columns)
        df= df[['User_Name', 'User_Role_Name', 'Product', 'Conversion_Criteria', 'U_M_Target', 'E_M_Count', 'Mper', 'P_M_Target', 'E_M_Count', 'Mpper',
        'U_Q_Target', 'E_Q_Count', 'Qper', 'P_Q_Target', 'E_Q_Count', 'Qpper', 'U_Y_Target', 'E_Y_Count', 'Yper', 'P_Y_Target', 'E_Y_Count', 'Ypper']]

        df.to_excel(writer, index=None, header=None ,startrow=3 ,sheet_name='Mobilizer-Report') 
        worksheet = writer.sheets['Mobilizer-Report']
        
        default_column = ['Mobilizer', 'Role', 'Product', 'Conversion Criteria']
        first_row = ['MTD', 'QTD', 'YTD']
        second_row = ['Mobilization', 'Conversion', 'Mobilization', 'Conversion', 'Mobilization', 'Conversion']
        third_row = ['Target', 'Actuals', '%', 'Projects mandate', 'Actuals', '%','Target', 'Actuals', '%',
                    'Projects mandate', 'Actuals', '%','Target', 'Actuals', '%', 'Projects mandate', 'Actuals', '%']
        for col_num, value in enumerate(default_column):
            worksheet.merge_range(0, col_num, 2, col_num, value, header_format)
        for col_num, value in enumerate(first_row):
            worksheet.merge_range(0, 4+col_num*6, 0, 9+col_num*6, value, header_format)
        for col_num, value in enumerate(second_row):
            worksheet.merge_range(1, 4+col_num*3, 1, 6+col_num*3, value, header_format)
        for col_num, value in enumerate(third_row):
            worksheet.write(2, 4+col_num, value, header_format)
                
        writer.save()
        curs.close()
        cnxn.close()
        return({'Description':'created excel', 'Status':True, 'filename':file_name})
        
    except Exception as e:
        curs.close()
        cnxn.close()
        return({'Description':'Error creating excel'+str(e), 'Status':False, 'Error':str(e)})
    ##########################################
