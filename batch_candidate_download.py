def create_report(batch_id, file_name):
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
        sql = 'exec [masters].[sp_Getcandidatebybatch] ?'
        values = (batch_id,)
        
        curs.execute(sql,(values))
        columns = [column[0].title() for column in curs.description]
        data = curs.fetchall()
        data = list(map(lambda x:list(x), data))

        df = pd.DataFrame(data, columns=columns)
        df= df[['Batch_Name', 'Course_Name','Center_Name','Intervention_Value', 'Candidate_Name', 'Date_Of_Birth', 'Gender', 'Mobile_Number', 'Email_Id', 'Father_Name', 'Annual_Income']]
        
        df.to_excel(writer, index=None, header=None ,startrow=1 ,sheet_name='candidate-Report') 
        worksheet = writer.sheets['candidate-Report']
        Column = ['Batch External Code', 'Course Name','Center Name','Enrollment Number', 'Candidate Name', 'Date Of Birth', 'Gender', 'Mobile Number', 'Email Id', 'Father Name', 'Annual Income']
        for col_num, value in enumerate(Column):
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
