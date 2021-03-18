def create_report(sub_project,project,region,customer,user_id,user_role_id,employee_status,sub_project_status,month,year, status_id,file_name):
    try:
        import pandas as pd
        import pypyodbc as pyodbc
        import xlsxwriter,re,os
        from datetime import datetime
        from Database import config
    except:
        return({'Description':'Module Error', 'Status':False})
    try:
        mon= -1 if pd.isna(month) else month
        yyyy= -1 if pd.isna(year) else year
        DownloadPath=config.neo_report_file_path+'report file/'
        report_name = 'User_SubProject_Report_'+datetime.now().strftime('%Y_%m_%d_%H_%M_%S')+".xlsx"  
        name_withpath = config.neo_report_file_path + 'report file/'+ report_name
        path = '{}{}'.format(DownloadPath,report_name)
            
        r=re.compile('User_SubProject_Report_.*')
        lst=os.listdir(DownloadPath)
        newlist = list(filter(r.match, lst))
        for i in newlist:
            os.remove( DownloadPath + i)
        
        writer = pd.ExcelWriter(name_withpath, engine='xlsxwriter')
        workbook  = writer.book
        header_format = workbook.add_format({
            'bold': True,
            #'text_wrap': True,
            'valign': 'center',
            'align' : 'left',                
            'fg_color': '#D7E4BC',
            'border': 1})

        cnxn=pyodbc.connect(config.conn_str) #
        curs = cnxn.cursor()
        sql = 'exec [reports].[sp_get_user_sub_project_report_download] ?, ?, ?, ?, ?, ?, ?, ?, ?'
        values = (customer,project,sub_project,region,user_id,user_role_id,employee_status,sub_project_status, status_id)
        #print(values)
        curs.execute(sql,(values))
        
        columns = [column[0].title() for column in curs.description]
        data = curs.fetchall()
        data = list(map(lambda x:list(x), data))
        df = pd.DataFrame(data, columns=columns)
        df= df[['Employee_Code', 'Employee_Name','Employee_Email','Sub_Project_Code', 'Sub_Project_Name', 'Employee_Neo_Role', 'Employement_Type','Region']]
        
        df.to_excel(writer, index=None, header=None ,startrow=1 ,sheet_name='User-SubProject') 
        worksheet = writer.sheets['User-SubProject']
        Column = ['Employee_Code', 'Employee_Name','Employee_Email','Sub_Project_Code', 'Sub_Project_Name', 'Employee_Neo_Role', 'Employement_Type','Region']
        for col_num, value in enumerate(Column):
            worksheet.write(0, col_num, value, header_format)

        sql = 'exec [reports].[sp_get_user_sub_project__weekwise_allocation_download] ?, ?, ?, ?, ?, ?, ?, ?, ?,?,?'
        values = (customer,project,sub_project,region,user_id,user_role_id,employee_status,sub_project_status, status_id,mon,yyyy)
        #print(values)
        
        curs.execute(sql,(values))
        
        columns = [column[0].title() for column in curs.description]
        data = curs.fetchall()
        data = list(map(lambda x:list(x), data))
        df = pd.DataFrame(data, columns=columns)
        df= df[['Employee_Code', 'Employee_Name','Employee_Email','Sub_Project_Code', 'Sub_Project_Name','Region','Month_Year','W1_Allocation_Percentage', 'W2_Allocation_Percentage','W3_Allocation_Percentage','W4_Allocation_Percentage', 'W1_Allocation', 'W2_Allocation','W3_Allocation','W4_Allocation']]
        
        df.to_excel(writer, index=None, header=None ,startrow=1 ,sheet_name='Allocation') 
        worksheet = writer.sheets['Allocation']
        Column = ['Employee_Code', 'Employee_Name','Employee_Email','Sub_Project_Code', 'Sub_Project_Name','Region','Month_Year', 'W1_Allocation_Percentage', 'W2_Allocation_Percentage','W3_Allocation_Percentage','W4_Allocation_Percentage', 'W1_Allocation(hours)', 'W2_Allocation(hours)','W3_Allocation(hours)','W4_Allocation(hours)']
        for col_num, value in enumerate(Column):
            worksheet.write(0, col_num, value, header_format)     
                    
        writer.save()
        os.chmod(name_withpath, 0o777)
        curs.close()
        cnxn.close()
        return {"success":True,"msg":"Report Created.",'FileName':report_name,'FilePath':config.neo_report_file_path_web}
           
        
    except Exception as e:
        curs.close()
        cnxn.close()
        print(str(e))
        return({'Description':'Error creating excel'+str(e), 'Status':False, 'Error':str(e)})
    ##########################################
