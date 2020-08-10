def create_report(user_id, user_role_id, region_ids, t_status, trainer_ids, from_date, to_date, report_name):
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

        def trainer_productivity_region():
            cnxn=pyodbc.connect(conn_str)
            curs = cnxn.cursor()
            sql = 'exec [reports].[sp_trainer_productivity_report_region] ?, ?, ?, ?, ?, ?, ?'
            values = (user_id, user_role_id, region_ids, t_status, trainer_ids, from_date, to_date)
            curs.execute(sql,(values))
            data = curs.fetchall()
            data = list(map(lambda x:list(x), data))
            df = pd.DataFrame(data)

            first_column = ['Trainer Name','Region','No of On going Batches','On going Training (Enrol)','Nos Attendance %','Hour Attendance %','Drop Out %','Certified Target','Certified Actual','Passed %','Placed %','Certified Target','Certified Actual','Passed %','Placed %','Certified Target','Certified Actual','Passed %','Placed %']
            header = ['MTD','QTD','YTD']
            
            df.to_excel(writer, index=None, header=None, startrow=2 ,sheet_name='Regionwise Productivity')
            worksheet = writer.sheets['Regionwise Productivity']

            j=7
            for i in range(len(header)):
                worksheet.merge_range(0, j+i*4, 0, j+i*4+3, header[i], header_format)
            
            for col_num, value in enumerate(first_column):
                if col_num <j:
                    worksheet.merge_range(0, col_num, 1, col_num, value, second_header_format)
                else:
                    worksheet.write(1, col_num, value, light_header_format)
                    
        def trainer_productivity_qp():
            cnxn=pyodbc.connect(conn_str)
            curs = cnxn.cursor()
            sql = 'exec [reports].[sp_trainer_productivity_report_qp] ?, ?, ?, ?, ?, ?, ?'
            values = (user_id, user_role_id, region_ids, t_status, trainer_ids, from_date, to_date)
            curs.execute(sql,(values))
            data = curs.fetchall()
            data = list(map(lambda x:list(x), data))
            df = pd.DataFrame(data)

            first_column = ['Trainer Name','QP Name','Course Code','Course Name','No of On going Batches','On going Training (Enrol)','Nos Attendance %','Hour Attendance %','Drop Out %','Certified Target','Certified Actual','Passed %','Placed %','Certified Target','Certified Actual','Passed %','Placed %','Certified Target','Certified Actual','Passed %','Placed %']
            header = ['MTD','QTD','YTD']
            
            df.to_excel(writer, index=None, header=None, startrow=2 ,sheet_name='QP and Course wise Productivity')

            worksheet = writer.sheets['QP and Course wise Productivity']
            
            j=9
            for i in range(len(header)):
                worksheet.merge_range(0, j+i*4, 0, j+i*4+3, header[i], header_format)
            
            for col_num, value in enumerate(first_column):
                if col_num <j:
                    worksheet.merge_range(0, col_num, 1, col_num, value, second_header_format)
                else:
                    worksheet.write(1, col_num, value, light_header_format)
            
                
        t1 = threading.Thread(target=trainer_productivity_region) 
        t2 = threading.Thread(target=trainer_productivity_qp)
        
        t1.start()
        t2.start()
        
        t1.join() 
        t2.join()
                        
        writer.save()
        return({'Description':'created excel', 'Status':True, 'filename':report_name})
        
    except Exception as e:
        return({'Description':'Error creating excel', 'Status':False, 'Error':str(e)})