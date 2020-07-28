def create_report(month, Customers, user_id, user_role_id, report_name):
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
            'bold': True,
            'text_wrap': True,
            'valign': 'center',
            'fg_color': '#74dc96',
            'border': 1})

        def national_batch_fxn():
            cnxn=pyodbc.connect(conn_str)
            curs = cnxn.cursor()
            sql = 'exec [reports].[sp_national_new_batch] ?, ?, ?, ?'
            values = (month, Customers, user_id, user_role_id)
            curs.execute(sql,(values))
            data = curs.fetchall()
            data = list(map(lambda x:list(x), data))
            df = pd.DataFrame(data)

            header = ['Enrolment Batch','Enrolment Nos','Certification Batch','Certification Nos']	
            header_size = [4,7,10,13]
            
            first_columns = ['vertical','Region','Target','Actual','% Achieved','Target','Actual','% Achieved','Target','Actual','% Achieved','Target','Actual','% Achieved']

            df.to_excel(writer, index=None, header=None, startrow=2 ,sheet_name='New Batch')
            worksheet = writer.sheets['New Batch']

            j=2
            for i in range(len(header)):
                worksheet.merge_range(0, j, 0, header_size[i], header[i], header_format)
                j=header_size[i]+1
            
            for col_num, value in enumerate(first_columns):
                if col_num in [0,1]:
                    worksheet.merge_range(0, col_num, 1, col_num, value, second_header_format)
                else:
                    worksheet.write(1, col_num, value, light_header_format)
                    
            
        def national_projectwise_fxn():
            cnxn=pyodbc.connect(conn_str)
            curs = cnxn.cursor()
            sql = 'exec [reports].[sp_national_projectwise] ?, ?, ?, ?'
            values = (month, Customers, user_id, user_role_id)
            curs.execute(sql,(values))
            data = curs.fetchall()
            data = list(map(lambda x:list(x), data))
            df = pd.DataFrame(data)

            header_1 = ['Contract']
            header = ['Enrolment','Certification','Placement','Revenue']
            second_line = ['Target','Actuals','Target','Actuals','Target','Actuals','Target','Actuals']
            secondlinecol = [5,11,16,22,27,33,38,44]
            third_line = ['w1','w2','w3','w4','total','w1','w2','w3','w4','total','% Achieved','w1','w2','w3','w4','total','w1','w2','w3','w4','total','% Achieved','w1','w2','w3','w4','total','w1','w2','w3','w4','total','% Achieved','w1','w2','w3','w4','total','w1','w2','w3','w4','total','% Achieved']

            df.to_excel(writer, index=None, header=None, startrow=3 ,sheet_name='National Projectwise')

            worksheet = writer.sheets['National Projectwise']

            for col_num, value in enumerate(header_1):
                worksheet.merge_range(0, col_num, 2, col_num, value, header_format)
            
            for col_num, value in enumerate(header):
                worksheet.merge_range(0, 11*col_num+1, 0, 11*(col_num+1), value, header_format)
            
            j=1
            for col_num, value in enumerate(second_line):
                worksheet.merge_range(1, j, 1, secondlinecol[col_num], second_line[col_num], second_header_format)
                j=secondlinecol[col_num]+1
            
            for col_num, value in enumerate(third_line):
                worksheet.write(2, col_num+1, value, light_header_format)

            
        def national_regionwise_contract_fxn():
            cnxn=pyodbc.connect(conn_str)
            curs = cnxn.cursor()
            sql = 'exec [reports].[sp_national_regionwise_contract] ?, ?, ?, ?'
            values = (month, Customers, user_id, user_role_id)
            curs.execute(sql,(values))
            data = curs.fetchall()
            data = list(map(lambda x:list(x), data))
            df = pd.DataFrame(data)

            header_1 = ['Region','Contract','Vertical']
            header = ['Enrolment','Certification','Placement','Revenue']
            second_line = ['Target','Actuals','Target','Actuals','Target','Actuals','Target','Actuals']
            secondlinecol = [7,13,18,24,29,35,40,46]
            third_line = ['w1','w2','w3','w4','total','w1','w2','w3','w4','total','% Achieved','w1','w2','w3','w4','total','w1','w2','w3','w4','total','% Achieved','w1','w2','w3','w4','total','w1','w2','w3','w4','total','% Achieved','w1','w2','w3','w4','total','w1','w2','w3','w4','total','% Achieved']

            df.to_excel(writer, index=None, header=None, startrow=3 ,sheet_name='National Regionwise Contract')

            worksheet = writer.sheets['National Regionwise Contract']

            for col_num, value in enumerate(header_1):
                worksheet.merge_range(0, col_num, 2, col_num, value, header_format)
            
            for col_num, value in enumerate(header):
                worksheet.merge_range(0, 11*col_num+3, 0, 11*(col_num+1)+2, value, header_format)
            
            j=3
            for col_num, value in enumerate(second_line):
                worksheet.merge_range(1, j, 1, secondlinecol[col_num], second_line[col_num], second_header_format)
                j=secondlinecol[col_num]+1
            
            for col_num, value in enumerate(third_line):
                worksheet.write(2, col_num+3, value, light_header_format)
        
        t1 = threading.Thread(target=national_batch_fxn) 
        t2 = threading.Thread(target=national_projectwise_fxn)
        t3 = threading.Thread(target=national_regionwise_contract_fxn)

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
