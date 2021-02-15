def create_report(user_id, user_role_id, customer_ids, contract_ids, region_ids, from_date, to_date,stage_ids,status_id, file_name):
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
        sql = 'exec [reports].[sp_get_ecp_report_data_download] ?, ?,?, ?, ?, ?, ?,?,?'
        values = (user_id, user_role_id, customer_ids, contract_ids, region_ids, from_date, to_date,stage_ids,status_id)
        curs.execute(sql,(values))
        columns = [column[0].title() for column in curs.description]
        data = curs.fetchall()
        data = list(map(lambda x:list(x), data))

        df = pd.DataFrame(data, columns=columns)
        df= df[['Customer_Name','Customer_Status', 'Contract_Name', 'Contract_Code','Contract_Stage_Name', 'Project_Name', 'Sub_Project_Name', 'Region_Name', 'User_Name_Coo', 'User_Name_Tm', 'Target_Enrolment', 'Target_Certification', 'Target_Placement', 'Enrolled', 'Certified', 'Placement', 'Enrolled_Filtered', 'Certified_Filtered', 'Placed_Filtered']]
        
        df.to_excel(writer, index=None, header=None ,startrow=2 ,sheet_name='ECP-Report') 
        worksheet = writer.sheets['ECP-Report']
        stagelog_default_column = ['Customer_Name','Customer_Status', 'Contract_Name', 'Contract_Code','Contract_Stage', 'Project_Name', 'Sub_Project_Name', 'Region_Name', 'COO', 'TM']
        first_row = ['Targets', 'Actuals (Contract Till Date)', 'Actuals']
        second_row = ['Enrolled','Certified','Placement','Enrolled','Certified','Placement','Enrolled','Certified','Placement']
        for col_num, value in enumerate(stagelog_default_column):
            worksheet.merge_range(0, col_num, 1, col_num, value, header_format)
        for col_num, value in enumerate(first_row):
            worksheet.merge_range(0, 8+col_num*3, 0, 10+col_num*3, value, header_format)
        for col_num, value in enumerate(second_row):
            worksheet.write(1, 8+col_num, value, header_format)
        writer.save()
        curs.close()
        cnxn.close()
        return({'Description':'created excel', 'Status':True, 'filename':file_name})
        
    except Exception as e:
        print(str(e))
        curs.close()
        cnxn.close()
        return({'Description':'Error creating excel'+str(e), 'Status':False, 'Error':str(e)})
    ##########################################
