'''
conn_str = (
            r'Driver={SQL Server};'
            r'Server=LNJAGDISH;'
            r'Database=MCLG_LIVE_Aug1;'
            r'Trusted_Connection=yes;'
            )
import pypyodbc as pyodbc
conn = pyodbc.connect(conn_str)
curs = conn.cursor()
curs.execute("""
EXEC	        [candidate_details].[sp_candidate_report]
		@user_id = NULL,
		@practice_id = NULL,
		@course_id = NULL,
		@from_date =NULL,
		@to_date = NULL
""")
data = curs.fetchall()

"""
le = 0
a= set()
for i in set(map(lambda x:x[12], data)):
	print("section :",i,)
	section = list(filter(lambda x:x[12]==i, data))
	question = set(map(lambda x:(x[15],x[16]),section))
	print(question, len(question))
	a=a|question
	le += len(question)

print(le,len(a))
"""
'''
def create_report(data,report_name):
    try:
        import xlsxwriter
        image_url = 'http://mcl.labournet.in/data/'
    except:
        return {'Description':'Module Error','Status':False}
    try:
        
        workbook = xlsxwriter.Workbook(report_name)

        header_format = workbook.add_format({
            'bold': True,
            #'text_wrap': True,
            'align': 'top',
            'valign': 'center',
            'fg_color': '#D7E4BC',
            'border': 1})

        merge_format = workbook.add_format({
            'border': 1,
            'align': 'top',
            'valign': 'top'})

        write_format = workbook.add_format({
            'border': 1,
            'align': 'top',
            'valign': 'top'})

        url_format = workbook.add_format({
            'border': 1,
            'align': 'top',
            'valign': 'top',
            'font_color': 'blue',
            'underline': 1})
        

        #worksheet = workbook.add_worksheet('Stage Log')

        for i in set(map(lambda x:(x[12],x[13]), data)):
            print(i[1])
            row=1
            worksheet = workbook.add_worksheet(str(i[1]))
            section = list(filter(lambda x:x[12]==i[0], data))
            question = set(map(lambda x:(x[15],x[16],x[22]),section))
            
            default_column = ['Candidate_id','Candidate_Name', 'Candidate_Mobile_Number', 'Date_Of_Join',
                          'Course_Name', 'Center_Name', 'Section_Name', 'Client_Name', 'Section_Completion_Date']
            default_column += [i[1] for i in question] + ['Section_Result', 'Registration_Id', 'Enrollment_Id']
            #print(default_column)
            candidate = set(map(lambda x:(x[0],x[1],x[2],x[3],x[8],x[9],x[10],x[11],x[14],x[18],x[19],x[20],x[21]),section))

            #print(question)
            for col_num, value in enumerate(default_column):
                worksheet.write(0, col_num, value, header_format)

            list_ques_id = [(j[0],j[2]) for j in question]

            for candi in candidate:
                """
                worksheet.write(row, 0, candi[1], write_format) #Name
                worksheet.write(row, 1, candi[2], write_format) #mobile_num
                worksheet.write(row, 2, candi[3], write_format) #DOJ
                worksheet.write(row, 3, candi[5], write_format) #course name
                worksheet.write(row, 4, candi[7], write_format) #center name
                worksheet.write(row, 5, i[1], write_format)     #section name
                worksheet.write(row, 6, candi[12], write_format)#client
                worksheet.write(row, 7, candi[8], write_format) #section completion date
                """
                
                max_l =1
                for lq in list_ques_id:
                    if lq[1]==13:
                        question_length_func = lambda x:(x[0]==candi[0]) and (x[1]==candi[1]) and (x[2]==candi[2]) and (x[3]==candi[3]) and (x[8]== candi[4]) and (x[10]==candi[6]) and (x[14]==candi[8]) and (x[18]==candi[9]) and (x[19]==candi[10]) and (x[20]==candi[11]) and (x[15]==lq[0]) and (x[22]==13)
                        ques_response = list(filter(question_length_func, data))
                        max_l = len(ques_response) if len(ques_response)>max_l else max_l
                        
                col=9   
                for lq in list_ques_id:
                    question_response_func = lambda x:(x[0]==candi[0]) and (x[1]==candi[1]) and (x[2]==candi[2]) and (x[3]==candi[3]) and (x[8]== candi[4]) and (x[10]==candi[6]) and (x[14]==candi[8]) and (x[18]==candi[9]) and (x[19]==candi[10]) and (x[20]==candi[11]) and (x[15]==lq[0]) and (x[22]==lq[1])
                    ques_response = list(filter(question_response_func, data))
                    #print(ques_response)
                    if max_l==1:
                        #question_response_func = lambda x:(x[0]==candi[0]) and (x[1]==candi[1]) and (x[2]==candi[2]) and (x[3]==candi[3]) and (x[8]== candi[4]) and (x[10]==candi[6]) and (x[14]==candi[8]) and (x[18]==candi[9]) and (x[19]==candi[10]) and (x[20]==candi[11]) and (x[15]==lq[0]) and (x[22]==lq[1])
                        #ques_response = list(filter(question_response_func, data))
                        if ques_response!=[]:
                            if (lq[1]==4) or (lq[1]==13):
                                worksheet.write_url(row, col, image_url+ques_response[0][17],  url_format, string='Image', tip='Click to open image') if (ques_response[0][17]!='') and (ques_response[0][17]!=None) else worksheet.write(row, col, 'NR', write_format) #section completion date
                            else:
                                worksheet.write(row, col, ques_response[0][17] if (ques_response[0][17]!='') and (ques_response[0][17]!=None) else 'NR', write_format) #section completion date
                        else:
                            worksheet.write(row, col, 'NA', write_format) #section completion date

                    else:
                        if lq[1]==13:
                            if ques_response!=[]:
                                for ij in range(len(ques_response)):
                                    worksheet.write_url(row+ij, col, image_url+ques_response[0][17],  url_format, string='Image', tip='Click to open image') if (ques_response[ij][17]!='') and (ques_response[ij][17]!=None) else worksheet.write(row+ij, col, 'NR', write_format) #section completion date
                                    #worksheet.write(row+ij, col, ques_response[ij][17] if (ques_response[ij][17]!='') and (ques_response[ij][17]!=None) else 'NR', write_format)
                            else:
                                worksheet.merge_range(row, col, row + max_l -1, col, 'NA', merge_format)
                        elif lq[1]==4:
                            if ques_response!=[]:
                                worksheet.write_url(row, col, image_url+ques_response[0][17],  url_format, string='Image', tip='Click to open image') if (ques_response[0][17]!='') and (ques_response[0][17]!=None) else worksheet.write(row, col, 'NR', write_format) #section completion date
                            else:
                                worksheet.merge_range(row, col, row + max_l -1, col, 'NA', merge_format)
                        else:
                            if ques_response!=[]:
                                worksheet.merge_range(row, col, row + max_l -1, col, ques_response[0][17] if (ques_response[0][17]!='') and (ques_response[0][17]!=None) else 'NR', merge_format)
                            else:
                                worksheet.merge_range(row, col, row + max_l -1, col, 'NA', merge_format)
                            

                        """
                        if (lq[1]!=13) and (lq[1]!=4):
                            if ques_response!=[]:
                                worksheet.merge_range(row, col, row + max_l -1, col, ques_response[0][17] if (ques_response[0][17]!='') and (ques_response[0][17]!=None) else 'NR', merge_format)
                            else:
                                worksheet.merge_range(row, col, row + max_l -1, col, 'NA', merge_format)
                            #worksheet.write(row, col, ques_response[0][17] if ques_response!=[] else 'NA', write_format) #section completion date
                        elif lq[1]==13:
                            if ques_response!=[]:
                                for ij in range(len(ques_response)):
                                    worksheet.write_url(row+ij, col, image_url+ques_response[0][17],  url_format, string='Image', tip='Click to open image') if (ques_response[ij][17]!='') and (ques_response[ij][17]!=None) else worksheet.write(row+ij, col, 'NR', write_format) #section completion date
                                    #worksheet.write(row+ij, col, ques_response[ij][17] if (ques_response[ij][17]!='') and (ques_response[ij][17]!=None) else 'NR', write_format)
                            else:
                                worksheet.merge_range(row, col, row + max_l -1, col, 'NA', merge_format)
                        else:
                            worksheet.write_url(row, col, image_url+ques_response[0][17],  url_format, string='Image', tip='Click to open image') if (ques_response[0][17]!='') and (ques_response[0][17]!=None) else worksheet.write(row, col, 'NR', write_format) #section completion date
                        """

                    col+=1
                    
                if max_l==1:
                    worksheet.write(row, 0, candi[0], write_format) #Name
                    worksheet.write(row, 1, candi[1], write_format) #Name
                    worksheet.write(row, 2, candi[2], write_format) #mobile_num
                    worksheet.write(row, 3, candi[3], write_format) #DOJ
                    worksheet.write(row, 4, candi[5], write_format) #course name
                    worksheet.write(row, 5, candi[7], write_format) #center name
                    worksheet.write(row, 6, i[1], write_format)     #section name
                    worksheet.write(row, 7, candi[12], write_format)#client
                    worksheet.write(row, 8, candi[8], write_format) #section completion date

                
                    worksheet.write(row, col, candi[9], write_format) #Section_Result
                    worksheet.write(row, col+1, candi[10], write_format) #Registration id
                    worksheet.write(row, col+2, candi[11], write_format) #Enrollment id
                else:
                    worksheet.merge_range(row, 0, row + max_l -1, 0, candi[0], merge_format)
                    worksheet.merge_range(row, 1, row + max_l -1, 1, candi[1], merge_format)
                    worksheet.merge_range(row, 2, row + max_l -1, 2, candi[2], merge_format)
                    worksheet.merge_range(row, 3, row + max_l -1, 3, candi[3], merge_format)
                    worksheet.merge_range(row, 4, row + max_l -1, 4, candi[5], merge_format)
                    worksheet.merge_range(row, 5, row + max_l -1, 5, candi[7], merge_format)
                    worksheet.merge_range(row, 6, row + max_l -1, 6, i[1], merge_format)
                    worksheet.merge_range(row, 7, row + max_l -1, 7, candi[12], merge_format)
                    worksheet.merge_range(row, 8, row + max_l -1, 8, candi[8], merge_format)

                    
                    worksheet.merge_range(row, col, row + max_l -1, col, candi[9], merge_format)
                    worksheet.merge_range(row, col+1, row + max_l -1, col+1, candi[10], merge_format)
                    worksheet.merge_range(row, col+2, row + max_l -1, col+2, candi[11], merge_format)
                    
                
                row+=max_l
                
            
        workbook.close()
        return {'Report Name':report_name,'Status':True}

        
        
        

    except Exception as e:
        return {'Description':'Not able to create file becuase of '+str(e),'Status':False}
    
        

    



"""
	print("section :",i,)
	section = list(filter(lambda x:x[12]==i, data))
	question = set(map(lambda x:(x[15],x[16]),section))
	print(question, len(question))
	a=a|question
	le += len(question)

"""


"""
can = list(filter(lambda x:x[0]==2 and x[8]==17 and x[12]==7 and x[10]==16 and x[22]==13, data))
len(can)
import pandas as pd
df = pd.DataFrame(can)
df.head()




"""








