import pypyodbc as pyodbc
#import pyodbc
from .config import *
#from Database import config
import pandas as pd
from datetime import datetime
from flask import request,make_response
import requests
import xml.etree.ElementTree as ET
import io
import csv
import json
import sent_mail
import os
import xlsxwriter,re,os,zipfile,zlib 


def to_xml(df, filename=None, mode='w'):
    if len(df)>0:
        if 'Candidate_Family_Details_Id' in df:
            df1=df[['Candidate_Id','Family_Salutation','Family_Name','Family_Date_Of_Birth','Family_Age','Family_Primary_Contact','Family_Email_Address','Family_Gender','Family_Education','Family_Relationship','Family_Current_Occupation','Candidate_Family_Details_Id']]
            df2=df.drop(['Family_Salutation','Family_Name','Family_Date_Of_Birth','Family_Age','Family_Primary_Contact','Family_Email_Address','Family_Gender','Family_Education','Family_Relationship','Family_Current_Occupation','Candidate_Family_Details_Id'],axis=1)
            
        else:
            df1=df[['Candidate_Id','Activity_Status_Id','Activity_Status_Name','Reason','Remarks','Activity_Date','Device_Date','Created_On']]
            df2=df.drop(['Activity_Status_Id','Activity_Status_Name','Reason','Remarks','Activity_Date','Device_Date','Created_On'],axis=1)
        df2.drop_duplicates(subset ="Candidate_Id",inplace=True)
    else:
        df1=None
        df2=None

    def nested_row_to_xml(row):
        xml = ['      <status>']
        for i, col_name in enumerate(row.index):
            xml.append('        <field name="{0}">{1}</field>'.format(col_name, row.iloc[i]))
        xml.append('      </status>')
        return '\n'.join(xml)

    def nested_family_details_row_to_xml(row):
        xml = ['      <family>']
        for i, col_name in enumerate(row.index):
            xml.append('        <field name="{0}">{1}</field>'.format(col_name, row.iloc[i]))
        xml.append('      </family>')
        return '\n'.join(xml)

    def row_to_xml(row):
        xml = ['  <candidate>']
        for i, col_name in enumerate(row.index):
            xml.append('    <field name="{0}">{1}</field>'.format(col_name, row.iloc[i]))
        if 'Candidate_Family_Details_Id' in df1:
            df3=df1.loc[(df1['Candidate_Id'] == row['Candidate_Id']) & (df1['Candidate_Family_Details_Id']>0)]
            xml.append('    <family_details>')
            xml.append('\n'.join(df3.apply(nested_family_details_row_to_xml, axis=1)))
            xml.append('    </family_details>')
        else:
            df3=df1.loc[(df1['Candidate_Id'] == row['Candidate_Id']) & (df1['Activity_Status_Id']>0)]
            xml.append('    <statushistory>')
            xml.append('\n'.join(df3.apply(nested_row_to_xml, axis=1)))
            xml.append('    </statushistory>')
        #print(df3.dtypes)
        
        xml.append('  </candidate>')
        return '\n'.join(xml)
    res=''
    if len(df)>0:
        res = '\n'.join(df2.apply(row_to_xml, axis=1))
    
    out = ['<data>',res,'</data>']
    res = '\n'.join(out)
    if filename is None:
        return res
    with open(filename, mode) as f:
        f.write(res)

pd.DataFrame.to_xml = to_xml

class Database:
    def AppVersionCheck(curs, app_version):
        quer = "SELECT TOP (1) version_code FROM [masters].[tbl_mclg_app_version_history] order by id desc"
        curs.execute(quer)
        data=curs.fetchall()
        data = 0 if data==[] else data[0][0]
        return (int(app_version) >= int(data))

    def Login(email,passw):
        tr =[]
        h={}
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [users].[sp_user_login] ?, ?'
        values = (email,passw)
        #print(values)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        #cur.execute("SELECT u.user_id,u.user_name,u.user_role_id FROM users.tbl_users AS u LEFT JOIN users.tbl_user_details AS ud ON ud.user_id=u.user_id where ud.email='"+email+"' AND u.password='"+passw+"';")
        for row in cur:
            for i in range(len(columns)):
                h[columns[i]]=row[i]
            #h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[3]+"":row[3]}
            tr.append(h)
        cur.commit()
        cur.close()
        con.close()
        return tr
    def practicebasedonuser(user_id):
        prac = []
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [users].[sp_user_practice_course_neo] ?, ?'
        values = (user_id,None)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[2]+"":row[2],""+columns[3]+"":row[3]}
            prac.append(h)
        cur.close()
        con.close()
        practiceforuser={'Pratices': prac}
        return practiceforuser
    def CourseBasedOnUserPractice(user_id,practice_id):
        courses =[]
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [users].[sp_user_practice_course_neo] ?, ?'
        values = (user_id,practice_id)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        lent=0
        for row in cur:
            course_json = list(set(list(zip(list(map(int,row[4].split(','))),row[5].split(',')))))
            #courseid = row[4].split(",")
            #oursename = row[5].split(",")
            #lent=len(courseid)
            #print(course_json)
        for course in course_json:
            h = { 'Course_Id': course[0], 'Course_Name':course[1]}
            courses.append(h)
        cur.close()
        con.close()
        courseforuserpractice={'Courses': courses}
        return courseforuserpractice
    def preview_center_count(course_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        preview = []
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [candidate_details].[sp_center_wise_count_report_temp] ?, ?, ?, ?, ?, ?'
        values = (course_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction)
        cur.execute(sql, (values))
        columns = [column[0].title() for column in cur.description]
        temp=cur.fetchall()
        if temp == []:
            return 0
        record="0"
        fil="0"
        record=temp[0][8]
        fil=temp[0][9]
        #print(temp)
        # for r in range(0,len(temp),3):
        r=0
        while r < len(temp):
            h=[]
            for i in range(0,len(temp[r])-6):
                h.append(temp[r][i])
            for c in range(r,r+temp[r][7]):
                h.append(str(temp[c][4])+","+str(temp[c][6]))
            preview.append(h)
            #print(h)
            r=r+temp[r][7]
            print(r)
        print(preview)
        count_list = []
        for one in preview:
            print(len(one))
            if len(one)==5:
                al=[]
                k=one[4].split(',')
                print(k[0])
                if k[0]==str(18):
                    al = [0,0,k[1]]
                elif k[0]==str(17):
                    al = [0,k[1],0]
                elif k[0]==str(12):
                    al = [k[1],0,0]
                count_list.append(al)
            elif len(one)==6:
                al=[]
                k1=one[4].split(',')
                k2=one[5].split(',')
                if k1[0]==str(18):
                    #al.appen(k1[1])
                    if k2[0]==str(17):
                        al = [0,k2[1],k1[1]]
                elif k1[0]==str(17):
                    al= [k2[1],k1[1],0]
                count_list.append(al)
            elif len(one)==7:
                al=[]
                k1=one[4].split(',')
                k2=one[5].split(',')
                k3=one[6].split(',')
                al=[k3[1],k2[1],k1[1]]
                count_list.append(al)
        print(count_list)
        cur.close()
        #print(preview)
        final_format =[]
        TTotal=0
        for i in range(0,len(preview)):
            g={"Practice_Name":preview[i][0],"Course_Name":preview[i][1],"Center_Id":preview[i][2],"Center_Name":preview[i][3],"MCL":count_list[i][0],"REG":count_list[i][1],"ENR":count_list[i][2],"Total":int(count_list[i][0])+int(count_list[i][1])+int(count_list[i][2])}
            TTotal=TTotal+int(count_list[i][0])+int(count_list[i][1])+int(count_list[i][2])
            final_format.append(g)
        con.close()
        counts= { "draw":draw,"recordsTotal":len(preview),"recordsFiltered":len(preview),'data' : final_format, 'total': TTotal}
        print(counts)
        return counts
    
    def report_table_db(user_id, practice_id, course_id, date_from, date_to):
        con = pyodbc.connect(conn_str)
        curs = con.cursor()
        # curs.execute("select * from [masters].[tbl_courses] where course_id='{}'".format(course))
        # course_id = curs.fetchall()[0][0]
        
        # curs.execute("select * from [masters].[tbl_practice] where practice_id='{}'".format(practice))
        # practice_id = curs.fetchall()[0][0]
        
        

        quer = "call [candidate_details].[sp_candidate_report]({},{},{},'{}','{}')".format(user_id, practice_id, course_id, date_from, date_to)
        quer = "{"+ quer + "}"
        
        curs.execute(quer)
        
        data = curs.fetchall()

        """
        data=[]
        for row in curs:
            h=[]
            for i in range(0,len(row)):
                v=row[i]
                h.append(v)
            data.append(h)
        ind=[]
        cl = ['candidate_id','candidate_name','candidate_mobile_number','date_of_join','mobilizer_name','workflow_id','practice_id','practice_name','course_id','course_name','center_id','center_name','section_id','section_name','section_completion_date','question_id','question_text','response','section_result','registration_id','enrollment_id']
        for i in range(0,len(data)):
            ind.append(i)
        #print(pd.DataFrame(data,columns=cl))
        df = pd.DataFrame(data,columns=cl)
        column_req=['candidate_name','candidate_mobile_number','date_of_join','mobilizer_name','practice_name','course_name','center_name','section_name','section_completion_date','question_text','response','section_result','registration_id','enrollment_id']
        df= df[column_req]
        df.columns = ['Candidate_Name','Candidate_Mobile_Number','Date_Of_Join','Mobilizer_Name','Practice_Name','Course_Name','Center_Name','Section_Name','Section_Completion_Date','Question_Text','Response','Section_Result','Registration_Id','Enrollment_Id']
        """

        
        curs.close()
        con.close()
        return data

    def center_type_list(center_type_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        content = {}
        d = []
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [masters].[sp_get_center_types_list] ?, ?, ?, ?, ?, ?'
        values = (center_type_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        record="0"
        fil="0"
        for row in cur:
            record=row[6]
            fil=row[5]
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[3]+"":row[3],""+columns[4]+"":row[4]}
            d.append(h)
        content = {"draw":draw,"recordsTotal":record,"recordsFiltered":fil,"data":d}
        cur.close()
        con.close()
        #global count
        #count = count + 1
        return content

    def add_center_type_details(center_type_name,user_id,is_active,center_type_id):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec	masters.sp_add_edit_center_types ?, ?, ?, ?'
        values = (center_type_id,center_type_name,user_id,is_active)
        cur.execute(sql,(values))
        for row in cur:
            pop=row[1]
        cur.commit()
        cur.close()
        con.close()
        if pop ==1:
            msg={"message":"Updated"}
        else:
            msg={"message":"Created"}
        return msg
    def get_center_type_details(glob_center_type_id):
        
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        
        sql = 'SELECT * FROM [masters].[tbl_center_type] where center_type_id=?'
        values = (glob_center_type_id,)
        
        cur.execute(sql,(values))
        
        columns = [column[0].title() for column in cur.description]
        
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[3]+"":row[3],""+columns[4]+"":row[4]}
        
        cur.close()
        con.close()
        return h

    def center_category_list(center_category_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        content = {}
        d = []
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [masters].[sp_get_center_category_list] ?, ?, ?, ?, ?, ?'
        values = (center_category_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        record="0"
        fil="0"
        for row in cur:
            record=row[6]
            fil=row[5]
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[3]+"":row[3],""+columns[4]+"":row[4]}
            d.append(h)
        content = {"draw":draw,"recordsTotal":record,"recordsFiltered":fil,"data":d}
        cur.close()
        con.close()
        return content
    def add_center_category_details(center_category_name,user_id,is_active,center_category_id):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec	masters.sp_add_edit_center_categories ?, ?, ?, ?'
        values = (center_category_id,center_category_name,user_id,is_active)
        cur.execute(sql,(values))
        for row in cur:
            pop=row[1]
        cur.commit()
        cur.close()
        con.close()
        if pop ==1:
            msg={"message":"Updated"}
        else:
            msg={"message":"Created"}
        return msg
    def get_center_category_details(glob_center_category_id):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'SELECT * FROM [masters].[tbl_center_category] where center_category_id=?'
        values = (glob_center_category_id,)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[3]+"":row[3],""+columns[4]+"":row[4]}
        cur.close()
        con.close()
        return h
    
    def project_list(user_id,user_role_id,user_region_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw,entity,customer,p_group,block,practice,bu,product,status):
        content = {}
        d = []
        h={}
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [masters].[sp_get_project_list] ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?'
        values = (user_id,user_role_id,user_region_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,entity,customer,p_group,block,practice,bu,product,status)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        record="0"
        fil="0"
        for row in cur:
            record=row[len(columns)-1]
            fil=row[len(columns)-2]
            for i in range(len(columns)-2):
                h[columns[i]]=row[i]
            d.append(h.copy())
        content = {"draw":draw,"recordsTotal":record,"recordsFiltered":fil,"data":d}
        cur.close()
        con.close()
        return content
        
    def GetALLClient(user_id,user_role_id):
        client = []
        h={}
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()
        values=(user_id,user_role_id)
        sql='exec [masters].[sp_get_all_clients] ?,?'
        cur2.execute(sql,(values))
        columns = [column[0].title() for column in cur2.description]
        for row in cur2:
            for i in range(len(columns)):
                h[columns[i]]=row[i]            
            client.append(h.copy())
            #h = {""+columns[0]+"":r[0],""+columns[1]+"":r[1]}
            #client.append(h)
        cur2.close()
        con.close()
        return client
    def add_project_details(ProjectName, ProjectCode, ClientName, ContractName, Practice, BU, projectgroup, ProjectType, Block, Product, ProjectManager, ActualEndDate, ActualStartDate, PlannedEndDate, PlannedStartDate, isactive, project_id, user_id,CourseIds):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec	[masters].[sp_add_edit_project] ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?'
        values = (ProjectName, ProjectCode, ClientName, ContractName, Practice, BU, projectgroup, ProjectType, Block, Product, ProjectManager, ActualEndDate, ActualStartDate, PlannedEndDate, PlannedStartDate, isactive, project_id, user_id,CourseIds)
        #print(values)
        cur.execute(sql,(values))
        for row in cur:
            pop=row[1]
        cur.commit()
        cur.close()
        con.close()
        if pop ==1:
            msg={"message":"Updated","client_flag":1}
        else: 
                if pop==0:
                    msg={"message":"Created","client_flag":0}
                else:
                    if pop==2:
                        msg={"message":"Customer with the Customer code already exists","client_flag":2}
        return msg
    
    def add_subproject_details(SubProjectName, SubProjectCode, Region, State, Centers, Course, PlannedStartDate, PlannedEndDate, ActualStartDate, ActualEndDate, user_id, subproject_id, project_code, isactive, is_ojt_req):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec	[masters].[sp_add_edit_subproject] ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?'
        values = (SubProjectName, SubProjectCode, Region, State, Centers, Course, PlannedStartDate, PlannedEndDate, ActualStartDate, ActualEndDate, user_id, subproject_id, project_code, isactive, is_ojt_req)
        #print(values)
        cur.execute(sql,(values))
        for row in cur:
            pop=row[1]
        cur.commit()
        cur.close()
        con.close()
        if pop ==1:
            msg={"message":"Updated","client_flag":1}
        else: 
                if pop==0:
                    msg={"message":"Created","client_flag":0}
                else:
                    if pop==2:
                        msg={"message":"Customer with the Customer code already exists","client_flag":2}
        return msg
        
    def get_project_details(glob_project_id):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        h={}
        sql = "[masters].[sp_get_project_details] ?"
        values = (glob_project_id,)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            for i in range(len(columns)):
                h[columns[i]]=row[i]
            #h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[3]+"":row[3],""+columns[4]+"":row[4],""+columns[5]+"":row[5],""+columns[6]+"":row[6],""+columns[7]+"":row[7],""+columns[8]+"":row[8],""+columns[9]+"":row[9],""+columns[10]+"":row[10],""+columns[11]+"":row[11],""+columns[12]+"":row[12],""+columns[13]+"":row[13],""+columns[14]+"":row[14],""+columns[15]+"":row[15]}
        cur.close()
        con.close()
        return h
    
    def get_subproject_details(glob_project_id):
        h={}
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = "exec	[masters].[sp_GetsubprojectDetails] ?"
        values = (glob_project_id,)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            for i in range(len(columns)):
                h[columns[i]]=row[i]
        cur.close()
        con.close()
        return h.copy()
    
    def center_list(center_id,user_id,user_role_id,user_region_id,center_type_ids,bu_ids,status,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw,regions,clusters,courses):
        content = {}
        d = []
        h={}
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [masters].[sp_get_centers_list] ?,?,?,?, ?, ?, ?, ?, ?,?,?,?,?,?,?'        
        values = (center_id,user_id,user_role_id,user_region_id,center_type_ids,bu_ids,status,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,regions,clusters,courses)
        #print(values)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        record="0"
        fil="0"
        for row in cur:
            record=row[len(columns)-1]
            fil=row[len(columns)-2]
            for i in range(len(columns)-2):
                h[columns[i]]=row[i]            
            d.append(h.copy())
        content = {"draw":draw,"recordsTotal":record,"recordsFiltered":fil,"data":d}
        cur.close()
        con.close()
        return content

    def add_center_details(center_name,user_id,is_active,center_id,center_type_id,country_id,satet_id,location_name,address,pincode,District,partner_id,geolocation):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec	[masters].[sp_add_edit_centers] ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?,?, ?'
        values = (center_name,user_id,is_active,center_id,center_type_id,country_id,satet_id,location_name,address,pincode,District,partner_id, geolocation)
        #print(values)
        cur.execute(sql,(values))
        for row in cur:
            pop=row[1]
        cur.commit()
        cur.close()
        con.close()
        if pop ==1:
            msg={"message":"Updated"}
        else:
            msg={"message":"Created"}
        return msg
    def GetCenter(glob_center_id):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'SELECT * FROM [masters].[tbl_center] where center_id=?'
        values = (glob_center_id,)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[3]+"":row[3],""+columns[4]+"":row[4],""+columns[5]+"":row[5],""+columns[6]+"":row[6],""+columns[7]+"":row[7],""+columns[8]+"":row[8],""+columns[9]+"":row[9],""+columns[10]+"":row[10],""+columns[11]+"":row[11],""+columns[12]+"":row[12],""+columns[13]+"":row[13]}
        cur.close()
        con.close()
        return h
    def GetCenterType():
        center_type = []
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()
        cur2.execute("EXEC [masters].[sp_get_all_center_types] @center_type_id = NULL;")
        columns = [column[0].title() for column in cur2.description]
        for r in cur2:
            h = {""+columns[0]+"":r[0],""+columns[1]+"":r[1]}
            center_type.append(h)
        cur2.close()
        con.close()
        return center_type
    def GetCenterCategory():
        center_cat = []
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()
        cur2.execute("EXEC [masters].[sp_get_all_center_categories] @center_category_id = NULL;")
        columns = [column[0].title() for column in cur2.description]
        for r in cur2:
            h = {""+columns[0]+"":r[0],""+columns[1]+"":r[1]}
            center_cat.append(h)
        cur2.close()
        con.close()
        return center_cat
    def get_all_BU():
        bu = []
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'SELECT bu_id, bu_name FROM [masters].[tbl_bu] where is_active=1;'
        cur.execute(sql)
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1]}
            bu.append(h)
        cur.close()
        con.close()
        return bu
    def Get_all_Sponser():
        sponser = []
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'SELECT sponser_id, sponser_name FROM [masters].[tbl_sponser] where is_active=1;'
        cur.execute(sql)
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1]}
            sponser.append(h)
        cur.close()
        con.close()
        return sponser
    def get_all_Cluster_Based_On_Region(region_id):
        cluster = []
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = "SELECT state_id,state_name FROM [masters].[tbl_states] where is_active=1 AND (('{}'='-1')OR(region_id in (select	value from	string_split('{}',',')   WHERE	trim(value)!='' )));".format(region_id,region_id)
        cur.execute(sql)
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1]}
            cluster.append(h)
        cur.close()
        con.close()
        #print(cluster)
        return cluster
    def GetCountry():
        countries = []
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()
        cur2.execute("SELECT country_id, country_name FROM [masters].[tbl_countries]")
        columns = [column[0].title() for column in cur2.description]
        for r in cur2:
            h = {""+columns[0]+"":r[0],""+columns[1]+"":r[1]}
            countries.append(h)
        cur2.close()
        con.close()
        return countries
    def GetStatesBasedOnCountry(country_id):
        states = []
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()
        cur2.execute("EXEC	[masters].[sp_get_all_states_based_on_country] @country_id = "+country_id)
        columns = [column[0].title() for column in cur2.description]
        for r in cur2:
            h = {""+columns[0]+"":r[0],""+columns[1]+"":r[1]}
            states.append(h)
        cur2.close()
        con.close()
        return states
    def GetDistrictsBasedOnStates(state_id):
        districts = []
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()
        cur2.execute("EXEC	[masters].[sp_get_all_districts_based_on_state] @state_id = "+state_id)
        columns = [column[0].title() for column in cur2.description]
        for r in cur2:
            h = {""+columns[0]+"":r[0],""+columns[1]+"":r[1]}
            districts.append(h)
        cur2.close()
        con.close()
        return districts

    def course_list(user_id,user_role_id,course_id,sectors,qps,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw, status):
        content = {}
        d = []
        h={}
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [content].[sp_get_course_list] ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?'
        values = (user_id,user_role_id,course_id,sectors,qps,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,status)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        record="0"
        fil="0"
        for row in cur:
            record=row[len(columns)-1]
            fil=row[len(columns)-2]
            for i in range(len(columns)-2):
                h[columns[i]]=row[i]
            d.append(h.copy())
        content = {"draw":draw,"recordsTotal":record,"recordsFiltered":fil,"data":d}
        cur.close()
        con.close()
        return content
    def GetPractice():
        practice = []
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        cur.execute("EXEC [masters].[sp_get_all_practices] @practice_id = NULL;")
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1]}
            practice.append(h)
        cur.close()
        con.close()
        return practice
    def GetProjectBasedOnPractice(project_id,practice_id):
        projects = []
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql="EXEC [masters].[sp_get_projects_based_on_practice] ?, ?;"
        values=(project_id,practice_id)
        cur.execute(sql, (values))
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1]}
            projects.append(h)
        cur.close()
        con.close()
        return projects
    def GetAllCenter(cluster_id):
        center = []
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()
        sql="EXEC [masters].[sp_get_all_centers] ?, ?;"
        values=(0,cluster_id)
        cur2.execute(sql, (values))
        columns = [column[0].title() for column in cur2.description]
        for r in cur2:
            h = {""+columns[0]+"":r[0],""+columns[1]+"":r[1]}
            center.append(h)
        cur2.close()
        con.close()
        return center
    def GetAllCluster():
        center = []
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()
        cur2.execute("EXEC [masters].[sp_get_all_clusters] @cluster_id = NULL;")
        columns = [column[0].title() for column in cur2.description]
        for r in cur2:
            h = {""+columns[0]+"":r[0],""+columns[1]+"":r[1]}
            center.append(h)
        cur2.close()
        con.close()
        return center
    def GetAllRegion():
        center = []
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()
        cur2.execute("EXEC [masters].[sp_get_all_regions] @region_id = NULL;")
        columns = [column[0].title() for column in cur2.description]
        for r in cur2:
            h = {""+columns[0]+"":r[0],""+columns[1]+"":r[1]}
            center.append(h)
        cur2.close()
        con.close()
        return center
    def GetAllProject():
        center = []
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()
        cur2.execute("EXEC [masters].[sp_get_all_projects] @project_id = NULL;")
        columns = [column[0].title() for column in cur2.description]
        for r in cur2:
            h = {""+columns[0]+"":r[0],""+columns[1]+"":r[1]}
            center.append(h)
        cur2.close()
        con.close()
        return center
    def add_course_details(CourseId, CourseName, CourseCode, Sector, Qp, Parent_Course, Course_Duration_day, Course_Duration_hour, is_ojt_req,OJT_Duration_hour, isactive, user_id):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec	[content].[sp_add_edit_course] ?, ?, ?, ?, ?, ?, ?, ?,?, ?, ?, ?'
        values = (CourseId, CourseName, CourseCode, Sector, Qp, Parent_Course, Course_Duration_day, Course_Duration_hour, is_ojt_req,OJT_Duration_hour, isactive, user_id)
        cur.execute(sql,(values))

        for row in cur:
            pop=row[1]
            if pop != 2:
                batch_code=row[2]
        cur.commit()
        cur.close()
        con.close()
        if pop ==1:
            msg={"message":"{} Updated Successfully".format(batch_code),"course_flag":1}
        else: 
                if pop==0:
                    msg={"message":batch_code+" Created Successfully","course_flag":0}
                else:
                    if pop==2:
                        msg={"message":"Course with the Course code already exists","course_flag":2}
        return msg

    def get_course_details(course_id):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [content].[sp_get_course_detail] ?'
        values = (course_id)
        cur.execute(sql,(values,))
        h={}
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            for i in range(len(columns)):
                h[columns[i]]=row[i]           
            
        cur.close()
        con.close()
        return h.copy()

    def get_qp_course():
        qp = []
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()
        cur2.execute("SELECT qp.qp_id,qp.qp_name FROM masters.tbl_qp AS qp where is_active=1")
        columns = [column[0].title() for column in cur2.description]
        for r in cur2:
            h = {""+columns[0]+"":r[0],""+columns[1]+"":r[1]}
            qp.append(h)
        cur2.close()
        con.close()
        return qp
        
    
    def user_role_list(user_role_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        content = {}
        d = []
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [users].[sp_get_user_role_list] ?, ?, ?, ?, ?, ?'
        values = (user_role_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        record="0"
        fil="0"
        for row in cur:
            record=row[6]
            fil=row[5]
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[3]+"":row[3],""+columns[4]+"":row[4]}
            d.append(h)
        content = {"draw":draw,"recordsTotal":record,"recordsFiltered":fil,"data":d}
        cur.close()
        con.close()
        return content
    def add_user_role_details(user_role_name,user_id,is_active,user_role_id):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec	[users].[sp_add_edit_user_role] ?, ?, ?, ?'
        values = (user_role_name,user_id,is_active,user_role_id)
        cur.execute(sql,(values))
        for row in cur:
            pop=row[1]
        cur.commit()
        cur.close()
        con.close()
        if pop ==1:
            msg={"message":"Updated"}
        else:
            msg={"message":"Created"}
        return msg
    def get_user_role_details(glob_user_role_id):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'SELECT * FROM [users].[tbl_user_role] where user_role_id=?'
        values = (glob_user_role_id,)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[3]+"":row[3],""+columns[4]+"":row[4]}
        cur.close()
        con.close()
        return h    
    def user_list(user_id,filter_role_id,user_region_id,user_role_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw, dept_ids, role_ids, entity_ids, region_ids, RM_Role_ids, R_mangager_ids,status_ids,project_ids):
        content = {}
        d = []
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [users].[sp_get_users_list] ?, ?, ?, ?, ?, ?,? ,? ,? ,? ,? ,?, ?, ?, ?, ?, ?'
        values = (user_id,filter_role_id,user_region_id,user_role_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction, dept_ids, role_ids, entity_ids, region_ids, RM_Role_ids, R_mangager_ids,status_ids,project_ids)
        print(values)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        record="0"
        fil="0"
        for row in cur:
            record=row[22]
            fil=row[21]
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[3]+"":row[3],""+columns[4]+"":row[4],""+columns[5]+"":row[5],""+columns[6]+"":row[6],""+columns[7]+"":row[7],""+columns[8]+"":row[8],""+columns[9]+"":row[9],""+columns[10]+"":row[10],""+columns[11]+"":row[11],""+columns[12]+"":row[12],""+columns[13]+"":row[13],""+columns[14]+"":row[14],""+columns[15]+"":row[15],""+columns[16]+"":row[16],""+columns[17]+"":row[17],""+columns[18]+"":row[18],""+columns[19]+"":row[19],""+columns[20]+"":row[20]}
            d.append(h)
        content = {"draw":draw,"recordsTotal":record,"recordsFiltered":fil,"data":d}
        cur.close()
        con.close()
        return content
    def trainer_list(user_id,user_region_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw,user_role_id,centers, status, Region_id, Cluster_id, Dept,entity_ids,project_ids,sector_ids,TrainerType):
        content = {}
        d = []
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [users].[sp_get_trainer_list] ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?,?,?,?'
        values = (user_id,user_region_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,user_role_id,centers, status, Region_id, Cluster_id, Dept,entity_ids,project_ids,sector_ids,TrainerType)
        
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        record="0"
        fil="0"
        for row in cur:
            record=row[18]
            fil=row[17]
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[3]+"":row[3],""+columns[4]+"":row[4],""+columns[5]+"":row[5],""+columns[6]+"":row[6],""+columns[7]+"":row[7],""+columns[8]+"":row[8],""+columns[9]+"":row[9],""+columns[10]+"":row[10],""+columns[11]+"":row[11],""+columns[12]+"":row[12],""+columns[13]+"":row[13],""+columns[14]+"":row[14],""+columns[15]+"":row[15],""+columns[16]+"":row[16]}
            d.append(h)
        content = {"draw":draw,"recordsTotal":record,"recordsFiltered":fil,"data":d}
        cur.close()
        con.close()
        return content
    def add_user_details(user_role_id,first_name,last_name,email,mobile,created_id,is_active,user_id,Id,is_reporting_manager):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec	[users].[sp_add_edit_users] ?, ?, ?, ?, ?, ?, ?, ?, ?, ?'
        if Id == None:
            values = (user_role_id,first_name,last_name,email,mobile,created_id,is_active,user_id,"",is_reporting_manager)
        else:
            values = (user_role_id,first_name,last_name,email,mobile,created_id,is_active,user_id,Id,is_reporting_manager)
        cur.execute(sql,(values))
        for row in cur:
            pop=row[1]
            UserId=row[0]
        cur.commit()
        cur.close()
        con.close()
        if pop ==1:
            msg={"message":"Updated" , "UserId": UserId}
        else: 
            if pop==0:
                msg={"message":"Created", "UserId": UserId}
            else:
                if pop==2:
                    msg={"message":"User with the email id already exists", "UserId": UserId}
        return msg
    def GetUserRole():
        userrole = []
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()
        cur2.execute("Select * from users.tbl_user_role where is_active=1;")
        columns = [column[0].title() for column in cur2.description]
        for r in cur2:
            h = {""+columns[0]+"":r[0],""+columns[1]+"":r[1]}
            userrole.append(h)
        cur2.close()
        con.close()
        return userrole
    def get_user_details(glob_user_id):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'EXEC	[users].[sp_get_user_details] @user_id = ?'
        values = (glob_user_id,)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[3]+"":row[3],""+columns[4]+"":row[4],""+columns[5]+"":row[5],""+columns[6]+"":row[6],""+columns[7]+"":row[7],columns[8]+"":row[8],columns[9]+"":row[9]}
        cur.close()
        con.close()
        return h
    def get_user_role_details_for_role_update(user_id):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        h={}
        sql = 'EXEC	[users].[sp_get_user_role_details] @user_id = ?'
        values = (user_id,)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        #print(columns)
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[3]+"":row[3],""+columns[4]+"":row[4],""+columns[5]+"":row[5],""+columns[6]+"":row[6],""+columns[7]+"":row[7],columns[8]+"":row[8]}
        cur.close()
        con.close()
        print(h)
        return h
    def batch_list(batch_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw,user_id,user_role_id):
        content = {}
        d = []
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [batches].[sp_get_batch_list] ?, ?, ?, ?, ?, ?, ?, ?'
        values = (batch_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,user_id,user_role_id)
        print(values)
        cur.execute(sql,(values))        
        columns = [column[0].title() for column in cur.description]
        record="0"
        fil="0"
        for row in cur:
            record=row[20]
            fil=row[19]
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[3]+"":row[3],""+columns[4]+"":row[4],""+columns[5]+"":row[5],""+columns[6]+"":row[6],""+columns[7]+"":row[7],""+columns[8]+"":row[8],""+columns[9]+"":row[9],""+columns[10]+"":row[10],""+columns[11]+"":row[11],""+columns[12]+"":row[12],""+columns[13]+"":row[13],""+columns[14]+"":row[14],""+columns[15]+"":row[15],""+columns[16]+"":row[16],""+columns[17]+"":row[17],""+columns[18]+"":row[18]}
            d.append(h)
        content = {"draw":draw,"recordsTotal":record,"recordsFiltered":fil,"data":d}
        cur.close()
        con.close()
        return content
        
    def batch_list_updated(batch_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw,user_id,user_role_id, status, customer, project, sub_project, region, center, center_type,course_ids,batch_codes, BU, Planned_actual, StartFromDate, StartToDate, EndFromDate, EndToDate):
        #print(status, customer, project, course, region, center)
        content = {}
        d = []
        h={}
        con = pyodbc.connect(conn_str)
        cur = con.cursor()

        sql = 'exec [batches].[sp_get_batch_list_updatd] ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?, ?, ?, ?, ?, ?'

        values = (batch_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,user_id,user_role_id, status, customer, project, sub_project, region, center, center_type, BU,course_ids, batch_codes,Planned_actual, StartFromDate, StartToDate, EndFromDate, EndToDate) #

        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        record="0"
        fil="0"
        for row in cur:
            record=row[len(columns)-2]
            fil=row[len(columns)-1]
            for i in range(len(columns)-1):
                h[columns[i]]=row[i]
            d.append(h.copy())
        content = {"draw":draw,"recordsTotal":record,"recordsFiltered":fil,"data":d}
        cur.close()
        con.close()
        return content
    def batch_list_assessment(batch_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw,user_id,user_role_id, status, customer, project, sub_project, region, center, center_type,course_ids,assessment_stage_id, BU, Planned_actual, StartFromDate, StartToDate, EndFromDate, EndToDate):
        #print(status, customer, project, course, region, center)
        content = {}
        d = []
        h={}
        con = pyodbc.connect(conn_str)
        cur = con.cursor()

        sql = 'exec [batches].[sp_get_batch_list_assessment] ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?, ?, ?, ?,?, ?, ?, ?, ?, ?'

        values = (batch_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,user_id,user_role_id, status, customer, project, sub_project, region, center, center_type, BU,course_ids,assessment_stage_id, Planned_actual, StartFromDate, StartToDate, EndFromDate, EndToDate) #
        #print(values)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        record="0"
        fil="0"
        for row in cur:
            record=row[len(columns)-1]
            fil=row[len(columns)-2]
            for i in range(len(columns)-2):
                h[columns[i]]=row[i]
            d.append(h.copy())
        content = {"draw":draw,"recordsTotal":record,"recordsFiltered":fil,"data":d}
        cur.close()
        con.close()
        return content
    def batch_list_certification(batch_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw,user_id,user_role_id, status, customer, project, sub_project, region, center, center_type,course_ids,assessment_stage_id,certification_stage_id, BU, Planned_actual, StartFromDate, StartToDate, EndFromDate, EndToDate):
        #print(status, customer, project, course, region, center)
        content = {}
        d = []
        h={}
        con = pyodbc.connect(conn_str)
        cur = con.cursor()

        sql = 'exec [batches].[sp_get_batch_list_certification] ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?, ?, ?, ?,?, ?, ?, ?, ?, ?'

        values = (batch_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,user_id,user_role_id, status, customer, project, sub_project, region, center, center_type, BU,course_ids,assessment_stage_id,certification_stage_id, Planned_actual, StartFromDate, StartToDate, EndFromDate, EndToDate) #
        #print(values)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        record="0"
        fil="0"
        for row in cur:
            record=row[len(columns)-1]
            fil=row[len(columns)-2]
            for i in range(len(columns)-2):
                h[columns[i]]=row[i]
            d.append(h.copy())
        content = {"draw":draw,"recordsTotal":record,"recordsFiltered":fil,"data":d}
        cur.close()
        con.close()
        return content

    def add_batch_details(BatchName, Product, Center, Course, SubProject, Cofunding, Trainer, isactive, PlannedStartDate, PlannedEndDate, ActualStartDate, ActualEndDate, StartTime, EndTime, BatchId, user_id, room_ids,planned_batch_id,OJTStartDate, OJTEndDate):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec	batches.sp_add_edit_batches ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?, ?, ?'
        values = (BatchName, Product, Center, Course, SubProject, Cofunding, Trainer, isactive, PlannedStartDate, PlannedEndDate, ActualStartDate, ActualEndDate, StartTime, EndTime, BatchId, user_id, room_ids,planned_batch_id,OJTStartDate, OJTEndDate)
        cur.execute(sql,(values))
        batch_code=""
        for row in cur:
            pop=row[1]
            batch_code=row[2]
        cur.commit()
        cur.close()
        con.close()
        if pop ==1:
            msg={"message":"{} Updated Successfully".format(batch_code),"batch_flag":1}
        else: 
                if pop==0:
                    msg={"message":batch_code+" Created Successfully","batch_flag":0}
                else:
                    if pop==2:
                        msg={"message":"Batch with the Batch code already exists","batch_flag":2}
        return msg
        
    def get_batch_details(batch_id):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        h={}
        sql = 'exec	[batches].[sp_get_batch_details] ?'
        values = (batch_id,)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            for i in range(len(columns)):
                h[columns[i]]=row[i]
            #h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[3]+"":row[3],""+columns[4]+"":row[4],""+columns[5]+"":row[5],""+columns[6]+"":row[6],""+columns[7]+"":row[7],""+columns[8]+"":row[8],""+columns[9]+"":row[9],""+columns[10]+"":row[10],""+columns[12]+"":row[12],""+columns[11]+"":row[11],""+columns[13]+"":row[13],""+columns[14]+"":row[14]}
        cur.close()
        con.close()
        return h

    def GetCourse():
        course = []
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()
        cur2.execute("Select * from masters.tbl_courses where is_active=1;")
        columns = [column[0].title() for column in cur2.description]
        for r in cur2:
            h = {""+columns[0]+"":r[0],""+columns[1]+"":r[1]}
            course.append(h)
        cur2.close()
        con.close()
        return course
    def GetCenterBasedOnCourse(course_id):
        centers = []
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()
        cur2.execute("EXEC masters.sp_get_centers_based_on_course @course_id="+course_id)
        columns = [column[0].title() for column in cur2.description]
        for r in cur2:
            h = {""+columns[0]+"":r[0],""+columns[1]+"":r[1]}
            centers.append(h)
        cur2.close()
        con.close()
        return centers
    def GetTrainersBasedOnCenter(center_id):
        trainers = []
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()
        cur2.execute("EXEC [masters].[sp_get_trainer_based_on_center] @center_id="+str(center_id))
        columns = [column[0].title() for column in cur2.description]
        for r in cur2:
            h = {""+columns[0]+"":r[0],""+columns[1]+"":r[1]}
            trainers.append(h)
        cur2.close()
        con.close()
        return trainers
    def GetTrainersBasedOnSubProject(sub_project_id):
        trainers = []
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()
        cur2.execute("EXEC [masters].[sp_get_trainer_based_on_sub_project] @sub_project_id="+str(sub_project_id))
        columns = [column[0].title() for column in cur2.description]
        j=0
        for r in cur2:
            j+=1
            h = {""+columns[0]+"":r[0],""+columns[1]+"":r[1]}
            trainers.append(h)
        trainers_f={"Trainers":trainers, "Is_Ojt":r[2] if (j>0) else 0}
        cur2.close()
        con.close()
        return trainers_f
    def GetCenterManagerBasedOnCenter(center_id):
        centermanager = []
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()
        cur2.execute("EXEC [masters].[sp_get_center_manager_based_on_center] @center_id="+center_id)
        columns = [column[0].title() for column in cur2.description]
        for r in cur2:
            h = {""+columns[0]+"":r[0],""+columns[1]+"":r[1]}
            centermanager.append(h)
        cur2.close()
        con.close()
        return centermanager
    def GetSubCenterBasedOnCenter(center_id):
        subcenter = []
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()
        cur2.execute("Select * from masters.tbl_center where main_center_id=" + center_id + "AND is_active=1;")
        columns = [column[0].title() for column in cur2.description]
        for r in cur2:
            h = {""+columns[0]+"":r[0],""+columns[1]+"":r[1]}
            subcenter.append(h)
        cur2.close()
        con.close()
        return subcenter

    def candidates_based_on_course(candidate_id,course_ids,batch_id,center_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        content = {}
        d = []
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [candidate_details].[sp_get_candidate_based_on_course] ?, ?,?, ?, ?, ?, ?, ?, ?'
        values = (candidate_id,course_ids,batch_id,center_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        record="0"
        fil="0"
        for row in cur:
            record=row[11]
            fil=row[10]
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[3]+"":row[3],""+columns[4]+"":row[4],""+columns[5]+"":row[5],""+columns[6]+"":row[6],""+columns[7]+"":row[7],""+columns[8]+"":row[8],""+columns[9]+"":row[9]}
            d.append(h)
        content = {"draw":draw,"recordsTotal":record,"recordsFiltered":fil,"data":d}
        cur.close()
        con.close()
        return content

    def candidate_maped_in_batch(candidate_id,course_ids,batch_id,center_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        content = {}
        d = []
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [candidate_details].[sp_get_candidate_maped_in_batch] ?, ?,?, ?, ?, ?, ?, ?, ?'
        values = (candidate_id,course_ids,batch_id,center_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        record="0"
        fil="0"
        for row in cur:
            record=row[11]
            fil=row[10]
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[3]+"":row[3],""+columns[4]+"":row[4],""+columns[5]+"":row[5],""+columns[6]+"":row[6],""+columns[7]+"":row[7],""+columns[8]+"":row[8],""+columns[9]+"":row[9]}
            d.append(h)
        content = {"draw":draw,"recordsTotal":record,"recordsFiltered":fil,"data":d}
        cur.close()
        con.close()
        return content
    def candidate_enrolled_in_batch(batch_id,assessment_id,candidate_id):
        h = {}
        response = []
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [candidate_details].[sp_get_candidate_enrolled_in_batch] ?,?,?'
       
        values = (batch_id,assessment_id,candidate_id)
        print(values)
        cur.execute(sql,(values))
        #print(values)
        #print(cur2.description)
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            for i in range(len(columns)):
                h[columns[i]]=row[i]           
            response.append(h.copy())
        cur.close()
        con.close()
        #print(response)
        return response
  
    def add_edit_map_candidate_batch(candidate_ids,batch_id,course_id,user_id):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec	[candidate_details].[add_edit_map_candidate_batch] ?, ?, ?, ?'
        values = (candidate_ids,batch_id,course_id,user_id)
        cur.execute(sql,(values))
        for row in cur:
            pop=row[1]
        cur.commit()
        cur.close()
        con.close()
        if pop ==1:
            msg={"message":"Candidate Updation"}
        else:
            msg={"message":"Candidate Mapping"}
        return msg

    def drop_edit_map_candidate_batch(skilling_ids,batch_id,course_id,user_id,drop_remark):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec	[candidate_details].[drop_edit_map_candidate_batch] ?, ?, ?, ?, ?'
        values = (skilling_ids,batch_id,course_id,user_id,drop_remark)
        cur.execute(sql,(values))
        for row in cur:
            pop=row[1]
        cur.commit()
        cur.close()
        con.close()
        if pop ==1:
            msg={"message":"Candidate(s) Dropped"}
        else:
            msg={"message":"Error fetching batch data for Droping"}
        return msg
    def tag_sponser_candidate(skilling_ids,sponser_ids,user_id):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec	[candidate_details].[tag_sponser_candidate] ?, ?, ?'
        values = (skilling_ids,sponser_ids,user_id)
        cur.execute(sql,(values))
        for row in cur:
            pop=row[1]
        cur.commit()
        cur.close()
        con.close()
        if pop ==1:
            msg={"message":"Candidate(s) tagged to sponsor"}
        else:
            msg={"message":"Error in tagging"}
        return msg
    
    def untag_users_from_sub_project(user_ids,sub_project_id):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec	[masters].[untag_users_from_sub_project] ?, ?'
        values = (user_ids,sub_project_id)
        cur.execute(sql,(values))
        for row in cur:
            pop=row[1]
        cur.commit()
        cur.close()
        con.close()
        if pop ==1:
            msg={"message":"User Untagged"}
        else:
            msg={"message":"Error in untagging"}
        return msg
    def tag_users_from_sub_project(user_id,sub_project_id,tagged_by):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec	[masters].[tag_users_from_sub_project] ?, ?, ?'
        values = (user_id,sub_project_id,tagged_by)
        cur.execute(sql,(values))
        for row in cur:
            pop=row[1]
        cur.commit()
        cur.close()
        con.close()
        if pop ==1:
            msg={"message":"User tagged"}
        else:
            msg={"message":"Error in tagging"}
        return msg
    def cancel_planned_batch(user_id,planned_batch_code,cancel_reason):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'UPDATE [masters].[tbl_planned_batches] SET is_cancelled=1 ,cancel_reason= ? where planned_batch_code=?'
        values = (cancel_reason,planned_batch_code)
        cur.execute(sql,(values))
        cur.commit()
        cur.close()
        con.close()
        msg={"message":"Batch Cancelled"}
        return msg
    def cancel_actual_batch(user_id,actual_batch_id,cancel_reason):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'UPDATE [batches].[tbl_batches] SET is_cancelled=1 ,cancel_reason= ? ,planned_batch_id=Null where batch_id=?'
        sql2 = 'update candidate_details.tbl_map_candidate_intervention_skilling set is_dropped=1,dropped_reason=?,dropped_date=getdate() where batch_id=?'
        values = (cancel_reason,actual_batch_id)
        cur.execute(sql,(values))
        cur.execute(sql2,(values))
        cur.commit()
        cur.close()
        con.close()
        msg={"message":"Batch Cancelled"}
        return msg
    def upload_assessment_certificate_copy(certi_name,user_id,enrolment_id,batch_id):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = '''update assessments.tbl_map_certification_candidates_stages 
                set certificate_copy=? ,
                created_by=?
                where intervention_value=? and assessment_id=(select TOP(1) assessment_id 
                                                            from assessments.tbl_batch_assessments
                                                            where batch_id=? and assessment_type_id=2
                                                            and assessment_stage_id=4
                                                            and is_active=1
                                                            order by assessment_id desc
                                                            )
                AND is_active=1;'''
        values = (certi_name,user_id,enrolment_id,batch_id)
        cur.execute(sql,(values))
        cur.commit()
        cur.close()
        con.close()
        msg={"Status":True,"message":"Certificate Uploaded"}
        return msg
    def upload_assessment_certificate_copy_bulk_upload(certi_name,user_id,enrolment_id,batch_id):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = '''update assessments.tbl_map_certification_candidates_stages 
                set certificate_copy=? ,
                created_by=?,
                created_on=getdate()
                where intervention_value in  (	
								select	value 
								from	string_split( ?,',')
								where	trim(value)!=''
								)
                and assessment_id=(select TOP(1) assessment_id 
                                                            from assessments.tbl_batch_assessments
                                                            where batch_id=? and assessment_type_id=2
                                                            and assessment_stage_id=4
                                                            and is_active=1
                                                            order by assessment_id desc
                                                            )
                AND is_active=1;'''
        values = (certi_name,user_id,enrolment_id,batch_id)
        cur.execute(sql,(values))
        cur.commit()
        cur.close()
        con.close()
        msg={"Status":True,"message":"Certificate Uploaded"}
        return msg
    
    def upload_cerification_cand_image(certi_name,user_id,enrolment_id,batch_id):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = '''update assessments.tbl_map_certification_candidates_stages 
                set uploaded_cand_image=? ,
                created_by=?
                where intervention_value=? and assessment_id=(select TOP(1) assessment_id 
                                                            from assessments.tbl_batch_assessments
                                                            where batch_id=? and assessment_type_id=2
                                                            and assessment_stage_id=4
                                                            and is_active=1
                                                            order by assessment_id desc
                                                            )
                AND is_active=1;'''
        values = (certi_name,user_id,enrolment_id,batch_id)
        cur.execute(sql,(values))
        cur.commit()
        cur.close()
        con.close()
        msg={"Status":True,"message":"Image Uploaded"}
        return msg
    
    def upload_cerification_batch_image(file_name,user_id,batch_id):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = '''update assessments.tbl_batch_assessments 
                set batch_image=? ,
                created_by=?
                where assessment_id=(select TOP(1) assessment_id 
                                                            from assessments.tbl_batch_assessments
                                                            where batch_id=? and assessment_type_id=2
                                                            and assessment_stage_id=4
                                                            and is_active=1
                                                            order by assessment_id desc
                                                            )
                AND is_active=1;'''
        values = (file_name,user_id,batch_id)
        cur.execute(sql,(values))
        cur.commit()
        cur.close()
        con.close()
        msg={"Status":True,"message":"Image Uploaded"}
        return msg
    
    def tag_user_roles(login_user_id,user_id,neo_role,jobs_role,crm_role):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec	[users].[sp_tag_user_roles] ?, ?, ?,?,?'
        values = (login_user_id,user_id,neo_role,jobs_role,crm_role)
        cur.execute(sql,(values))
        for row in cur:
            pop=row[0]
        cur.commit()
        cur.close()
        con.close()
        if pop ==1:
            msg={"message":"Success"}
        else:
            msg={"message":"Updation Error"}
        return msg
    def qp_list(user_id,user_role_id,qp_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw, sectors):
        content = {}
        d = []
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [masters].[sp_get_qp_list] ?,?,?, ?, ?, ?, ?, ?, ?'
        values = (user_id,user_role_id,qp_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction, sectors)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        record="0"
        fil="0"
        for row in cur:
            record=row[8]
            fil=row[7]
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[3]+"":row[3],""+columns[4]+"":row[4],""+columns[5]+"":row[5],""+columns[6]+"":row[6]}
            d.append(h)
        content = {"draw":draw,"recordsTotal":record,"recordsFiltered":fil,"data":d}
        cur.close()
        con.close()
        return content
    def add_qp_details(qp_name,qp_code,user_id,is_active,qp_id,sector):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec	masters.sp_add_edit_qp ?, ?, ?, ?, ?,?'
        values = (qp_id,qp_name,qp_code,user_id,is_active,sector)
        cur.execute(sql,(values))
        for row in cur:
            pop=row[1]
        cur.commit()
        cur.close()
        con.close()
        if pop ==1:
            msg={"message":"Updated Successfully","qp_flag":1}
        else: 
                if pop==0:
                    msg={"message":"Created Successfully","qp_flag":0}
                else:
                    if pop==2:
                        msg={"message":"Qualification Pack with the Qualification code already exists","qp_flag":2}
        return msg
    def get_qp_details(glob_qp_id):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'SELECT * FROM [masters].[tbl_qp] where qp_id=?'
        values = (glob_qp_id,)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[4]+"":row[4],""+columns[5]+"":row[5],""+columns[10]+"":row[10]}
        cur.close()
        con.close()
        return h

    def candidate_list(candidate_id,customer,project,sub_project,batch,region,center,center_type,status,user_id,user_role_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw, Contracts, candidate_stage, from_date, to_date):
        content = {}
        d = []
        h={}
        
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [candidate_details].[sp_get_candidate_web_list_new] ?, ?, ?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?,?,?,?,?,?'
        values = (candidate_id,customer,project,sub_project,batch,region,center,center_type,status,user_id,user_role_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,Contracts, candidate_stage, from_date, to_date)
        print(values)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        record="0"
        fil="0"
        for row in cur:
            record=row[len(columns)-1]
            fil=row[len(columns)-2]
            for i in range(len(columns)-2):                
                h[columns[i]]=row[i] if row[i]!=None else 'NA'
            d.append(h.copy())            
        content = {"draw":draw,"recordsTotal":record,"recordsFiltered":fil,"data":d}
        cur.close()
        con.close()
        return content
    def user_sub_project_list(customer,project,sub_project,region,user_id,user_role_id,employee_status,sub_project_status,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        content = {}
        d = []
        h={}
        
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [reports].[sp_get_user_sub_project_report] ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?'
        values = (customer,project,sub_project,region,user_id,user_role_id,employee_status,sub_project_status,start_index,page_length,search_value,order_by_column_position,order_by_column_direction)
        #print(values)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        record="0"
        fil="0"
        for row in cur:
            record=row[len(columns)-1]
            fil=row[len(columns)-2]
            for i in range(len(columns)-2):                
                h[columns[i]]=row[i] if row[i]!=None else 'NA'
            d.append(h.copy())            
        content = {"draw":draw,"recordsTotal":record,"recordsFiltered":fil,"data":d}
        cur.close()
        con.close()
        return content
           
    def mobilized_list(candidate_id,region_ids, state_ids, MinAge, MaxAge, user_id, user_role_id, start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw,created_by,FromDate, ToDate):
        content = {}
        d = []
        h={}
        
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [candidate_details].[sp_get_candidate_web_list_new_M] ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?'
        values = (candidate_id,region_ids, state_ids, MinAge, MaxAge, user_id, user_role_id, start_index,page_length,search_value,order_by_column_position,order_by_column_direction,created_by,FromDate, ToDate)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        record="0"
        fil="0"
        for row in cur:
            record=row[len(columns)-1]
            fil=row[len(columns)-2]
            for i in range(len(columns)-2):                
                h[columns[i]]=row[i] if row[i]!=None else 'NA'
            d.append(h.copy())            
        content = {"draw":draw,"recordsTotal":record,"recordsFiltered":fil,"data":d}
        cur.close()
        con.close()
        return content

    def registered_list(candidate_id,region_ids, state_ids, Pincode, created_by, FromDate, ToDate, user_id, user_role_id, start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        content = {}
        d = []
        h={}
        
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [candidate_details].[sp_get_candidate_web_list_new_R] ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?'
        values = (candidate_id,region_ids, state_ids, Pincode, created_by, FromDate, ToDate, user_id, user_role_id, start_index,page_length,search_value,order_by_column_position,order_by_column_direction)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        record="0"
        fil="0"
        for row in cur:
            record=row[len(columns)-1]
            fil=row[len(columns)-2]
            for i in range(len(columns)-2):                
                h[columns[i]]=row[i] if row[i]!=None else 'NA'
            d.append(h.copy())            
        content = {"draw":draw,"recordsTotal":record,"recordsFiltered":fil,"data":d}
        cur.close()
        con.close()
        return content
    
    def enrolled_list(candidate_id,region_ids, state_ids, Pincode, created_by, FromDate, ToDate, user_id, user_role_id, start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        content = {}
        d = []
        h={}
        
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [candidate_details].[sp_get_candidate_web_list_new_E] ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?'
        values = (candidate_id,region_ids, state_ids, Pincode, created_by, FromDate, ToDate, user_id, user_role_id, start_index,page_length,search_value,order_by_column_position,order_by_column_direction)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        record="0"
        fil="0"
        for row in cur:
            record=row[len(columns)-1]
            fil=row[len(columns)-2]
            for i in range(len(columns)-2):                
                h[columns[i]]=row[i] if row[i]!=None else 'NA'
            d.append(h.copy())            
        content = {"draw":draw,"recordsTotal":record,"recordsFiltered":fil,"data":d}
        cur.close()
        con.close()
        return content

    def get_project_basedon_client(client_id):
        project = []
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()
        cur2.execute("SELECT * FROM masters.tbl_projects WHERE client_id="+client_id)
        columns = [column[0].title() for column in cur2.description]
        for r in cur2:
            h = {""+columns[0]+"":r[0],""+columns[1]+"":r[1]}
            project.append(h)
        cur2.close()
        con.close()
        return project
    def get_cand_course_basedon_proj(project_id):
        courses = []
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()
        
        cur2.execute("SELECT * FROM masters.tbl_courses WHERE project_id="+project_id)
        columns = [column[0].title() for column in cur2.description]
        for r in cur2:
            h = {""+columns[0]+"":r[0],""+columns[1]+"":r[1]}
            courses.append(h)
        cur2.close()
        con.close()
        return courses

    def get_cand_course_basedon_proj_multiple(project_id):
        courses = []
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()

        sql = """SELECT distinct * FROM masters.tbl_courses WHERE is_active=1 and is_deleted=0 and ('{}'='-1' or project_id in (select value from string_split('{}',',') where trim(value)!=''))""".format(project_id, project_id)  #'{}'='' or 
        cur2.execute(sql)
        columns = [column[0].title() for column in cur2.description]
        for r in cur2:
            h = {""+columns[0]+"":r[0],""+columns[1]+"":r[1]}
            courses.append(h)
        cur2.close()
        con.close()
        return courses

    def get_cand_center_basedon_course(course_id):
        center = []
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()
        cur2.execute("SELECT cen.center_id,cen.center_name FROM masters.tbl_center As cen LEFT JOIN masters.tbl_map_course_center As map on map.center_id=cen.center_id WHERE map.course_id="+course_id)
        columns = [column[0].title() for column in cur2.description]
        for r in cur2:
            h = {""+columns[0]+"":r[0],""+columns[1]+"":r[1]}
            center.append(h)
        cur2.close()
        con.close()
        return center
    def get_cand_center_basedon_course_multiple(user_id,user_role_id,course_id, RegionId):
        center = []
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()
        sql = """SELECT distinct cen.center_id,cen.center_name FROM masters.tbl_center As cen left join masters.tbl_states as st on st.state_id=cen.state_id where cen.is_active=1 and cen.is_deleted=0 and ('{}'='-1' or '{}'='' or st.region_id in (select value from string_split('{}',',') where trim(value)!=''))""".format(RegionId, RegionId, RegionId)
        cur2.execute(sql)
        columns = [column[0].title() for column in cur2.description]
        for r in cur2:
            h = {""+columns[0]+"":r[0],""+columns[1]+"":r[1]}
            center.append(h)
        cur2.close()
        con.close()
        return center
    def get_section_for_cand():
        section=[]
        con = pyodbc.connect(conn_str)
        cur=con.cursor()
        cur.execute("EXEC content.[sp_get_sections for cand_neo]")
        columns = [column[0].title() for column in cur.description]
        for r in cur:
            h = {""+columns[0]+"":r[0],""+columns[1]+"":r[1]}
            section.append(h)
        cur.close()
        con.close()
        return section

    def client_list(user_id,user_role_id,client_id,Is_Active,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw, funding_sources,customer_groups,category_type_ids):
        content = {}
        d = []
        h={}
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [masters].[sp_get_client_list] ?,?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?'
        values = (user_id,user_role_id,client_id,Is_Active, funding_sources,customer_groups,category_type_ids,start_index,page_length,search_value,order_by_column_position,order_by_column_direction)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        record="0"
        fil="0"
        for row in cur:
            record=row[len(columns)-1]
            fil=row[len(columns)-2]
            for i in range(len(columns)-2):
                h[columns[i]]=row[i]
            #h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[3]+"":row[3],""+columns[4]+"":row[4],""+columns[5]+"":row[5],""+columns[6]+"":row[6]}
            d.append(h.copy())
        content = {"draw":draw,"recordsTotal":record,"recordsFiltered":fil,"data":d}
        cur.close()
        con.close()
        return content
    def add_client_details(client_name,client_code,user_id,is_active,client_id,FundingSource, CustomerGroup, IndustryType, CategoryType, POC_details):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec	[masters].[sp_add_edit_client] ?, ?, ?, ?, ?, ?, ?, ?, ?, ?'
        values = (client_name,client_code,user_id,is_active,client_id,FundingSource, CustomerGroup, IndustryType, CategoryType, POC_details)
        cur.execute(sql,(values))
        for row in cur:
            pop=row[1]
        cur.commit()
        cur.close()
        con.close()
        if pop ==1:
            msg={"message":"Updated Successfully","client_flag":1}
        else: 
                if pop==0:
                    msg={"message":"Created Successfully","client_flag":0}
                else:
                    if pop==2:
                        msg={"message":"Customer with the Customer code already exists","client_flag":2}
        return msg

    def get_client_detail(glob_client_id):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'select customer_name,customer_code,is_active,funding_source_id,customer_group_id,industry_type_id,category_type_id from masters.tbl_customer where customer_id=?'
        values = (glob_client_id,)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[3]+"":row[3],""+columns[4]+"":row[4],""+columns[5]+"":row[5],""+columns[6]+"":row[6]}
        cur.close()
        con.close()
        return h
    
    def get_contarct_detail(glob_contract_id):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = "select contract_name, contract_code, coalesce(customer_id,'') as customer_id, coalesce(entity_id,'') as entity_id, coalesce(sales_category_id,'') as sales_category_id, coalesce(cast(start_date as varchar(MAX)),'') as start_date, coalesce(cast(end_date as varchar(MAX)),'') as end_date, is_active, coalesce(value,'') as value, coalesce(sales_manager_id,'') as sales_manager_id  from masters.tbl_contract where contract_id=?"
        values = (glob_contract_id,)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        h={}
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[3]+"":row[3],""+columns[4]+"":row[4],""+columns[5]+"":row[5],""+columns[6]+"":row[6],""+columns[7]+"":row[7],""+columns[8]+"":row[8],""+columns[9]+"":row[9]}
        cur.close()
        con.close()
        return h

    def add_contract_details(ContractName, ContractCode, ClientName, EntityName, SalesCatergory, StartDate, EndDate, SalesManager, ContractValue, isactive, user_id, contract_id):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec	[masters].[sp_add_edit_contract] ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?'
        values = (ContractName, ContractCode, ClientName, EntityName, SalesCatergory, StartDate, EndDate, SalesManager, ContractValue, isactive, user_id, contract_id)
        cur.execute(sql,(values))
        for row in cur:
            pop=row[1]
        cur.commit()
        cur.close()
        con.close()
        if pop ==1:
            msg={"message":"Updated Successfully","client_flag":1}
        else: 
                if pop==0:
                    msg={"message":"Created Successfully","client_flag":0}
                else:
                    if pop==2:
                        msg={"message":"Customer with the Customer code already exists","client_flag":2}
        return msg

    def get_contract_detail(glob_client_id):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'select customer_name,customer_code,is_active,funding_source_id,customer_group_id,industry_type_id,category_type_id from masters.tbl_customer where customer_id=?'
        values = (glob_client_id,)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[3]+"":row[3],""+columns[4]+"":row[4],""+columns[5]+"":row[5],""+columns[6]+"":row[6]}
        cur.close()
        con.close()
        return h

    def region_list(region_id,user_id,user_role_id,user_region_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        content = {}
        d = []
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [masters].[sp_get_region_list] ?, ?, ?, ?, ?, ?, ?, ?, ?'
        values = (region_id,user_id,user_role_id,user_region_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        record="0"
        fil="0"
        for row in cur:
            record=row[7]
            fil=row[6]
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[3]+"":row[3],""+columns[4]+"":row[4],""+columns[5]+"":row[5]}
            d.append(h)
        content = {"draw":draw,"recordsTotal":record,"recordsFiltered":fil,"data":d}
        cur.close()
        con.close()
        return content
    def add_region_details(region_name,region_code,user_id,is_active,region_id):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec	[masters].[sp_add_edit_region] ?, ?, ?, ?, ?'
        values = (region_name,region_code,user_id,is_active,region_id)
        cur.execute(sql,(values))
        for row in cur:
            pop=row[1]
        cur.commit()
        cur.close()
        con.close()
        if pop ==1:
            msg={"message":"Updated Successfully","region_flag":1}
        else: 
                if pop==0:
                    msg={"message":"Created Successfully","region_flag":0}
                else:
                    if pop==2:
                        msg={"message":"Region with the Region code already exists","region_flag":2}
        return msg
    def get_region_detail(glob_region_id):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'SELECT * FROM [masters].[tbl_region] where region_id=?'
        values = (glob_region_id,)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[3]+"":row[3],""+columns[5]+"":row[5]}
        cur.close()
        con.close()
        return h
        
    def cluster_list(cluster_id,user_id,user_role_id,user_region_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        content = {}
        d = []
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [masters].[sp_get_cluster_list] ?, ?, ?, ?, ?, ?, ?, ? ,?'
        values = (cluster_id,user_id,user_role_id,user_region_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        record="0"
        fil="0"
        for row in cur:
            record=row[8]
            fil=row[7]
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[3]+"":row[3],""+columns[4]+"":row[4],""+columns[5]+"":row[5],""+columns[6]+"":row[6]}
            d.append(h)
        content = {"draw":draw,"recordsTotal":record,"recordsFiltered":fil,"data":d}
        cur.close()
        con.close()
        return content
    def add_cluster_details(cluster_name,cluster_code,region_id,user_id,is_active,cluster_id):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec	[masters].[sp_add_edit_cluster] ?, ?, ?, ?, ?, ?'
        values = (cluster_name,cluster_code,region_id,user_id,is_active,cluster_id)
        cur.execute(sql,(values))
        for row in cur:
            pop=row[1]
        cur.commit()
        cur.close()
        con.close()
        if pop ==1:
            msg={"message":"Updated Successfully","cluster_flag":1}
        else: 
                if pop==0:
                    msg={"message":"Created Successfully","cluster_flag":0}
                else:
                    if pop==2:
                        msg={"message":"Cluster with the Cluster code already exists","cluster_flag":2}
        return msg
    def get_cluster_detail(glob_cluster_id):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'SELECT * FROM [masters].[tbl_cluster] where cluster_id=?'
        values = (glob_cluster_id,)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[3]+"":row[3],""+columns[4]+"":row[4],""+columns[6]+"":row[6]}
        cur.close()
        con.close()
        return h
    def get_all_Region():
        region = []
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'SELECT region_id, region_name, region_code, created_by, ref_region_id, is_deleted FROM [masters].[tbl_region] where is_active=1;'
        cur.execute(sql)
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1]}
            region.append(h)
        cur.close()
        con.close()
        return region

    def question_type_list(question_type_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        content = {}
        d = []
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [content].[sp_get_question_type_list] ?, ?, ?, ?, ?, ?'
        values = (question_type_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        record="0"
        fil="0"
        for row in cur:
            record=row[6]
            fil=row[5]
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[3]+"":row[3],""+columns[4]+"":row[4]}
            d.append(h)
        content = {"draw":draw,"recordsTotal":record,"recordsFiltered":fil,"data":d}
        cur.close()
        con.close()
        return content
    def add_question_type_details(question_type_name,user_id,is_active,question_type_id):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec	[content].[sp_add_edit_question_type] ?, ?, ?, ?'
        values = (question_type_name,user_id,is_active,question_type_id)
        cur.execute(sql,(values))
        for row in cur:
            pop=row[1]
        cur.commit()
        cur.close()
        con.close()
        if pop ==1:
            msg={"message":"Updated"}
        else:
            msg={"message":"Created"}
        return msg
    def get_question_type_details(glob_question_type_id):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'SELECT * FROM [masters].[tbl_question_type] where question_type_id=?'
        values = (glob_question_type_id,)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[3]+"":row[3],""+columns[4]+"":row[4]}
        cur.close()
        con.close()
        return h
   
    def section_type_list(section_type_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        content = {}
        d = []
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [content].[sp_get_section_type_list] ?, ?, ?, ?, ?, ?'
        values = (section_type_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        record="0"
        fil="0"
        for row in cur:
            record=row[6]
            fil=row[5]
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[3]+"":row[3],""+columns[4]+"":row[4]}
            d.append(h)
        content = {"draw":draw,"recordsTotal":record,"recordsFiltered":fil,"data":d}
        cur.close()
        con.close()
        return content
    def add_section_type_details(section_type_name,user_id,is_active,section_type_id):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec	[content].[sp_add_edit_section_type] ?, ?, ?, ?'
        values = (section_type_name,user_id,is_active,section_type_id)
        cur.execute(sql,(values))
        for row in cur:
            pop=row[1]
        cur.commit()
        cur.close()
        con.close()
        if pop ==1:
            msg={"message":"Updated"}
        else:
            msg={"message":"Created"}
        return msg
    def get_section_type_details(glob_section_type_id):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'SELECT * FROM [content].[tbl_section_type] where section_type_id=?'
        values = (glob_section_type_id,)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[3]+"":row[3],""+columns[4]+"":row[4]}
        cur.close()
        con.close()
        return h

    def section_list(section_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        content = {}
        d = []
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [content].[sp_get_section_list] ?, ?, ?, ?, ?, ?'
        values = (section_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        record="0"
        fil="0"
        for row in cur:
            record=row[8]
            fil=row[7]
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[3]+"":row[3],""+columns[4]+"":row[4],""+columns[5]+"":row[5],""+columns[6]+"":row[6]}
            d.append(h)
        content = {"draw":draw,"recordsTotal":record,"recordsFiltered":fil,"data":d}
        cur.close()
        con.close()
        return content
    def add_section_details(section_name,section_type_id,p_section,user_id,is_active,section_id):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec	[content].[sp_add_edit_section] ?, ?, ?, ?, ?, ?'
        values = (section_name,section_type_id,p_section,user_id,is_active,section_id)
        cur.execute(sql,(values))
        for row in cur:
            pop=row[1]
        cur.commit()
        cur.close()
        con.close()
        if pop ==1:
            msg={"message":"Updated"}
        else:
            msg={"message":"Created"}
        return msg
    def get_section_details(glob_section_id):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'SELECT * FROM [content].[tbl_section] where section_id=?'
        values = (glob_section_id,)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[4]+"":row[4],""+columns[5]+"":row[5],""+columns[6]+"":row[6]}
        cur.close()
        con.close()
        return h
    def all_section_types():
        sec_type=[]
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'SELECT * FROM [content].[tbl_section_type] where is_active=1'
        cur.execute(sql)
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1]}
            sec_type.append(h)
        cur.close()
        con.close()
        return sec_type
    def all_parent_section():
        sec = []
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'SELECT * FROM [content].[tbl_section] where is_active=1'
        cur.execute(sql)
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1]}
            sec.append(h)
        cur.close()
        con.close()
        return sec
    
    # def state_and_district_list(state_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
    #     content = {}
    #     d = []
    #     con = pyodbc.connect(conn_str)
    #     cur = con.cursor()
    #     sql = 'exec [content].[sp_get_section_list] ?, ?, ?, ?, ?, ?'
    #     values = (state_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction)
    #     cur.execute(sql,(values))
    #     columns = [column[0].title() for column in cur.description]
    #     record="0"
    #     fil="0"
    #     for row in cur:
    #         record=row[8]
    #         fil=row[7]
    #         h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[3]+"":row[3],""+columns[4]+"":row[4],""+columns[5]+"":row[5],""+columns[6]+"":row[6]}
    #         d.append(h)
    #     content = {"draw":draw,"recordsTotal":record,"recordsFiltered":fil,"data":d}
    #     cur.close()
    #     con.close()
    #     return content

    
    def sub_center_list(sub_center_id,parent_center_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        content = {}
        d = []
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [masters].[sp_get_sub_center_list] ?, ?, ?, ?, ?, ?, ?'
        values = (sub_center_id,parent_center_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        record="0"
        fil="0"
        for row in cur:
            record=row[8]
            fil=row[7]
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[3]+"":row[3],""+columns[4]+"":row[4],""+columns[5]+"":row[5],""+columns[6]+"":row[6]}
            d.append(h)
        content = {"draw":draw,"recordsTotal":record,"recordsFiltered":fil,"data":d}
        cur.close()
        con.close()
        return content
    def add_sub_center_details(sub_center_name,sub_center_loc,parent_center_id,user_id,is_active,sub_center_id):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec	[masters].[sp_add_edit_sub_center] ?, ?, ?, ?, ?, ?'
        values = (sub_center_name,sub_center_loc,parent_center_id,user_id,is_active,sub_center_id)
        cur.execute(sql,(values))
        for row in cur:
            pop=row[1]
        cur.commit()
        cur.close()
        con.close()
        if pop ==1:
            msg={"message":"Updated"}
        else:
            msg={"message":"Created"}
        return msg
    def get_sub_center_detail(glob_sub_center_id):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'SELECT center_id,center_name,main_center_id,created_by,created_on,is_active,location FROM [masters].[tbl_center] where center_id=?'
        values = (glob_sub_center_id,)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[3]+"":row[3],""+columns[5]+"":row[5],""+columns[6]+"":row[6]}
        cur.close()
        con.close()
        return h
    
    def all_session_plan(course_id):
        sessionplans = []
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'SELECT sp.session_plan_id, sp.session_plan_name FROM [content].[tbl_session_plans] AS sp LEFT JOIN [content].[tbl_map_session_plan_course] AS map ON map.session_plan_id=sp.session_plan_id where map.course_id=?'
        values= (course_id,)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1]}
            sessionplans.append(h)
        cur.close()
        con.close()
        return sessionplans
    def all_module(session_plan_id):
        modules = []
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'SELECT module_id, module_name FROM [content].[tbl_modules] where session_plan_id=?'
        values= (session_plan_id,)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1]}
            modules.append(h)
        cur.close()
        con.close()
        return modules
    def module_order_for_session_plan(session_plan_id):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'SELECT MAX(module_order) FROM [content].[tbl_modules] where session_plan_id=?'
        values= (session_plan_id,)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h=row[0]
        cur.close()
        con.close()
        return h
    def get_session_order_for_module(module_id):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'SELECT MAX(session_order) FROM [content].[tbl_sessions] where module_id=?'
        values= (module_id,)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h=row[0]
        cur.close()
        con.close()
        return h
    def sessioncode_for_module(module_id):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'SELECT code FROM [content].[tbl_modules] where module_id=?'
        values= (module_id,)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h=row[0]
        cur.close()
        con.close()
        return h
    def module_session_list(session_id,module_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        content = {}
        d = []
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [content].[sp_get_module_session_list] ?, ?, ?, ?, ?, ?, ?'
        values = (session_id,module_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        record="0"
        fil="0"
        for row in cur:
            record=row[9]
            fil=row[8]
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[3]+"":row[3],""+columns[4]+"":row[4],""+columns[5]+"":row[5],""+columns[6]+"":row[6],""+columns[7]+"":row[7]}#,""+columns[12]+"":row[12],""+columns[14]+"":row[14]}
            d.append(h)
        content = {"draw":draw,"recordsTotal":record,"recordsFiltered":fil,"data":d}
        cur.close()
        con.close()
        return content
    def add_session_plan(session_plan_name,session_plan_duration,course_id,user_id,is_active,session_plan_id):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec	[content].[sp_add_edit_session_plan] ?, ?, ?, ?, ?, ?'
        values = (session_plan_name,session_plan_duration,course_id,user_id,is_active,session_plan_id)
        cur.execute(sql,(values))
        for row in cur:
            pop=row[1]
        cur.commit()
        cur.close()
        con.close()
        if pop ==1:
            msg={"message":"Updated"}
        else:
            msg={"message":"Created"}
        return msg
    def add_module(module_name,module_code,module_order,session_plan_id,user_id,is_active,module_id):
        #print(module_name,module_code,module_order,session_plan_id,user_id,is_active,module_id)
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec	[content].[sp_add_edit_module] ?, ?, ?, ?, ?, ?, ?'
        values = (module_name,module_code,module_order,session_plan_id,user_id,is_active,module_id)
        cur.execute(sql,(values))
        for row in cur:
            pop=row[1]
        cur.commit()
        cur.close()
        con.close()
        if pop ==1:
            msg={"message":"Updated"}
        else:
            msg={"message":"Created"}
        return msg
    def add_edit_session(session_name,session_code,session_order,module_id,session_des,learning_out,learning_act,learning_aids,user_id,is_active,session_id,session_duration):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec	[content].[sp_add_edit_session] ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?'
        values = (session_name,session_code,session_order,module_id,session_des,learning_out,learning_act,learning_aids,user_id,is_active,session_id,session_duration)
        cur.execute(sql,(values))
        for row in cur:
            pop=row[1]
        cur.commit()
        cur.close()
        con.close()
        if pop ==1:
            msg={"message":"Updated"}
        else:
            msg={"message":"Created"}
        return msg
    def get_session_detail(session_id):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'SELECT * FROM [content].[tbl_sessions] where session_id=?'
        values = (session_id,)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[3]+"":row[3],""+columns[4]+"":row[4],""+columns[5]+"":row[5],""+columns[6]+"":row[6],""+columns[7]+"":row[7],""+columns[8]+"":row[8],""+columns[9]+"":row[9],""+columns[10]+"":row[10],""+columns[11]+"":row[11],""+columns[13]+"":row[13]}
        cur.close()
        con.close()
        return h
    ###########################################3  TMA BATCH

    @classmethod
    def get_trainer_data_db(cls):
        con = pyodbc.connect(conn_str)
        curs = con.cursor()

        
        quer = """
                                        SELECT	 trainer_name + ' (' + trainer_email + ')' AS trainer_name,
							 trainer_email
					FROM	 tma.tbl_trainers
					WHERE	 is_active=1
					ORDER BY trainer_name
        """
        quer = """

        /****** Script for SelectTopNRows command from SSMS  ******/
SELECT first_name + last_name  + ' (' + email + ')' AS trainer_name,
		email
  FROM [users].[tbl_user_details] as T
  LEFT JOIN users.tbl_users as U ON U.user_id = T.user_id
  where U.user_role_id = 7
  and U.is_active=1
  ORDER BY trainer_name
  

                                        
        """
        curs.execute(quer)
        data = curs.fetchall()
        curs.close()
        con.close()
        return data

    @classmethod
    def get_batch_list_count_db(cls, email_condition, batch_condition):
        con = pyodbc.connect(conn_str)
        curs = con.cursor()
        quer = """
WITH SCount AS
										(
										/****** Script for SelectTopNRows command from SSMS  ******/
										SELECT --count(S.[session_id]) as session_count 
												S.[session_id] as session_id
												,S.[module_id] as module_id
												,M.[session_plan_id] as session_plan_id
												,mp.[course_id] as course_id

										FROM [content].[tbl_sessions] as S
										left join [content].[tbl_modules] as M on S.module_id = M.module_id
										left join [content].[tbl_session_plans] as C on C.session_plan_id = M.session_plan_id
                                        left join content.tbl_map_session_plan_course AS mp on mp.session_plan_id=c.session_plan_id
										--where course_id=
										),
RES AS 
(
                            SELECT		DISTINCT 
										B.[batch_id],
										(TD.first_name + ' ' + TD.last_name) as trainer_name,
										TD.email as trainer_email,
										B.[batch_code],
										B.[start_date] as batch_start_date,
										B.[end_date] as batch_end_date,
										B.[batch_status],
										B.[is_active] as batch_active_status,
                                        CASE 
                                            WHEN CAST(UPPER(B.[end_date]) AS DATE) < CAST(GETDATE() AS DATE) THEN 1
                                            WHEN (CAST(GETDATE() AS DATE) BETWEEN CAST(UPPER(B.[start_date]) AS DATE) AND CAST(UPPER(B.[end_date]) AS DATE)) THEN 2
                                            WHEN CAST(UPPER(B.[start_date]) AS DATE) > CAST(GETDATE() AS DATE) THEN 3				
                                            ELSE 0
                                        END AS batch_stage_id,
                                        CASE 
                                            WHEN CAST(UPPER(B.[end_date]) AS DATE) < CAST(GETDATE() AS DATE) THEN 'Completed'
                                            WHEN (CAST(GETDATE() AS DATE) BETWEEN CAST(UPPER(B.[start_date]) AS DATE) AND CAST(UPPER(B.[end_date]) AS DATE)) THEN 'Ongoing'
                                            WHEN CAST(UPPER(B.[start_date]) AS DATE) > CAST(GETDATE() AS DATE) THEN 'Scheduled'
                                            ELSE 'Invalid'
                                        END AS batch_stage_name,
                                        B.[business_unit],
										
										Cen.center_name,
										CenT.[center_type_name] as center_type,
                                        (CONCAT(Cou.course_code, '-', Cou.course_name)) as course_name,
										CONCAT(Q.qp_code, '-', Q.qp_name) AS qp_name,
										Client.[client_name] as customer_name,
                                        CASE B.[image_required] WHEN 1 THEN 'Yes' ELSE 'No' END AS image_required,
										
										(SELECT COUNT(SC.session_id) FROM SCount AS SC WHERE SC.course_id=B.course_id) AS session_count	


                            FROM		                        [batches].[tbl_batches] as B
							left join	[users].[tbl_user_details] as TD on TD.user_id = B.trainer_id
							left join   [masters].[tbl_courses] as Cou on Cou.course_id = B.course_id
							left join	[masters].[tbl_qp] as Q on Q.qp_id = B.qp_id
							left join	[masters].[tbl_center] as Cen on Cen.center_id = B.center_id
							left join	[masters].[tbl_center_type] as CenT on CenT.[center_type_id] = Cen.center_type_id
							left join	[masters].[tbl_projects] as Pro on Pro.project_id = Cou.project_id
							left join	[masters].[tbl_client] as Client on Client.client_id = Pro.client_id 
							
							WHERE		1=1 {}
                            AND			UPPER(B.[start_date]) NOT IN ('NULL','00-JAN-1900') 
                            AND			UPPER(B.[end_date]) NOT IN ('NULL','00-JAN-1900')
                            AND	 		B.is_active=1
                            AND			UPPER(B.batch_status)='BATCH OPEN'
                        )
                      SELECT COUNT(batch_id) AS total_record_count
                        FROM RES 
                        WHERE 1=1
                        {}
                        
""".format(email_condition, batch_condition)
        curs.execute(quer)
        data = curs.fetchall()
        curs.close()
        con.close()
        return data


    @classmethod
    def getfilter_batch_list_count_db(cls, email_condition, batch_condition, search_condition):
        con = pyodbc.connect(conn_str)
        curs = con.cursor()


        quer = """
WITH SCount AS
										(
										/****** Script for SelectTopNRows command from SSMS  ******/
										SELECT --count(S.[session_id]) as session_count 
												S.[session_id] as session_id
												,S.[module_id] as module_id
												,M.[session_plan_id] as session_plan_id
												,mp.[course_id] as course_id

										FROM [content].[tbl_sessions] as S
										left join [content].[tbl_modules] as M on S.module_id = M.module_id
										left join [content].[tbl_session_plans] as C on C.session_plan_id = M.session_plan_id
                                        left join content.tbl_map_session_plan_course AS mp on mp.session_plan_id=c.session_plan_id
										--where course_id=
										),
RES AS 
(
                            SELECT		DISTINCT 
										B.[batch_id],
										(TD.first_name + ' ' + TD.last_name) as trainer_name,
										TD.email as trainer_email,
										B.[batch_code],
										B.[start_date] as batch_start_date,
										B.[end_date] as batch_end_date,
										B.[batch_status],
										B.[is_active] as batch_active_status,
                                        CASE 
                                            WHEN CAST(UPPER(B.[end_date]) AS DATE) < CAST(GETDATE() AS DATE) THEN 1
                                            WHEN (CAST(GETDATE() AS DATE) BETWEEN CAST(UPPER(B.[start_date]) AS DATE) AND CAST(UPPER(B.[end_date]) AS DATE)) THEN 2
                                            WHEN CAST(UPPER(B.[start_date]) AS DATE) > CAST(GETDATE() AS DATE) THEN 3				
                                            ELSE 0
                                        END AS batch_stage_id,
                                        CASE 
                                            WHEN CAST(UPPER(B.[end_date]) AS DATE) < CAST(GETDATE() AS DATE) THEN 'Completed'
                                            WHEN (CAST(GETDATE() AS DATE) BETWEEN CAST(UPPER(B.[start_date]) AS DATE) AND CAST(UPPER(B.[end_date]) AS DATE)) THEN 'Ongoing'
                                            WHEN CAST(UPPER(B.[start_date]) AS DATE) > CAST(GETDATE() AS DATE) THEN 'Scheduled'
                                            ELSE 'Invalid'
                                        END AS batch_stage_name,
                                        B.[business_unit],
										
										Cen.center_name,
										CenT.[center_type_name] as center_type,
                                        (CONCAT(Cou.course_code, '-', Cou.course_name)) as course_name,
										CONCAT(Q.qp_code, '-', Q.qp_name) AS qp_name,
										Client.[client_name] as customer_name,
                                        CASE B.[image_required] WHEN 1 THEN 'Yes' ELSE 'No' END AS image_required,
										
										(SELECT COUNT(SC.session_id) FROM SCount AS SC WHERE SC.course_id=B.course_id) AS session_count	


                            FROM		[batches].[tbl_batches] as B
							left join	[users].[tbl_user_details] as TD on TD.user_id = B.trainer_id
							left join   [masters].[tbl_courses] as Cou on Cou.course_id = B.course_id
							left join	[masters].[tbl_qp] as Q on Q.qp_id = B.qp_id
							left join	[masters].[tbl_center] as Cen on Cen.center_id = B.center_id
							left join	[masters].[tbl_center_type] as CenT on CenT.[center_type_id] = Cen.center_type_id
							left join	[masters].[tbl_projects] as Pro on Pro.project_id = Cou.project_id
							left join	[masters].[tbl_client] as Client on Client.client_id = Pro.client_id 
							
							WHERE		1=1 {}
                            AND			UPPER(B.[start_date]) NOT IN ('NULL','00-JAN-1900') 
                            AND			UPPER(B.[end_date]) NOT IN ('NULL','00-JAN-1900')
                            AND	 		B.is_active=1
                            AND			UPPER(B.batch_status)='BATCH OPEN'
                        )
                      SELECT COUNT(batch_id) AS total_record_count
                        FROM RES 
                        WHERE 1=1
                        {}
                        {}
                        
""".format(email_condition, batch_condition, search_condition)


        curs.execute(quer)
        data = curs.fetchall()
        curs.close()
        con.close()
        return data


    @classmethod
    def result_data_db(cls, email_condition, batch_condition, search_condition, order_by_statement, limit_statement):
        con = pyodbc.connect(conn_str)
        curs = con.cursor()
        quer = """WITH SCount AS
										(
										/****** Script for SelectTopNRows command from SSMS  ******/
										SELECT --count(S.[session_id]) as session_count 
												S.[session_id] as session_id
												,S.[module_id] as module_id
												,M.[session_plan_id] as session_plan_id
												,mp.[course_id] as course_id

										FROM [content].[tbl_sessions] as S
										left join [content].[tbl_modules] as M on S.module_id = M.module_id
										left join [content].[tbl_session_plans] as C on C.session_plan_id = M.session_plan_id
                                        left join content.tbl_map_session_plan_course AS mp on mp.session_plan_id=c.session_plan_id
										--where course_id=
										),
RES AS 
(
                            SELECT		DISTINCT 
										B.[batch_id],
										(TD.first_name + ' ' + TD.last_name) as trainer_name,
										TD.email as trainer_email,
										B.[batch_code],
										B.[start_date] as batch_start_date,
										B.[end_date] as batch_end_date,
										B.[batch_status],
										B.[is_active] as batch_active_status,
                                        CASE 
                                            WHEN CAST(UPPER(B.[end_date]) AS DATE) < CAST(GETDATE() AS DATE) THEN 1
                                            WHEN (CAST(GETDATE() AS DATE) BETWEEN CAST(UPPER(B.[start_date]) AS DATE) AND CAST(UPPER(B.[end_date]) AS DATE)) THEN 2
                                            WHEN CAST(UPPER(B.[start_date]) AS DATE) > CAST(GETDATE() AS DATE) THEN 3				
                                            ELSE 0
                                        END AS batch_stage_id,
                                        CASE 
                                            WHEN CAST(UPPER(B.[end_date]) AS DATE) < CAST(GETDATE() AS DATE) THEN 'Completed'
                                            WHEN (CAST(GETDATE() AS DATE) BETWEEN CAST(UPPER(B.[start_date]) AS DATE) AND CAST(UPPER(B.[end_date]) AS DATE)) THEN 'Ongoing'
                                            WHEN CAST(UPPER(B.[start_date]) AS DATE) > CAST(GETDATE() AS DATE) THEN 'Scheduled'
                                            ELSE 'Invalid'
                                        END AS batch_stage_name,
                                        BU.bu_name AS business_unit,
										
										Cen.center_name,
										CenT.[center_type_name] as center_type,
                                        (CONCAT(Cou.course_code, '-', Cou.course_name)) as course_name,
										CONCAT(Q.qp_code, '-', Q.qp_name) AS qp_name,
										Client.[client_name] as customer_name,
                                        CASE B.[image_required] WHEN 1 THEN 'Yes' ELSE 'No' END AS image_required,
										
										(SELECT COUNT(SC.session_id) FROM SCount AS SC WHERE SC.course_id=B.course_id) AS session_count	


                            FROM		                        [batches].[tbl_batches] as B
							left join	[users].[tbl_user_details] as TD on TD.user_id = B.trainer_id
							left join       [masters].[tbl_courses] as Cou on Cou.course_id = B.course_id
							left join	[masters].[tbl_qp] as Q on Q.qp_id = Cou.qp_id
							left join	[masters].[tbl_center] as Cen on Cen.center_id = B.center_id
							left join	[masters].[tbl_center_type] as CenT on CenT.[center_type_id] = Cen.center_type_id
							left join	[masters].[tbl_projects] as Pro on Pro.project_id = Cou.project_id
							left join	[masters].[tbl_client] as Client on Client.client_id = Pro.client_id
                            left join   [masters].[tbl_bu] as BU on BU.bu_id = Cen.bu_id 
							
							WHERE		1=1 {}
                            AND			UPPER(B.[start_date]) NOT IN ('NULL','00-JAN-1900') 
                            AND			UPPER(B.[end_date]) NOT IN ('NULL','00-JAN-1900')
                            AND	 		B.is_active=1
                            AND			UPPER(B.batch_status)='BATCH OPEN'
                        )
                      
                      SELECT
                             RES.trainer_name,
                             RES.trainer_email,
                             RES.batch_code,
                             RES.session_count,
                             RES.batch_start_date,
                             RES.batch_end_date,
                             RES.batch_status,
                             RES.batch_active_status,
                             RES.batch_stage_name,
                             RES.business_unit,
                             RES.center_name,
                             RES.center_type,
                             RES.course_name,
                             RES.qp_name,
                             RES.customer_name,
                             RES.image_required,
                             RES.batch_id
                             
                    FROM 	 RES 
                    WHERE    1=1
                    {}
                    {}
                    {}
                    {}
                        
""".format(email_condition, batch_condition, search_condition, order_by_statement, limit_statement)
        curs.execute(quer)
        data = curs.fetchall()
        curs.close()
        con.close()
        return data

    


    @classmethod
    def get_trainer_batch(cls,batch_id):
        con = pyodbc.connect(conn_str)
        curs = con.cursor()
        quer = """
/****** Script for SelectTopNRows command from SSMS  ******/
SELECT           [batch_id]
		,[batch_code]
		,[batch_status]
		,B.[is_active]
		,[start_date]
		,[end_date]
		,[business_unit]
		,Cen.center_name
		,CenT.[center_type_name] as center_type
		,B.[course_id]
		,Cou.course_code
		,Cou.course_name
		,B.qp_id
		,Q.qp_code
		,Q.qp_name
		,Client.[client_name] as customer_name
		,(TD.first_name + ' ' + TD.last_name) as trainer_name
		,TD.email as trainer_email
		,[image_required]
		,(TD.first_name + ' ' + TD.last_name) as trainer_name

      
  FROM          [batches].[tbl_batches] as B
  left join	[users].[tbl_user_details] as TD on TD.user_id = B.trainer_id
  left join     [masters].[tbl_courses] as Cou on Cou.course_id = B.course_id
  left join	[masters].[tbl_qp] as Q on Q.qp_id = B.qp_id
  left join	[masters].[tbl_center] as Cen on Cen.center_id = B.center_id
  left join	[masters].[tbl_center_type] as CenT on CenT.[center_type_id] = Cen.center_type_id
  left join	[masters].[tbl_projects] as Pro on Pro.project_id = Cou.project_id
  left join	[masters].[tbl_client] as Client on Client.client_id = Pro.client_id

  WHERE		B.batch_id={}

""".format(batch_id)
        curs.execute(quer)
        data = curs.fetchall()
        curs.close()
        con.close()
        return data


    @classmethod
    def trainer_session_db(cls, trainer_email, batch_id):
        con = pyodbc.connect(conn_str)
        curs = con.cursor()

        quer = """SELECT count(*)

  FROM [users].[tbl_user_details]
  where email = '{}'
  """.format(trainer_email)
        curs.execute(quer)
        data = curs.fetchall()[0][0]
        if data<=0:
            return []
        

        
        quer = """
/****** Script for SelectTopNRows command from SSMS  ******/
WITH SCount AS
										(
										/****** Script for SelectTopNRows command from SSMS  ******/
										SELECT --count(S.[session_id]) as session_count 
												S.[session_id] as session_id
												,S.session_name as session_name
												,S.[module_id] as module_id
												,M.[session_plan_id] as session_plan_id
												,mp.[course_id] as course_id

										FROM      [content].[tbl_sessions] as S
										left join [content].[tbl_modules] as M on S.module_id = M.module_id
										left join [content].[tbl_session_plans] as C on C.session_plan_id = M.session_plan_id
                                        left join content.tbl_map_session_plan_course AS mp on mp.session_plan_id=c.session_plan_id
										--where course_id=
										)
SELECT 
				 B.[batch_id]
				,SC.session_id
				,SC.session_name
				,FORMAT(STG1.log_date_time,'dd-MMM-yyyy hh:mm:ss tt') AS stage1_log_time
				,STG1.image_file_name AS stage1_image
				,STG1.latitude AS stage1_latitide
				,STG1.longitute AS stage1_longitude
				,FORMAT(STG2.log_date_time,'dd-MMM-yyyy hh:mm:ss tt') AS stage2_log_time
				,STG2.image_file_name AS stage2_image
				,STG2.latitude AS stage2_latitide
				,STG2.longitute AS stage2_longitude
				,FORMAT(STG3.log_date_time,'dd-MMM-yyyy hh:mm:ss tt') AS stage3_log_time
				,STG3.image_file_name AS stage3_image
				,STG3.latitude AS stage3_latitide
				,STG3.longitute AS stage3_longitude
				,FORMAT(STG4.log_date_time,'dd-MMM-yyyy hh:mm:ss tt') AS stage4_log_time
				,STG4.image_file_name AS stage4_image
				,STG4.latitude AS stage4_latitide
				,STG4.longitute AS stage4_longitude

      
  FROM [batches].[tbl_batches] as B
  left join SCount as SC on SC.course_id=B.course_id
  left join [masters].[tbl_tma_trainer_stage_log] as STG1 on STG1.trainer_id=B.trainer_id AND STG1.batch_id=B.batch_id AND STG1.stage_id=1 AND STG1.session_id=SC.session_id
  left join [masters].[tbl_tma_trainer_stage_log] as STG2 on STG2.trainer_id=B.trainer_id AND STG2.batch_id=B.batch_id AND STG2.stage_id=2 AND STG2.session_id=SC.session_id
  left join [masters].[tbl_tma_trainer_stage_log] as STG3 on STG3.trainer_id=B.trainer_id AND STG3.batch_id=B.batch_id AND STG3.stage_id=3 AND STG3.session_id=SC.session_id
  left join [masters].[tbl_tma_trainer_stage_log] as STG4 on STG4.trainer_id=B.trainer_id AND STG4.batch_id=B.batch_id AND STG4.stage_id=4 AND STG4.session_id=SC.session_id

  WHERE		B.batch_id={}
  AND		ISNULL(SC.session_id,0)>0
  ORDER BY	SC.session_id
""".format(batch_id)
        #return quer
        curs.execute(quer)
        data = curs.fetchall()
        curs.close()
        con.close()
        return data

    def get_candidate_attendance_db(batch_id, session_id):
        con = pyodbc.connect(conn_str)
        curs = con.cursor()
        quer = """
                WITH RES AS
                    (
                        SELECT	    A.[key] AS enrollment_id,
                                    REPLACE(CONVERT(VARCHAR,ATT.attendance_date,106),' ','-') AS attendance_date,
                                    A.[value] AS image_file_name,
				    ATT.batch_id,
				    ATT.session_id
									
									
                        FROM		[masters].[tbl_tma_candidate_attendance] AS ATT
                        CROSS APPLY OPENJSON(ATT.attendance_json_data) AS A
                        WHERE		ATT.batch_id={}
                        AND		ATT.session_id={}
                    )
/*
Candi as (
SELECT * FROM E
)*/
--SELECT * FROM E
SELECT					cb.name as candidate_name,
                        COALESCE(can_reg.enrollment_id,'') AS enrollment_id,
						--0 AS enrollment_id,
						'' AS guardian_name,
                        cb.mobile_number as phone,
                        '' AS gender,
                        '' AS date_of_birth,
                        COALESCE(E.attendance_date,'') AS attendance_date,
                        (CASE WHEN ISNULL(E.enrollment_id,'') != '' THEN 'Present' ELSE 'Absent' END) AS attendance,
                        COALESCE(E.image_file_name,'') AS image_file_name
            FROM		        batches.tbl_map_candidate_batches AS C
			LEFT JOIN	candidate_details.tbl_candidate_registration_enrollment_id AS can_reg ON can_reg.candidate_id=c.candidate_id AND can_reg.course_id=c.course_id 
			LEFT JOIN	candidate_details.tbl_candidate_basic_details AS cb ON cb.candidate_id=c.candidate_id
            INNER JOIN  batches.tbl_batches AS B ON B.batch_id=C.batch_id
			LEFT JOIN	RES AS E ON CAST(E.enrollment_id AS nvarchar) COLLATE SQL_Latin1_General_CP1_CI_AS =can_reg.enrollment_id COLLATE SQL_Latin1_General_CP1_CI_AS
            --LEFT JOIN	E ON CAST(E.enrollment_id AS varchar(MAX))=CAST(can_reg.enrollment_id AS nvarchar(MAX))
            WHERE		B.batch_id={}
            AND			TRIM(ISNULL(cb.name,''))<>''
            AND			IIF(ISNULL(CAST(C.dropped_date AS nvarchar(30)),'')='','NULL',CAST(C.dropped_date AS nvarchar(30)))='NULL'
            ORDER BY	cb.name
                
                        """.format(batch_id, session_id, batch_id)
        curs.execute(quer)
        data = curs.fetchall()
        curs.close()
        con.close()
        #return quer
        return data
    

    @classmethod
    def get_candidate_group_attendance_db(cls,batch_id, session_id):
        con = pyodbc.connect(conn_str)
        curs = con.cursor()
        quer = """
                SELECT		A.[key] AS image_file_name,
                                A.[value] AS remarks
			
                FROM		[masters].[tbl_tma_candidate_attendance] AS ATT
                CROSS APPLY     OPENJSON(ISNULL(NULLIF(ATT.group_attendance_image_json_data,''),'{}')) AS A
                WHERE		ATT.batch_id={}
                AND		ATT.session_id={}
                                
                        """.format(batch_id, session_id)
        curs.execute(quer)
        data = curs.fetchall()
        curs.close()
        con.close()
        return data
       
    def AllAssessmentStages(UserId,UserRoleId):
        response=[]
        h={}
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec	[assessments].[sp_get_assessment_stages] ?, ?'
        values = (UserId,UserRoleId)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            for i in range(len(columns)):
                h[columns[i]]=row[i] 
            #h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1]}
            response.append(h.copy())
        cur.commit()
        cur.close()
        con.close()
        return response
    def AllCertificationStages(UserId,UserRoleId):
        response=[]
        h={}
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec	[assessments].[sp_get_certification_stages] ?, ?'
        values = (UserId,UserRoleId)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            for i in range(len(columns)):
                h[columns[i]]=row[i] 
            #h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1]}
            response.append(h.copy())
        cur.commit()
        cur.close()
        con.close()
        return response
    def AllCertificateNames(batch_id,stage):
        response=[]
        h={}
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec	[assessments].[sp_get_certificate_names] ?,?'
        values = (batch_id,stage)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            for i in range(len(columns)):
                h[columns[i]]=row[i] 
            #h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1]}
            response.append(h.copy())
        cur.commit()
        cur.close()
        con.close()
        return response
     
    def AllRegionsBasedOnUser(UserId,UserRoleId,UserRegionId):
        response=[]
        h={}
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec	[masters].[sp_get_regions_based_on_user] ?, ?, ?'
        values = (UserId,UserRoleId,UserRegionId)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            for i in range(len(columns)):
                h[columns[i]]=row[i] 
            #h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1]}
            response.append(h.copy())
        cur.commit()
        cur.close()
        con.close()
        return response
    
    def GetAllCentersBasedOnRegion_User(UserId,UserRoleId,RegionId):
        response=[]
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec	[masters].[sp_get_centers_based_on_region_user] ?, ?,?'
        values = (UserId,UserRoleId,RegionId)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1]}
            response.append(h)
        cur.commit()
        cur.close()
        con.close()       
        return response
    
    def GetAllCoursesBasedOnCenter_User(UserId,UserRoleId,CenterId):
        response=[]
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec	masters.sp_get_courses_based_on_center_user ?, ?,?'
        values = (UserId,UserRoleId,CenterId)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1]}
            response.append(h)
        cur.commit()
        cur.close()
        con.close()       
        return response
        
    def GetAllTrainersBasedOnCenter_User(UserId,UserRoleId,CenterId):
        response=[]
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec	masters.sp_get_trainers_based_on_center_user ?, ?,?'
        values = (UserId,UserRoleId,CenterId)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1]}
            response.append(h)
        cur.commit()
        cur.close()
        con.close()       
        return response
    
    def GetAllMobilizersBasedOnCenter_User(UserId,UserRoleId,CenterId):
        response=[]
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec	[masters].[sp_get_mobilizers_based_on_center_user] ?, ?,?'
        values = (UserId,UserRoleId,CenterId)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1]}
            response.append(h)
        cur.commit()
        cur.close()
        con.close()       
        return response

    def TrainerDeploymentBatches(region_id,sub_project_ids,course_ids,trainer_ids,from_date,to_date,batch_stage_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        batch = {}
        d = []
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [batches].[sp_tma_web_batch_detail_list] ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?'
        values = (region_id,sub_project_ids,course_ids,trainer_ids,batch_stage_id,from_date,to_date,start_index,page_length,search_value,order_by_column_position,order_by_column_direction)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        record="0"
        fil="0"
        for row in cur:
            record=row[24]
            fil=row[23]
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[3]+"":row[3],""+columns[4]+"":row[4],""+columns[5]+"":row[5],""+columns[6]+"":row[6],""+columns[7]+"":row[7],""+columns[8]+"":row[8],""+columns[9]+"":row[9],""+columns[10]+"":row[10],""+columns[11]+"":row[11],""+columns[12]+"":row[12],""+columns[13]+"":row[13],""+columns[14]+"":row[14],""+columns[15]+"":row[15],""+columns[16]+"":row[16],""+columns[17]+"":row[17],""+columns[18]+"":row[18],""+columns[19]+"":row[19],""+columns[20]+"":row[20],""+columns[21]+"":row[21],""+columns[22]+"":row[22]}
            d.append(h)
        batch = {"draw":draw,"recordsTotal":record,"recordsFiltered":fil,"data":d}
        cur.close()
        con.close()
        return batch
    def ReportAttendanceBatches(region_id,sub_project_ids,course_ids,trainer_ids,from_date,to_date,batch_stage_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw, user_id, user_role_id):
        batch = {}
        d = []
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [batches].[sp_tma_batch_list_for_attendance_report] ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?'
        values = (region_id,sub_project_ids,course_ids,trainer_ids,batch_stage_id,from_date,to_date,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,user_id, user_role_id)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        record="0"
        fil="0"
        for row in cur:
            record=row[24]
            fil=row[23]
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[3]+"":row[3],""+columns[4]+"":row[4],""+columns[5]+"":row[5],""+columns[6]+"":row[6],""+columns[7]+"":row[7],""+columns[8]+"":row[8],""+columns[9]+"":row[9],""+columns[10]+"":row[10],""+columns[11]+"":row[11],""+columns[12]+"":row[12],""+columns[13]+"":row[13],""+columns[14]+"":row[14],""+columns[15]+"":row[15],""+columns[16]+"":row[16],""+columns[17]+"":row[17],""+columns[18]+"":row[18],""+columns[19]+"":row[19],""+columns[20]+"":row[20],""+columns[21]+"":row[21],""+columns[22]+"":row[22]}
            d.append(h)
        batch = {"draw":draw,"recordsTotal":record,"recordsFiltered":fil,"data":d}
        cur.close()
        con.close()
        return batch
    
    def ReportBatchSession(batch_id,course_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        sessions = {}
        d = []
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [batches].[sp_tma_batch_session_information] ?, ?, ?, ?, ?, ?, ?'
        values = (batch_id,course_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        record="0"
        fil="0"
        for row in cur:
            record=row[11]
            fil=row[10]
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[3]+"":row[3],""+columns[4]+"":row[4],""+columns[5]+"":row[5],""+columns[6]+"":row[6],""+columns[7]+"":row[7],""+columns[8]+"":row[8],""+columns[9]+"":row[9]}
            d.append(h)
        sessions = {"draw":draw,"recordsTotal":record,"recordsFiltered":fil,"data":d}
        cur.close()
        con.close()
        return sessions
    def GetBatchDetailsForAttReport(batch_id):
        details={}
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec batches.sp_get_batch_details_for_att_report ?'
        values = (batch_id,)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            details={""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[3]+"":row[3],""+columns[4]+"":row[4],""+columns[5]+"":row[5]}
        cur.close()
        con.close()
        return details
    def GetSessionTrainerActivity(batch_id,session_id):
        details={}
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec batches.sp_get_session_trainer_activity ?,?'
        values = (batch_id,session_id)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            details={""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[3]+"":row[3],""+columns[4]+"":row[4],""+columns[5]+"":row[5],""+columns[6]+"":row[6],""+columns[7]+"":row[7],""+columns[8]+"":row[8],""+columns[9]+"":row[9],""+columns[10]+"":row[10],""+columns[11]+"":row[11],""+columns[12]+"":row[12],""+columns[13]+"":row[13],""+columns[14]+"":row[14],""+columns[15]+"":row[15],""+columns[16]+"":row[16],""+columns[17]+"":row[17],""+columns[18]+"":row[18]}
        cur.close()
        con.close()
        return details
    def GetCandidateSessionAttendance(batch_id,session_id):
        details=[]
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec batches.sp_get_candidate_session_attendance ?,?'
        values = (batch_id,session_id)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h={""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[3]+"":row[3],""+columns[4]+"":row[4],""+columns[5]+"":row[5],""+columns[6]+"":row[6]}
            details.append(h)
        cur.close()
        con.close()
        return details
    def GetCandidateGrpAttendance(batch_id,session_id):
        details=[]
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        quer = """
                SELECT		A.[key] AS image_file_name,
                                A.[value] AS remarks
			
                FROM		[masters].[tbl_tma_candidate_attendance] AS ATT
                CROSS APPLY     OPENJSON(ISNULL(NULLIF(ATT.group_attendance_image_json_data,''),'{}')) AS A
                WHERE		ATT.batch_id={}
                AND		ATT.session_id={}
                                
                        """.format('{}',batch_id, session_id)
        cur.execute(quer)
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h={""+columns[0]+"":row[0],""+columns[1]+"":row[1]}
            details.append(h)
        cur.close()
        con.close()
        return details
    def GetMobilizationReportData(region_id,center_id,course_ids,mobilizer_ids,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        list = {}
        d = []
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec masters.sp_get_mobilization_report_data ?, ?, ?, ?, ?, ?, ?, ?, ?'
        values = (region_id,center_id,course_ids,mobilizer_ids,start_index,page_length,search_value,order_by_column_position,order_by_column_direction)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        record="0"
        fil="0"
        for row in cur:
            record=row[10]
            fil=row[9]
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[3]+"":row[3],""+columns[4]+"":row[4],""+columns[5]+"":row[5],""+columns[6]+"":row[6],""+columns[7]+"":row[7],""+columns[8]+"":row[8]}
            d.append(h)
        list = {"draw":draw,"recordsTotal":record,"recordsFiltered":fil,"data":d}
        cur.close()
        con.close()
        return list
    def GetRegisteredCandidatesList(center_id,course_id,mobilizer_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        candidates = {}
        d = []
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [masters].[sp_get_registered_candidate_list_by_mob] ?, ?, ?, ?, ?, ?, ?, ?'
        values = (center_id,course_id,mobilizer_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        record="0"
        fil="0"
        for row in cur:
            record=row[10]
            fil=row[9]
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[3]+"":row[3],""+columns[4]+"":row[4],""+columns[5]+"":row[5],""+columns[6]+"":row[6],""+columns[7]+"":row[7],""+columns[8]+"":row[8]}
            d.append(h)
        candidates = {"draw":draw,"recordsTotal":record,"recordsFiltered":fil,"data":d}
        cur.close()
        con.close()
        return candidates
    def GetCandidateBasicDetails(candidate_id):
        details = {}
        
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec candidate_details.sp_get_candidate_basic_details ?'
        values = (candidate_id,)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            #h = {""+str(row[2])+"":str(row[3])}
            details[str(row[2])]=str(row[3])
        cur.close()
        con.close()
        return details

    def recover_pass_db(email_id):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()

        sql = 'exec users.sp_recover_password ?'
        values = (email_id,)
        cur.execute(sql,(values))

        data = cur.fetchall()

        cur.close()
        con.close()
        return data

    def change_password_api_db(old_password, new_password, user_id):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()

        sql = 'exec users.sp_change_password ?, ?, ?'
        values = (new_password, old_password, user_id)
        cur.execute(sql,(values))

        data = cur.fetchall()
        if data[0][0]==0:
            message = {'title' : 'Error', 'message': 'Failed to update Password', 'Row_count':data[0][0]}
        else:
            message = {'title' : 'Success', 'message': 'Successfully updated Password', 'Row_count':data[0][0]}

        #message = {'message' : 'db_done', 'title': 'check', 'UserId':0}
        cur.commit()
        cur.close()
        con.close()
        return message
    def GetAllClustersBasedOnMultipleRegion_User(UserId,UserRoleId,RegionIds):
        response=[]
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec	[masters].[sp_get_clusters_based_on_multiple_region_user] ?, ?,?'
        values = (UserId,UserRoleId,RegionIds)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1]}
            response.append(h)
        cur.commit()
        cur.close()
        con.close()       
        return response
    
    def GetAllCentersBasedOnMultipleClusters_User(UserId,UserRoleId,ClusterIds):
        response=[]
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec	[masters].[sp_get_centers_based_on_multiple_clusters_user] ?, ?,?'
        values = (UserId,UserRoleId,ClusterIds)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1]}
            response.append(h)
        cur.commit()
        cur.close()
        con.close()       
        return response
    
    def GetAllCoursesBasedOnMultipleCenters_User(UserId,UserRoleId,CenterIds):
        response=[]
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec	[masters].[sp_get_courses_based_on_multiple_centers_user] ?, ?,?'
        values = (UserId,UserRoleId,CenterIds)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1]}
            response.append(h)
        cur.commit()
        cur.close()
        con.close()       
        return response
    def GetAllCooBasedOnMultipleRegions_User(UserId,UserRoleId,RegionIds):
        response=[]
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec	[masters].[sp_get_coos_based_on_multiple_regions_user]  ?, ?,?'
        values = (UserId,UserRoleId,RegionIds)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1]}
            response.append(h)
        cur.commit()
        cur.close()
        con.close()       
        return response
    def GetAllTmBasedOnMultipleClusters_User(UserId,UserRoleId,ClusterIds):
        response=[]
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec	[masters].[sp_get_tms_based_on_multiple_clusters_user] ?, ?,?'
        values = (UserId,UserRoleId,ClusterIds)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1]}
            response.append(h)
        cur.commit()
        cur.close()
        con.close()       
        return response

    def tma_registration_compliance_report(region_id,cluster_id,center_id,center_type_id,course_id,tm,coo,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        details = {}
        d = []
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec masters.sp_tma_registration_compliance_web_list ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?'
        values = (region_id,cluster_id,center_type_id,center_id,course_id,coo,tm,start_index,page_length,search_value,order_by_column_position,order_by_column_direction)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        record="0"
        fil="0"
        for row in cur:
            record=row[17]
            fil=row[16]
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[3]+"":row[3],""+columns[4]+"":row[4],""+columns[5]+"":row[5],""+columns[6]+"":row[6],""+columns[7]+"":row[7],""+columns[8]+"":row[8],""+columns[9]+"":row[9],""+columns[10]+"":row[10],""+columns[11]+"":row[11],""+columns[12]+"":row[12],""+columns[13]+"":row[13],""+columns[14]+"":row[14],""+columns[15]+"":row[15]}
            d.append(h)
        details = {"draw":draw,"recordsTotal":record,"recordsFiltered":fil,"data":d}
        cur.close()
        con.close()
        return details

    def download_tma_registration_compliance_report(region_id,cluster_id,center_id,center_type_id,course_id,tm,coo):
        columns=[]
        response={}
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [masters].[sp_tma_registration_compliance_data] ?, ?, ?, ?, ?, ?, ?'
        values = (region_id,cluster_id,center_id,center_type_id,course_id,tm,coo)
        cur.execute(sql,(values))
        columnss = [column[0].title() for column in cur.description]
        data=cur.fetchall()        
        col=['Region_Name', 'Cluster_Name', 'Center_Type_Name', 'Center_Name', 'Course_Name', 'Batch_Count', 'Trainer_Count', 'Tma_Used_Trainer','Coo','Tm']
        
        out = []
        for i in data:
            out.append(list(i))        
        df=pd.DataFrame(out,columns=columnss)
        #print(df.head())
        df=df[col]        
        cur.close()
        con.close()
        #print(df)
        return df
    def trainerwise_tma_registration_compliance_report(region_id,cluster_id,center_id,center_type_id,course_id,tm,coo,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        details = {}
        d = []
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [masters].[sp_trainerwise_tma_registration_compliance_web_list] ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?'
        values = (region_id,cluster_id,center_type_id,center_id,course_id,coo,tm,start_index,page_length,search_value,order_by_column_position,order_by_column_direction)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        record="0"
        fil="0"
        for row in cur:
            record=row[17]
            fil=row[16]
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[3]+"":row[3],""+columns[4]+"":row[4],""+columns[5]+"":row[5],""+columns[6]+"":row[6],""+columns[7]+"":row[7],""+columns[8]+"":row[8],""+columns[9]+"":row[9],""+columns[10]+"":row[10],""+columns[11]+"":row[11],""+columns[12]+"":row[12],""+columns[13]+"":row[13],""+columns[14]+"":row[14],""+columns[15]+"":row[15]}
            d.append(h)
        details = {"draw":draw,"recordsTotal":record,"recordsFiltered":fil,"data":d}
        cur.close()
        con.close()
        return details
    def download_trainerwise_tma_registration_compliance_report(region_id,cluster_id,center_id,center_type_id,course_id,tm,coo):
        columns=[]
        response={}
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [masters].[sp_trainerwise_tma_registration_compliance_data] ?, ?, ?, ?, ?, ?, ?'
        values = (region_id,cluster_id,center_id,center_type_id,course_id,tm,coo)
        cur.execute(sql,(values))
        columnss = [column[0].title() for column in cur.description]
        data=cur.fetchall()        
        col=['Trainer_Name','Region_Name', 'Cluster_Name', 'Center_Type_Name', 'Center_Name', 'Course_Name', 'Batch_Count','Coo','Tm']
        
        out = []
        for i in data:
            out.append(list(i))        
        df=pd.DataFrame(out,columns=columnss)
        
        df=df[col]        
        cur.close()
        con.close()
        return df

    def sector_list(sector_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        content = {}
        d = []
        h={}
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [masters].[sp_get_sector_list] ?, ?, ?, ?, ?, ?'
        values = (sector_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        record="0"
        fil="0"
        for row in cur:
            record=row[len(columns)-1]
            fil=row[len(columns)-2]
            for i in range(len(columns)-2):
                h[columns[i]]=row[i]
            d.append(h.copy())
        content = {"draw":draw,"recordsTotal":record,"recordsFiltered":fil,"data":d}
        cur.close()
        con.close()
        return content

    def contract_list(user_id,user_role_id,contract_id,customer_ids,stage_ids,from_date,to_date,entity_ids,sales_category_ids,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        content = {}
        d = []
        h={}
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [masters].[sp_get_contract_list] ?,?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?'
        values = (user_id,user_role_id,contract_id,customer_ids,stage_ids,from_date,to_date,entity_ids,sales_category_ids,start_index,page_length,search_value,order_by_column_position,order_by_column_direction)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        record="0"
        fil="0"
        for row in cur:
            record=row[len(columns)-1]
            fil=row[len(columns)-2]
            for i in range(len(columns)-2):
                h[columns[i]]=row[i]
            #h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[3]+"":row[3],""+columns[4]+"":row[4],""+columns[5]+"":row[5],""+columns[6]+"":row[6],""+columns[7]+"":row[7],""+columns[8]+"":row[8],""+columns[9]+"":row[9]}
            d.append(h.copy())
        content = {"draw":draw,"recordsTotal":record,"recordsFiltered":fil,"data":d}
        cur.close()
        con.close()
        return content
    
    def GetAllBusBasedOn_User(UserId,UserRoleId):
        response=[]
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec	[masters].[sp_get_bu_based_on_user] ?, ?'
        values = (UserId,UserRoleId)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1]}
            response.append(h)
        cur.commit()
        cur.close()
        con.close()       
        return response
    
    def download_centers_list(center_type_ids,bu_ids,status):
        columns=[]
        response={}
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [masters].[sp_get_centers_list_data] ?, ?, ?'
        values =(center_type_ids,bu_ids,status)
        cur.execute(sql,(values))
        columnss = [column[0].title() for column in cur.description]
        data=cur.fetchall()        
        col=['Center_Name', 'Center_Type_Name','Bu_Name','Is_Active', 'Region_Name','Cluster_Name','Country_Name','State_Name','District_Name','Location']        
        out = []
        for i in data:
            out.append(list(i))        
        df=pd.DataFrame(out,columns=columnss)
        #print(df.head())
        df=df[col]        
        cur.close()
        con.close()
        #print(df)
        return df


    def get_all_me():
        bu = []
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'select * from masters.[tbl_map_ME_category] where is_active=1;'
        cur.execute(sql)
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[1]+"":row[1],""+columns[2]+"":row[2], ""+columns[3]+"":row[3], ""+columns[4]+"":row[4]}
            bu.append(h)
        cur.close()
        con.close()
        return bu

    def get_me_category_db():
        bu = []
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'select * from [masters].[tbl_mecategory] where is_active=1;'
        cur.execute(sql)
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[1]+"":row[1],""+columns[2]+"":row[2]}
            bu.append(h)
        cur.close()
        con.close()
        return bu

    def client_basedon_user(user_id, user_role_id):
        client = []
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()

        sql = 'exec masters.sp_client_based_on_user ?, ?'
        values = (user_id, user_role_id)
        cur2.execute(sql,(values))

        columns = [column[0].title() for column in cur2.description]
        for r in cur2:
            h = {""+columns[0]+"":r[0],""+columns[1]+"":r[1]}
            client.append(h)
        cur2.close()
        con.close()
        return client

    @classmethod
    def AllCustomer_report_db(cls):
        response=[]
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = '''
        SELECT      distinct
		            [customer_name]
		FROM        [tma].[tbl_batches]
        order by    customer_name asc
        '''
        cur.execute(sql)
        for row in cur:
            h = {"customer_name":row[0]}
            response.append(h)
        cur.close()
        con.close()       
        return response

    @classmethod
    def AllCenter_customer_db(cls, customer_id):
        response=[]
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [masters].[sp_center_basedon_course] ?'
        values = (customer_id,)
        cur.execute(sql,(values))

        for row in cur:
            h = {"Center_Name":row[0]}
            response.append(h)
        cur.close()
        con.close()       
        return response

    @classmethod
    def AllCourse_customercenter_db(cls, customer_id, center_id):
        response=[]
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [masters].[sp_course_basedon_coursecenter] ?, ?'
        values = (customer_id, center_id)
        cur.execute(sql,(values))
        
        for row in cur:
            h = {"Course_Name":row[0]}
            response.append(h)
        cur.close()
        con.close()       
        return response

    @classmethod
    def download_trainer_filter(cls, user_id, user_role_id, centers, status, path):
        
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [users].[sp_get_trainer_list_download] ?, ?, ?, ?'
        values = (user_id, user_role_id, centers, status)
        cur.execute(sql,(values))

        columns = [column[0].title() for column in cur.description]
        data=cur.fetchall()

        writer = pd.ExcelWriter(path, engine='xlsxwriter')
        workbook  = writer.book

        header_format = workbook.add_format({
            'bold': True,
            'text_wrap': True,
            'valign': 'center',
            'fg_color': '#D7E4BC',
            'border': 1})

        df = pd.DataFrame(data)
        df.to_excel(writer, index=None, header=None, startrow=1 ,sheet_name='Trainer List')
        worksheet = writer.sheets['Trainer List']
        for col_num, value in enumerate(columns):
            worksheet.write(0, col_num, value, header_format)
        writer.save()
        cur.close()
        con.close()
        return True
    def GetAllContractStages():
        client = []
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()

        sql = 'exec masters.sp_get_contract_stages '
        #values = (,)
        cur2.execute(sql)
        columns = [column[0].title() for column in cur2.description]
        for r in cur2:
            h = {""+columns[0]+"":r[0],""+columns[1]+"":r[1]}
            client.append(h)
        cur2.close()
        con.close()
        return client


    def AllSector_db():
        response=[]
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        cur.execute("select	sector_id, sector_name  from		masters.tbl_sector  where		is_active=1  and			is_deleted=0")
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1]}
            response.append(h)
        cur.commit()
        cur.close()
        con.close()       
        return response

    def All_Emp_Status_db():
        response=[]
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        cur.execute("SELECT distinct [employment_status_id] ,[employment_status_name] FROM [users].[tbl_employment_status] where is_active=1 and is_deleted=0")
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1]}
            response.append(h)
        cur.commit()
        cur.close()
        con.close()       
        return response

    def All_RM_role_db():
        response=[]
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec users.sp_get_all_RM_role'
        cur.execute(sql)
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1]}
            response.append(h)
        cur.commit()
        cur.close()
        con.close()       
        return response

    def All_RM_basedon_role_db(rm_role_id):
        response=[]
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec users.sp_get_all_RM_basedon_role ?'
        values = (rm_role_id,)
        cur.execute(sql,(values))
        
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1]}
            response.append(h)
        cur.commit()
        cur.close()
        con.close()       
        return response

    def All_entity_db():
        response=[]
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        h={}
        cur.execute("SELECT entity_id,entity_name  FROM [masters].[tbl_entity] where is_active=1 and is_deleted=0")
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            for i in range(len(columns)):
                h[columns[i]]=row[i]
            response.append(h.copy())
        cur.commit()
        cur.close()
        con.close()       
        return response

    def All_role_db():
        response=[]
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        
        cur.execute("SELECT employee_role_id, employee_role_name  FROM [users].[tbl_employee_role] where is_active=1 and is_deleted=0 and employee_role_name not like '%trainer%'")
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1]}
            response.append(h)
        cur.commit()
        cur.close()
        con.close()       
        return response
    
    def All_role_neo_db():
        response=[]
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        
        cur.execute("SELECT user_role_id, user_role_name  FROM [users].[tbl_user_role] where is_active=1 and is_deleted=0 order by user_role_name")
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1]}
            response.append(h)
        cur.commit()
        cur.close()
        con.close()
        #print(response)       
        return response

    def All_dept_db():
        response=[]
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        
        cur.execute("SELECT employee_department_id, employee_department_name  FROM [users].[tbl_employee_department] where is_active=1 and is_deleted=0")
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1]}
            response.append(h)
        cur.commit()
        cur.close()
        con.close()       
        return response

    def AllQPBasedOnSector_db(sector_id):
        response=[]
        con = pyodbc.connect(conn_str)
        cur = con.cursor()        
        sql = 'exec [masters].[sp_get_qp_list_bysector] ?'
        values = (sector_id,)
        cur.execute(sql,(values))
        
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1]}
            response.append(h)
        cur.commit()
        cur.close()
        con.close()       
        return response

    
    def AllCourse_db():
        response=[]
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        cur.execute("exec [masters].[sp_get_all_courses]")
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1]}
            response.append(h)
        cur.commit()
        cur.close()
        con.close()       
        return response


    def GetDataForExcel(sp_name):
        try:
            col=[]
            response={}
            con = pyodbc.connect(conn_str)
            cur = con.cursor()
            sql = 'exec '+ sp_name            
            cur.execute(sql)
            col = [column[0].title() for column in cur.description]
            data=cur.fetchall()   
            out = []
            for i in data:
                out.append(list(i))        
            df=pd.DataFrame(out)       
            cur.close()
            con.close()
            response= {"columns":col,"data":df}
            return response
        except Exception as e:
            print(str(e))


    def All_Funding_resources_db():
        response=[]
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        
        cur.execute("select funding_source_id, funding_source_name from [masters].[tbl_funding_source] where is_active=1 and is_deleted=0")
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1]}
            response.append(h)
        cur.commit()
        cur.close()
        con.close()       
        return response
    
    def GetDashboardCount(UserId,UserRoleId,UserRegionId):
        response={}
        con = pyodbc.connect(conn_str)
        cur = con.cursor()        
        sql = 'exec [masters].[sp_get_dashboard_count]  ?,?,?'
        values = (UserId,UserRoleId,UserRegionId)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            for i in range(len(columns)):
                response[columns[i]]=row[i]
        cur.close()
        con.close()
        return response
    
    def GetDepartmentUsers(UserId,UserRoleId,UserRegionId):
        res=[]
        response={}
        con = pyodbc.connect(conn_str)
        cur = con.cursor()        
        sql = 'exec [masters].[sp_get_department_trainers]  ?,?,?'
        values = (UserId,UserRoleId,UserRegionId)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            for i in range(len(columns)):
                response[columns[i]]=row[i]            
            res.append(response.copy())
        cur.close()
        con.close()
        return res
    def get_project_basedon_client_multiple(user_id,user_role_id,client_id):
        project = []
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()
        values=(user_id,user_role_id,client_id)
        sql = 'exec masters.sp_get_projects_based_on_customer ?,?,?'
        cur2.execute(sql,(values))
        columns = [column[0].title() for column in cur2.description]
        for r in cur2:
            h = {""+columns[0]+"":r[0],""+columns[1]+"":r[1]}
            project.append(h)
        cur2.close()
        con.close()
        return project

    def All_Department_db():
        response=[]
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        
        cur.execute("SELECT distinct [employee_department_id],[employee_department_name] FROM [users].[tbl_employee_department] where is_active=1 and is_deleted=0 and is_oprt=1")
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1]}
            response.append(h)
        cur.commit()
        cur.close()
        con.close()       
        return response

    def GetAllSalesCategory():
        response = []
        h={}
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()
        cur2.execute("exec [masters].[sp_get_sales_category]")
        columns = [column[0].title() for column in cur2.description]
        for row in cur2:
            for i in range(len(columns)):
                h[columns[i]]=row[i]           
            response.append(h.copy())
        cur2.close()
        con.close()
        return response

    
    def Get_all_Customer_Group_db(customer_group_id):
        response=[]
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [masters].[sp_get_all_customer_group]  ?'
        values = (customer_group_id,)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1]}
            response.append(h)
        cur.commit()
        cur.close()
        con.close()     
        return response

    def GetAllCategoryTypes():
        response = []
        h={}
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()
        cur2.execute("exec [masters].[sp_get_category_type]")
        columns = [column[0].title() for column in cur2.description]
        for row in cur2:
            for i in range(len(columns)):
                h[columns[i]]=row[i]           
            response.append(h.copy())
        cur2.close()
        con.close()
        return response

    def GetSubProjectsForCenter(center_id):
        response = []
        h={}
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()
        sql = 'exec [masters].[sp_get_sub_projects_for_center]  ?'
        values = (center_id,)
        cur2.execute(sql,(values))
        columns = [column[0].title() for column in cur2.description]
        for row in cur2:
            for i in range(len(columns)):
                h[columns[i]]=row[i]           
            response.append(h.copy())
        cur2.close()
        con.close()
        return response
        con.close()       
        return response
    def GetBatchDetailsAssessment(batch_code):
        response = []
        h={}
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()
        sql = 'exec [batches].[sp_get_batch_details_for_assessment]  ?'
        values = (batch_code,)
        #print(values)
        cur2.execute(sql,(values))
        columns = [column[0].title() for column in cur2.description]
        for row in cur2:
            for i in range(len(columns)):
                h[columns[i]]=row[i]           
            response.append(h.copy())
        cur2.close()
        con.close()
        return response
               
    def GetSubProjectsForCenter_course(user_id,user_role_id,center_id, course_id, sub_project_id):
        response = []
        h={}
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()
        sql = 'exec [masters].[sp_get_sub_projects_for_center_course]  ?,?,?, ?, ?'
        values = (user_id,user_role_id,center_id, course_id, sub_project_id)
        cur2.execute(sql,(values))
        columns = [column[0].title() for column in cur2.description]
        for row in cur2:
            for i in range(len(columns)):
                h[columns[i]]=row[i]           
            response.append(h.copy())
        cur2.close()
        con.close()
        #print(response)
        return response
        con.close()       
        return response
    def Get_all_Entity_db():
        response=[]
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [masters].[get_all_entity]'
        cur.execute(sql)
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1]}
            response.append(h)
        cur.commit()
        cur.close()
        con.close()       
        return response

    def Get_all_Project_Group_db():
        response=[]
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [masters].[get_all_group]'
        cur.execute(sql)
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1]}
            response.append(h)
        cur.commit()
        cur.close()
        con.close()       
        return response
    
    def Get_all_Block_db():
        response=[]
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [masters].[get_all_block]'
        cur.execute(sql)
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1]}
            response.append(h)
        cur.commit()
        cur.close()
        con.close()       
        return response

    def Get_all_Product_db():
        response=[]
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [masters].[get_all_product]'
        cur.execute(sql)
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1]}
            response.append(h)
        cur.commit()
        cur.close()
        con.close()       
        return response

    def Get_all_Center_db(user_id,user_role_id):
        response=[]
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [masters].[get_all_Center] ?,?'
        values=(user_id,user_role_id)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1]}
            response.append(h)
        cur.commit()
        cur.close()
        con.close()       
        return response

    def GetContractbycustomer_db(Customer_Id):
        response=[]
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [masters].[sp_GetContractbycustomer]  ?'
        values = (Customer_Id,)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[3]+"":row[3],""+columns[4]+"":row[4],""+columns[9]+"":row[9]}
            response.append(h)

        out = {'contracts':response,'Customer_Name':row[5],'Funding_Source':row[6],'Customer_Group':row[7],'Industry_type':row[8]}
        cur.commit()
        cur.close()
        con.close()       
        return out

    def Getsubprojectbyproject_db(Project_Id):
        response=[]
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [masters].[sp_Getsubprojectbyproject]  ?'
        values = (Project_Id,)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2], ""+columns[3]+"":row[3],""+columns[4]+"":row[4],""+columns[5]+"":row[5],""+columns[6]+"":row[6],""+columns[10]+"":row[10]}
            response.append(h)

        out = {'sub_project':response,'project_name':row[7],'project_code':row[8],'project_id':row[9]}
        cur.commit()
        cur.close()
        con.close()       
        return out

    def get_subproject_basedon_proj_multiple(user_id,user_role_id,project_id):
        courses = []
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()

        sql = 'exec [masters].[sp_get_sub_projects_based_on_projects] ?,?,?'
        values=(user_id,user_role_id,project_id)
        cur2.execute(sql,(values))
        columns = [column[0].title() for column in cur2.description]
        for r in cur2:
            h = {""+columns[0]+"":r[0],""+columns[1]+"":r[1]}
            courses.append(h)
        cur2.close()
        con.close()
        return courses

    def get_batches_basedon_sub_proj_multiple(user_id,user_role_id,sub_project_id):
        Batches = []
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()

        sql = 'exec [masters].[sp_get_batches_based_on_sub_projects] ?,?,?'
        values=(user_id,user_role_id,sub_project_id)
        print(values)
        cur2.execute(sql,(values))
        columns = [column[0].title() for column in cur2.description]
        for r in cur2:
            h = {""+columns[0]+"":r[0],""+columns[1]+"":r[1]}
            Batches.append(h)
        cur2.close()
        con.close()
        #print(Batches)
        return Batches


    def Get_all_industry_db():
        response=[]
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'SELECT distinct [industry_type_id], [industry_type_name] FROM [masters].[tbl_industry_type] where is_deleted=0'
        cur.execute(sql)
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1]}
            response.append(h)
        cur.commit()
        cur.close()
        con.close()       
        return response
    
    def GetProjectsForCourse(CourseId):
        response=[]
        h={}
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [masters].[sp_get_projects_for_course]  ?'
        values = (CourseId,)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            for i in range(len(columns)):
                h[columns[i]]=row[i]
            response.append(h.copy())
        out = {'Projects':response}
        cur.commit()
        cur.close()
        con.close()       
        return out

    def GetSubProjectsForCourse(CourseId):
        response=[]
        h={}
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [masters].[sp_get_sub_projects_for_course] ?'
        values = (CourseId,)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            for i in range(len(columns)):
                h[columns[i]]=row[i]
            response.append(h.copy())
        out = {'Projects':response}
        cur.commit()
        cur.close()
        con.close()       
        return out

    def GetCourseVariantsForCourse(CourseId):
        response=[]
        h={}
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [masters].[sp_get_course_variants_for_course] ?'
        values = (CourseId,)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            for i in range(len(columns)):
                h[columns[i]]=row[i]
            response.append(h.copy())
        out = {'CourseVariants':response}
        cur.commit()
        cur.close()
        con.close()       
        return out
    def GetCentersForCourse(CourseId):
        response=[]
        h={}
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [masters].[sp_get_centers_for_course] ?'
        values = (CourseId,)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            for i in range(len(columns)):
                h[columns[i]]=row[i]
            response.append(h.copy())
        out = {'Centers':response}
        cur.commit()
        cur.close()
        con.close()
        return out
    def GetBatchAssessments(BatchId,Stage):
        response=[]
        h={}
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [assessments].[get_batch_assessments] ?,?'
        values = (BatchId,Stage)
        print(values)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            for i in range(len(columns)):
                h[columns[i]]=row[i]
            response.append(h.copy())
        out = {'Assessments':response}
        cur.commit()
        cur.close()
        con.close()       
        return out

    def GetBatchAssessmentsHistory(AssessentId):
        response=[]
        h={}
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [assessments].[get_batch_assessments_history] ?'
        values = (AssessentId,)
        print("Hii")
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            for i in range(len(columns)):
                h[columns[i]]=row[i]
            response.append(h.copy())
        out = {'Assessments':response}
        cur.commit()
        cur.close()
        con.close()   
        print(response)    
        return out


    def Get_all_ProjectType_db():
        response=[]
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [masters].[get_all_ProjectType]'
        cur.execute(sql)
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1]}
            response.append(h)
        cur.commit()
        cur.close()
        con.close()       
        return response

    @classmethod
    def AllCourse_center_db(cls, user_id,user_role_id,center_id):
        response=[]
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [masters].[sp_course_basedon_center] ?,?,?'
        values = (user_id,user_role_id,center_id, )
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1]}
            response.append(h)
        cur.commit()
        cur.close()
        con.close()       
        return response

    def GetAssessmentTypes():
        response=[]
        h={}
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [assessments].[sp_get_assessment_types]'
        #values = (BatchId,)
        cur.execute(sql)
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            for i in range(len(columns)):
                h[columns[i]]=row[i]
            response.append(h.copy())
        out = {'AssessmentTypes':response}
        cur.commit()
        cur.close()
        con.close()       
        return out
    def GetAssessmentAgency():
        response=[]
        h={}
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [assessments].[sp_get_assessment_agency] '
        cur.execute(sql)
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            for i in range(len(columns)):
                h[columns[i]]=row[i]
            response.append(h.copy())
        out = {'AssessmentAgency':response}
        cur.close()
        con.close()       
        return out
    def ScheduleAssessment(batch_id,user_id,requested_date,scheduled_date,assessment_date,assessment_type_id,assessment_agency_id,assessment_id,partner_id,current_stage_id,present_candidate,absent_candidate,assessor_name,assessor_email,assessor_mobile,reassessment_flag):
        try:
            response=[]
            h={}
            con = pyodbc.connect(conn_str)
            cur = con.cursor()
            sql = 'exec [assessments].[sp_add_edit_batch_assessment] ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?'
            values = (batch_id,user_id,requested_date,scheduled_date,assessment_date,assessment_type_id,assessment_agency_id,assessment_id,partner_id,current_stage_id,present_candidate,absent_candidate,assessor_name,assessor_email,assessor_mobile,reassessment_flag)
            cur.execute(sql,(values))
            columns = [column[0].title() for column in cur.description]
            for row in cur:
                pop=row[0]
                msg=row[1]
            cur.commit()
            
            if pop>0:
                out={"message":msg,"success":1,"assessment_id":pop}
                print(str(partner_id),str(assessment_type_id),msg)
                if((str(partner_id)=="1") & (str(assessment_type_id)=="2") & ((msg=='Assessment Proposed') | (msg=='Re-Assessment Proposed'))):
                    SDMSBatchId=''
                    Stage=''
                    AssessmentDate=''
                    BatchAttemptNumber=''
                    sql = '''select TOP(1) b.batch_code,ba.assessment_stage_id as assessment_stage,CONVERT(varchar,FORMAT(ba.requested_date,'dd-MMM-yyyy'),106) as requested_date,ba.attempt  
                             from batches.tbl_batches as b 
                             left join assessments.tbl_batch_assessments as ba on ba.batch_id=b.batch_id
                            where b.is_active=1
                            AND ba.assessment_type_id=2
                            AND b.batch_id='''+batch_id
                    cur.execute(sql)
                    columns = [column[0].title() for column in cur.description]
                    for row in cur:
                        SDMSBatchId=str(row[0])
                        Stage=str(row[1])
                        AssessmentDate=str(row[2])
                        BatchAttemptNumber=str(row[3])
                    #if BatchAttemptNumber != '1':
                        #present_candidate = absent_candidate
                    center_name=''
                    course_name=row=''
                    customer_name=row=''
                    cm_emails=''
                    sql2 = 'exec [batches].[sp_get_batch_detail_for_assessment_mail] ?'
                    values = (batch_id,)
                    cur.execute(sql2,(values))
                    
                    for row in cur:
                        center_name=row[0]
                        course_name=row[1]
                        customer_name=row[2]
                        cm_emails=row[3]
                        #print(cm_emails)
                        cm_emails=','.join(set(cm_emails.split(',')))
                        #print(cm_emails)
                    sql = 'exec [candidate_details].[sp_get_candidate_details_for_assessment_UAP] ?,?,?'
                    values = (batch_id,pop,present_candidate)
                    cur.execute(sql,(values))
                    columns = [column[0].title() for column in cur.description]
                   
                    for row in cur:
                        for i in range(len(columns)):
                            h[columns[i]]=row[i]
                        response.append(h.copy())
                    uap_url=''
                    params={"SDMSBatchId":SDMSBatchId,"CenterName":center_name,"CourseName":course_name,"ClientName":customer_name,"CMEmails":cm_emails,"NeoBatchStage":Stage,"AssessmentDate":AssessmentDate,"BatchAttemptNumber":BatchAttemptNumber,"CandidateList":response}
                    json_data = json.dumps(params)   
                    uap_api=UAP_API_BASE_URL + 'CreateNeoSkillsBatchJSONRequest?JSONRequest='+json_data
                    x = requests.get(uap_api)
                    data = x.json()
                    if 'CreateNeoSkillsBatch' in data:
                        if  str(data['CreateNeoSkillsBatch']['Succsess']) == "True":
                            attachment_file=Database.create_assessment_candidate_file(response,columns,SDMSBatchId,'assessment')
                            #print(cm_emails)
                            status_mail=sent_mail.UAP_Batch_Creation_MAIL(str(data['CreateNeoSkillsBatch']['RequestId']),SDMSBatchId,requested_date,center_name,course_name,customer_name,cm_emails,attachment_file)                 
                            if(status_mail['status']==False):
                                out={"message":status_mail['description'],"success":0,"assessment_id":pop}
                                return out
                        
            
            else:
                out={"message":"Error scheduling assessment","success":0,"assessment_id":pop}
            cur.close()
            con.close()
            return out
        except Exception as e:
            return {"message":"Error changing assessment stage"+e.message,"success":0,"assessment_id":0}
    def create_assessment_candidate_file(data,columns,batch_code,file_type):
        try:
            import pandas as pd
            import pypyodbc as pyodbc
            import xlsxwriter
            import calendar
            import time
            from Database import config
        except:
            return({'Description':'Module Error', 'Status':False})

        try:
            gmt = time.gmtime() 
            ts = calendar.timegm(gmt)
            r=re.compile("Candidate_List_.*")
            lst=os.listdir(config.neo_report_file_path + 'report file/')
            newlist = list(filter(r.match, lst))
            for i in newlist:
                os.remove( config.neo_report_file_path + 'report file/' + i) 
            if file_type=='assessment':
                name_withpath = config.neo_report_file_path + 'report file/'+ 'Candidate_List_Assessment_'+batch_code+str(ts)+'.xlsx'
            if file_type=='certification':
                name_withpath = config.neo_report_file_path + 'report file/'+ 'Candidate_List_Certification_'+batch_code+str(ts)+'.xlsx'
            writer = pd.ExcelWriter(name_withpath, engine='xlsxwriter')
            workbook  = writer.book

            header_format = workbook.add_format({
                'bold': True,
                #'text_wrap': True,
                'valign': 'center',
                'fg_color': '#D7E4BC',
                'border': 1})
            #data = list(map(lambda x:list(x), data))
            #print(len(data))
            df = pd.DataFrame(data, columns=columns)
            if file_type=='assessment':
                df = df[['Candidateid','Candidatename','Enrollmentnumber','Fathername','Emailid','Candidateattemptnumber']]
                columns = ['CandidateId','CandidateName','EnrollmentNumber','FatherName','EmailId','CandidateAttemptNumber']
            if file_type=='certification':
                df = df[['Candidateid','Candidatename','Enrollmentnumber','Fathername','Emailid']]
                columns = ['CandidateId','CandidateName','EnrollmentNumber','FatherName','EmailId']
            
            df.to_excel(writer, index=None, header=None ,startrow=1 ,sheet_name='Candidates') 
            worksheet = writer.sheets['Candidates']

            for col_num, value in enumerate(columns):
                worksheet.write(0, col_num, value, header_format)

                            
            writer.save()
            return(name_withpath)
            
        except Exception as e:
            print("Exc"+str(e))
            return(str(e))
    def ChangeCertificationStage(batch_id,batch_code,user_id,current_stage_id,enrollment_ids,sent_printing_date,sent_center_date,expected_arrival_date,received_date,planned_distribution_date,actual_distribution_date,cg_name,cg_desig,cg_org,cg_org_loc):
        try:
            response=[]
            h={}
            con = pyodbc.connect(conn_str)
            cur = con.cursor()
            sql = 'exec [assessments].[sp_change_certification_stage] ?,?,?,?,?,?,?,?,?,?,?,?,?,?'
            values = (batch_id,user_id,current_stage_id,enrollment_ids,sent_printing_date,sent_center_date,expected_arrival_date,received_date,planned_distribution_date,actual_distribution_date,cg_name,cg_desig,cg_org,cg_org_loc)
            cur.execute(sql,(values))
            columns = [column[0].title() for column in cur.description]
            for row in cur:
                pop=row[0]
                msg=row[1]
            cur.commit()
            
            if pop>0:
                if(pop==2):
                    user_mail_id_cc=''
                    user_mail_id_to=''
                    user_name_to=''
                    sql = '''
                          select top(1) coalesce(first_name,'Team'),coalesce(email,'do-not-reply@labournet.in') from users.tbl_user_details where user_id=
                                                    (select top(1) created_by as stage_changed_by 
                                                    from assessments.tbl_map_certification_candidates_stages_revision_history 
                                                    where assessment_id = (select TOP(1) assessment_id 
                                                                            from assessments.tbl_batch_assessments
                                                                            where batch_id='''+ str(batch_id)+''' and assessment_type_id=2
                                                                            and assessment_stage_id=4
                                                                            order by assessment_id desc
                                                                            )
                                                    AND certification_stage_id=1)
                            AND is_active=1;'''
                    cur.execute(sql)
                    for row in cur:
                        user_name_to=row[0]
                        user_mail_id_to=row[1]
                    sql = 'select top(1) email from users.tbl_user_details where user_id='+ str(user_id) +' and is_active=1'
                    cur.execute(sql)
                    for row in cur:
                        user_mail_id_cc=row[0]
                    sql = 'exec [candidate_details].[sp_get_candidate_details_for_certification] ?,?'
                    values = (batch_id,enrollment_ids)
                    cur.execute(sql,(values))
                    columns = [column[0].title() for column in cur.description]                   
                    for row in cur:
                        for i in range(len(columns)):
                            h[columns[i]]=row[i]
                        response.append(h.copy())
                    attachment_file=Database.create_assessment_candidate_file(response,columns,batch_code,'certification')
                    sent_mail.certification_stage_change_mail(2,user_mail_id_to,user_name_to,user_mail_id_cc,batch_code,attachment_file)
                if(pop==3):
                    user_mail_id_cc=''
                    user_mail_id_to=''
                    user_name_to=''
                    sql = '''
                            select top(1) coalesce(first_name,'Team'),coalesce(email,'do-not-reply@labournet.in') from users.tbl_user_details where user_id in 
                                        (select u.user_id from masters.tbl_map_sub_project_user as u
                                        inner join users.tbl_map_User_UserRole as urr on urr.user_id=u.user_id
                                        and urr.user_role_id =5
                                        where sub_project_id=(select sub_project_id from batches.tbl_batches where batch_id='''+ batch_id +''')
                                        AND u.is_active=1
                                        )
                            ANd is_active=1;
                          '''
                    cur.execute(sql)
                    for row in cur:
                        user_name_to=row[0]
                        user_mail_id_to=row[1]
                    sql = 'select top(1) email from users.tbl_user_details where user_id='+ str(user_id) +' and is_active=1'
                    cur.execute(sql)
                    for row in cur:
                        user_mail_id_cc=row[0]
                    sql = 'exec [candidate_details].[sp_get_candidate_details_for_certification] ?,?'
                    values = (batch_id,enrollment_ids)
                    cur.execute(sql,(values))
                    columns = [column[0].title() for column in cur.description]                   
                    for row in cur:
                        for i in range(len(columns)):
                            h[columns[i]]=row[i]
                        response.append(h.copy())
                    attachment_file=Database.create_assessment_candidate_file(response,columns,batch_code,'certification')
                    sent_mail.certification_stage_change_mail(3,user_mail_id_to,user_name_to,user_mail_id_cc,batch_code,attachment_file)
                if(pop==4):
                    user_mail_id_cc=''
                    user_mail_id_to=''
                    user_name_to=''
                    sql = '''
                            select top(1) coalesce(first_name,'Team'),coalesce(email,'do-not-reply@labournet.in') from users.tbl_user_details where user_id=
                                                    (select top(1) assigned_to as logistic_user 
                                                    from assessments.tbl_map_certification_candidates_stages_revision_history 
                                                    where assessment_id = (select TOP(1) assessment_id 
                                                                            from assessments.tbl_batch_assessments
                                                                            where batch_id='''+ str(batch_id)+''' and assessment_type_id=2
                                                                            and assessment_stage_id=4
                                                                            order by assessment_id desc
                                                                            )
                                                    AND certification_stage_id=1)
                            AND is_active=1;
                          '''
                    cur.execute(sql)
                    for row in cur:
                        user_name_to=row[0]
                        user_mail_id_to=row[1]
                    sql = 'select top(1) email from users.tbl_user_details where user_id='+ str(user_id) +' and is_active=1'
                    cur.execute(sql)
                    for row in cur:
                        user_mail_id_cc=row[0]
                    sql = 'exec [candidate_details].[sp_get_candidate_details_for_certification] ?,?'
                    values = (batch_id,enrollment_ids)
                    cur.execute(sql,(values))
                    columns = [column[0].title() for column in cur.description]                   
                    for row in cur:
                        for i in range(len(columns)):
                            h[columns[i]]=row[i]
                        response.append(h.copy())
                    attachment_file=Database.create_assessment_candidate_file(response,columns,batch_code,'certification')
                    sent_mail.certification_stage_change_mail(4,user_mail_id_to,user_name_to,user_mail_id_cc,batch_code,attachment_file)
                if(pop==5):
                    user_mail_id_cc=''
                    user_mail_id_to=''
                    user_name_to=''
                    sql = '''
                            select top(1) coalesce(first_name,'Team'),coalesce(email,'do-not-reply@labournet.in') from users.tbl_user_details where user_id=
                                                    (select top(1) created_by as amt_user 
                                                    from assessments.tbl_map_certification_candidates_stages_revision_history 
                                                    where assessment_id = (select TOP(1) assessment_id 
                                                                            from assessments.tbl_batch_assessments
                                                                            where batch_id='''+ str(batch_id)+''' and assessment_type_id=2
                                                                            and assessment_stage_id=4
                                                                            order by assessment_id desc
                                                                            )
                                                    AND certification_stage_id=1)
                            AND is_active=1;
                          '''
                    cur.execute(sql)
                    for row in cur:
                        user_name_to=row[0]
                        user_mail_id_to=row[1]
                    sql = 'select top(1) email from users.tbl_user_details where user_id='+ str(user_id) +' and is_active=1'
                    cur.execute(sql)
                    for row in cur:
                        user_mail_id_cc=row[0]
                    sql = 'exec [candidate_details].[sp_get_candidate_details_for_certification] ?,?'
                    values = (batch_id,enrollment_ids)
                    cur.execute(sql,(values))
                    columns = [column[0].title() for column in cur.description]                   
                    for row in cur:
                        for i in range(len(columns)):
                            h[columns[i]]=row[i]
                        response.append(h.copy())
                    attachment_file=Database.create_assessment_candidate_file(response,columns,batch_code,'certification')
                    sent_mail.certification_stage_change_mail(5,user_mail_id_to,user_name_to,user_mail_id_cc,batch_code,attachment_file)
                if(pop==6):
                    user_mail_id_cc=''
                    user_mail_id_to=''
                    user_name_to=''
                    sql = '''
                            select top(1) coalesce(first_name,'Team'),coalesce(email,'do-not-reply@labournet.in') from users.tbl_user_details where user_id=
                                                    (select top(1) created_by as amt_user 
                                                    from assessments.tbl_map_certification_candidates_stages_revision_history 
                                                    where assessment_id = (select TOP(1) assessment_id 
                                                                            from assessments.tbl_batch_assessments
                                                                            where batch_id='''+ str(batch_id)+''' and assessment_type_id=2
                                                                            and assessment_stage_id=4
                                                                            order by assessment_id desc
                                                                            )
                                                    AND certification_stage_id=1)
                            AND is_active=1;
                          '''
                    cur.execute(sql)
                    for row in cur:
                        user_name_to=row[0]
                        user_mail_id_to=row[1]
                    sql = 'select top(1) email from users.tbl_user_details where user_id='+ str(user_id) +' and is_active=1'
                    cur.execute(sql)
                    for row in cur:
                        user_mail_id_cc=row[0]
                    sql = 'exec [candidate_details].[sp_get_candidate_details_for_certification] ?,?'
                    values = (batch_id,enrollment_ids)
                    cur.execute(sql,(values))
                    columns = [column[0].title() for column in cur.description]                   
                    for row in cur:
                        for i in range(len(columns)):
                            h[columns[i]]=row[i]
                        response.append(h.copy())
                    attachment_file=Database.create_assessment_candidate_file(response,columns,batch_code,'certification')
                    sent_mail.certification_stage_change_mail(6,user_mail_id_to,user_name_to,user_mail_id_cc,batch_code,attachment_file)
                
                
                out={"message":msg,"success":1}
            else:
                out={"message":"Error changing in stage","success":0}
            cur.close()
            con.close()
            return out
        except Exception as e:
            return {"message":"Error changing assessment stage"+e.message,"success":0,"assessment_id":0}
    
    def GetAssessmentCandidateResults(AssessmentId):
        try:
            col=[]
            response={}
            con = pyodbc.connect(conn_str)
            cur = con.cursor()
            sql = 'exec [assessments].[sp_get_candidate_result] ?'
            values=(AssessmentId,)  
            print(values)          
            cur.execute(sql,(values))
            col = [column[0].title() for column in cur.description]
            data=cur.fetchall()   
            out = []
            for i in data:
                out.append(list(i))        
            df=pd.DataFrame(out)       
            cur.close()
            con.close()
            response= {"columns":col,"data":df}
            print(response)
            return response
        except Exception as e:
            print(str(e))
        return out

    def PMT_Department_user_db():
        response=[]
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [users].[sp_get_PMT_Dept]'
        cur.execute(sql)
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1]}
            response.append(h)

        out = {"PMT_Dept_role":response}
        #cur.commit()
        cur.close()
        con.close()       
        return out

    def sales_Department_user_db():
        response=[]
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [users].[sales_Department_user_db]'
        cur.execute(sql)
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1]}
            response.append(h)

        out = {"sales_Department_role":response}
        #cur.commit()
        cur.close()
        con.close()        
        return out


    def Getstatebasedonregion_db(region_id):
        response=[]
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'select state_id, state_name from masters.tbl_states where is_active=1 and region_id ='+str(region_id)
        cur.execute(sql)
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1]}
            response.append(h)

        out = {"state":response}
        #cur.commit()
        cur.close()
        con.close()       
        return out
    
    def Getcenterbasedonstate_db(state_id):
        response=[]
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'select center_id, center_name from masters.tbl_center where is_active=1 and state_id='+str(state_id)
        cur.execute(sql)
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1]}
            response.append(h)

        out = {"center":response}
        #cur.commit()
        cur.close()
        con.close()       
        return out

    def Getcoursebasedoncenter_db(center_ids,project_code):
        response=[]
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [masters].[sp_course_basedon_center_project] ?, ?'
        values=(center_ids,project_code)      
        print(values)  
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1]}
            response.append(h)

        out = {"course":response}
        #cur.commit()
        cur.close()
        con.close()       
        return out
      
    def my_project_list(user_id,user_role_id,user_region_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        content = {}
        d = []
        h={}
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [masters].[sp_get_my_project_list] ?, ?, ?, ?, ?, ?, ?, ?'
        values = (user_id,user_role_id,user_region_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        record="0"
        fil="0"
        for row in cur:
            record=row[len(columns)-1]
            fil=row[len(columns)-2]
            for i in range(len(columns)-2):
                h[columns[i]]=row[i]
            d.append(h.copy())
        content = {"draw":draw,"recordsTotal":record,"recordsFiltered":fil,"data":d}
        cur.close()
        con.close()
        return content
    def GetCoursesForCenter(center_id):
        response = []
        h={}
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()
        sql = 'exec [masters].[sp_get_courses_for_center]  ?'
        values = (center_id,)
        cur2.execute(sql,(values))
        columns = [column[0].title() for column in cur2.description]
        for row in cur2:
            for i in range(len(columns)):
                h[columns[i]]=row[i]           
            response.append(h.copy())
        cur2.close()
        con.close()
        return response
        con.close()       
        return response
    
    def GetCoursesForProject(project_id):
        response = []
        h={}
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()
        sql = 'exec [masters].[sp_get_courses_for_project]  ?'
        values = (project_id,)
        cur2.execute(sql,(values))
        columns = [column[0].title() for column in cur2.description]
        for row in cur2:
            for i in range(len(columns)):
                h[columns[i]]=row[i]           
            response.append(h.copy())
        cur2.close()
        con.close()
        return response
        con.close()       
        return response
    def GetCentersForProject(project_id):
        response = []
        h={}
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()
        sql = 'exec [masters].[sp_get_centers_for_project]  ?'
        values = (project_id,)
        cur2.execute(sql,(values))
        columns = [column[0].title() for column in cur2.description]
        for row in cur2:
            for i in range(len(columns)):
                h[columns[i]]=row[i]           
            response.append(h.copy())
        cur2.close()
        con.close()
        return response
        con.close()       
        return response

    def Getcandidatebybatch_db(batch_id):
        response = []
        
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        h={}
        sql = 'exec [masters].[sp_Getcandidatebybatch]  ?'
        values = (batch_id,)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            for i in range(len(columns)):
                h[columns[i]]=row[i]
            #h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[3]+"":row[3],""+columns[4]+"":row[4],""+columns[5]+"":row[5],""+columns[6]+"":row[6]}
            response.append(h.copy())
        out = {"candidates":response,"batch_name":row[9],"center_name":row[10],"course_name":row[11]}
        cur.close()
        con.close() 
        return out
    def ALLCandidatesBasedOnCertifiactionStage(batch_id,stage_id):
        response = []
        
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        h={}
        sql = 'exec [assessments].[getcandidatesbasedoncertifiactionstage]  ?,?'
        values = (batch_id,stage_id)
        #print(values)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            for i in range(len(columns)):
                h[columns[i]]=row[i]
            #h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[3]+"":row[3],""+columns[4]+"":row[4],""+columns[5]+"":row[5],""+columns[6]+"":row[6]}
            response.append(h.copy())
        out = {"Candidates":response}
        cur.close()
        con.close() 
        #print(response)
        return out
    
    def CandidateFamilyDetails(candidate_id):
        response = []
        
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        h={}
        sql = 'exec [candidate_details].[sp_get_candidate_family_details]  ?'
        values = (candidate_id,)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            for i in range(len(columns)):
                h[columns[i]]=row[i]
            #h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[3]+"":row[3],""+columns[4]+"":row[4],""+columns[5]+"":row[5],""+columns[6]+"":row[6]}
            response.append(h.copy())
        out = {"Members":response}
        cur.close()
        con.close() 
        #print(out)      
        return out
    def GetSubProjectsForuser(user_id):
        response = []
        h={}
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()
        sql = 'exec [users].[sp_get_sub_projects_for_user]  ?'
        values = (user_id,)
        cur2.execute(sql,(values))
        columns = [column[0].title() for column in cur2.description]
        for row in cur2:
            for i in range(len(columns)):
                h[columns[i]]=row[i]           
            response.append(h.copy())
        cur2.close()
        con.close()
        return response
    
    def GetSubProjectsForRegionUser(user_id,user_role_id,region_id):
        response = []
        h={}
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()
        sql = 'exec [masters].[sp_get_sub_projects_for_regionuser]  ?,?,?'
        values = (user_id,user_role_id,region_id)
        cur2.execute(sql,(values))
        columns = [column[0].title() for column in cur2.description]
        for row in cur2:
            for i in range(len(columns)):
                h[columns[i]]=row[i]           
            response.append(h.copy())
        cur2.close()
        con.close()
        return response

    def GetECPReportData(user_id,user_role_id,customer_ids,contract_ids,region_ids,from_date,to_date):
        response = []
        h={}
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()
        sql = 'exec [reports].[sp_get_ecp_report_data ]  ?,?,?,?,?,?,?'
        values = (user_id,user_role_id,customer_ids,contract_ids,region_ids,from_date,to_date)
        #print(values)
        cur2.execute(sql,(values))
        columns = [column[0].title() for column in cur2.description]
        for row in cur2:
            for i in range(len(columns)):
                h[columns[i]]=row[i]           
            response.append(h.copy())
        cur2.close()
        con.close()
        return {"Data":response}
    def GetContractsBasedOnCustomer(user_id,user_role_id,customer_id):
        response = []
        h={}
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()
        sql = 'exec [masters].[sp_get_contracts_based_on_customer]  ?,?,?'
        values = (user_id,user_role_id,customer_id)
        #print(values)
        cur2.execute(sql,(values))
        columns = [column[0].title() for column in cur2.description]
        for row in cur2:
            for i in range(len(columns)):
                h[columns[i]]=row[i]           
            response.append(h.copy())
        cur2.close()
        con.close()
        return {"Contracts":response}

    def GetBillingMilestones():
        response = []
        h={}
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()
        sql = 'exec [masters].[get_billing_milestones] '        
        cur2.execute(sql)
        columns = [column[0].title() for column in cur2.description]
        for row in cur2:
            for i in range(len(columns)):
                h[columns[i]]=row[i]           
            response.append(h.copy())
        cur2.close()
        con.close()
        return response

    def GetUnitTypes():
        response = []
        h={}
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()
        sql = 'exec [masters].[get_unit_types]  '        
        cur2.execute(sql)
        columns = [column[0].title() for column in cur2.description]
        for row in cur2:
            for i in range(len(columns)):
                h[columns[i]]=row[i]           
            response.append(h.copy())
        cur2.close()
        con.close()
        return response
    def SaveProjectBillingMilestones(json_string,project_id,user_id):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec	[masters].[sp_store_project_milestone] ?, ?, ?'
        values = (json_string,project_id,user_id)
        cur.execute(sql,(values))
        for row in cur:
            pop=row[0]
        cur.commit()
        cur.close()
        con.close()
        if pop >0 :
            msg="Saved Successfully"
        else:
            msg="Error"
        return {"PopupMessage":msg,"RowCount":pop}
    def GetProjectMilestones(project_id):
        response = []
        h={}
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()
        sql = 'exec [masters].[sp_get_project_milestones] ?'  
        values=(project_id,)      
        cur2.execute(sql,(values))
        columns = [column[0].title() for column in cur2.description]
        for row in cur2:
            for i in range(len(columns)):
                h[columns[i]]=row[i]           
            response.append(h.copy())
        cur2.close()
        con.close()
        return response
    def GetSubProjectCourseMilestones(sub_project_id,course_id):
        response = []
        h={}
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()
        sql = 'exec [masters].[sp_get_sub_project_course_milestones] ?,?'  
        values=(sub_project_id,course_id)     
        cur2.execute(sql,(values))
        columns = [column[0].title() for column in cur2.description]
        for row in cur2:
            for i in range(len(columns)):
                h[columns[i]]=row[i]           
            response.append(h.copy())
        cur2.close()
        con.close()
        return response
    def SaveSubProjectCourseMilestones(json_string,sub_project_id,user_id):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec	[masters].[sp_store_sub_project_course_milestone] ?, ?, ?'
        values = (json_string,sub_project_id,user_id)
        cur.execute(sql,(values))
        for row in cur:
            pop=row[0]
        cur.commit()
        cur.close()
        con.close()
        if pop >0 :
            msg="Saved Successfully"
        else:
            msg="Error"
        return {"PopupMessage":msg,"RowCount":pop}
    def GetCoursesBasedOnSubProject(sub_project_id):
        response = []
        h={}
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()
        sql = 'exec [masters].[sp_get_courses_based_on_sub_project]  ?'
        values = (sub_project_id,)
        cur2.execute(sql,(values))
        columns = [column[0].title() for column in cur2.description]
        for row in cur2:
            for i in range(len(columns)):
                h[columns[i]]=row[i]           
            response.append(h.copy())
        cur2.close()
        con.close()
        return response
    def GetUsersBasedOnSubProject(sub_project_id):
        response = []
        h={}
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()
        sql = 'exec [masters].[sp_get_users_based_on_sub_project]  ?'
        values = (sub_project_id,)
        cur2.execute(sql,(values))
        
        columns = [column[0].title() for column in cur2.description]
        for row in cur2:
            for i in range(len(columns)):
                h[columns[i]]=row[i]           
            response.append(h.copy())
        cur2.close()
        con.close()
        #print(response)
        return response
    def GetUserListForSubProject(sub_project_id):
        response = []
        h={}
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()
        sql = 'exec [masters].[sp_get_user_list_for_sub_project]  ?'
        values = (sub_project_id,)
        cur2.execute(sql,(values))
        #print(values)
        #print(cur2.description)
        columns = [column[0].title() for column in cur2.description]
        for row in cur2:
            for i in range(len(columns)):
                h[columns[i]]=row[i]           
            response.append(h.copy())
        cur2.close()
        con.close()
        #print(response)
        return response
    def GetCentersbasedOnSubProject(sub_project_id):
        response = []
        h={}
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()
        sql = 'exec [masters].[sp_get_centers_based_on_sub_project]  ?'
        values = (sub_project_id,)
        cur2.execute(sql,(values))
        columns = [column[0].title() for column in cur2.description]
        for row in cur2:
            for i in range(len(columns)):
                h[columns[i]]=row[i]           
            response.append(h.copy())
        cur2.close()
        con.close()
        return response
    def GetTrainersBasedOnType(trainer_flag):
        response = []
        h={}
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()
        sql = 'exec [masters].[sp_get_trainers_based_on_type]  ?'
        values = (trainer_flag,)
        cur2.execute(sql,(values))
        columns = [column[0].title() for column in cur2.description]
        for row in cur2:
            for i in range(len(columns)):
                h[columns[i]]=row[i]           
            response.append(h.copy())
        cur2.close()
        con.close()
        return response
    def GetUsersBasedOnRole(user_role_id):
        response = []
        h={}
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()
        sql = 'exec [masters].[sp_get_users_based_on_role]  ?'
        values = (user_role_id,)
        #print(values)
        cur2.execute(sql,(values))
        columns = [column[0].title() for column in cur2.description]
        for row in cur2:
            for i in range(len(columns)):
                h[columns[i]]=row[i]           
            response.append(h.copy())
        cur2.close()
        con.close()
        #print(response)
        return response
    def GetUserRole():
        response = []
        h={}
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()
        sql = 'exec [masters].[sp_get_user_roles_for_sub_project_tagging] '
        cur2.execute(sql)
        columns = [column[0].title() for column in cur2.description]
        for row in cur2:
            for i in range(len(columns)):
                h[columns[i]]=row[i]           
            response.append(h.copy())
        cur2.close()
        con.close()
        #print(response)
        return response
    def SaveSubProjectCourseCenterUnitPrice(json_string,primary_key_id,user_id):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec	[masters].[sp_store_sub_project_course_center_unitrate]  ?, ?, ?'
        values = (json_string,primary_key_id,user_id)
        #print(values)
        cur.execute(sql,(values))
        for row in cur:
            pop=row[0]
        cur.commit()
        cur.close()
        con.close()
        if pop >0 :
            msg="Saved Successfully"
        else:
            msg="Error"
        return {"PopupMessage":msg,"RowCount":pop}
    def GetSubProjectCourseCenterUnitRates(sub_project_id,primary_key):
        response = []
        h={}
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()
        sql = 'exec  [masters].[sp_get_sub_projects_course_center_unitrates]  ?,?'
        values = (sub_project_id,primary_key)
        cur2.execute(sql,(values))
        columns = [column[0].title() for column in cur2.description]
        for row in cur2:
            for i in range(len(columns)):
                h[columns[i]]=row[i]           
            response.append(h.copy())
        cur2.close()
        con.close()
        return response

    def check_password(username,password,app_version,device_model,imei_num,android_version):
        conn = pyodbc.connect(conn_str)
        curs = conn.cursor()
        quer = "call users.sp_user_authentication_updated('{}','{}','{}','{}','{}','{}')".format(username,password,app_version,device_model,imei_num,android_version)
        quer = "{"+ quer + "}"
        curs.execute(quer)
        data = curs.fetchall()
        data = data[0]

        if str.lower(data[0]) =='false':
            return {'app_status':False, 'success': False, 'description': data[2]}
        elif str.lower(data[0]) =='true':
            if str.lower(data[1])=='false':
                return {'success': False, 'description': data[2],'app_status':True}
            elif str.lower(data[1])=='true':
                res=[]
                for i in range(len(data[3].split(','))):
                    res.append({'id':data[3].split(',')[i],'name':data[4].split(',')[i]})
                return {'app_status':True, 'success': True, 'description': data[2], 'user_role':res,'user_id':data[5],'user_name':data[6],'user_email':data[7]}
            else:
                return {'success': False, 'description': 'stored procedure not return true/false','app_status':True}
        else:
            return {'success': False, 'description': 'stored procedure not return true/false','app_status':False}
    
    def otp_send_db(otp, mobile_no, app_name, flag,candidate_id):
        conn = pyodbc.connect(conn_str)
        curs = conn.cursor()
        quer = "call [masters].[sp_mobile_otp_verification]('{}','{}',{},'{}',{})".format(mobile_no, otp, flag, app_name,candidate_id)
        quer = "{"+ quer + "}"
        curs.execute(quer)
        data = curs.fetchall()[0]
        curs.commit()
        curs.close()
        conn.close()
        return [data[0], data[2]]

    def otp_verification_db(otp, mobile_no, app_name,web_flag):
        conn = pyodbc.connect(conn_str)
        curs = conn.cursor()
        quer = "call [masters].[sp_to_verify_otp]('{}','{}','{}',{})".format(mobile_no, otp, app_name,web_flag)
        quer = "{"+ quer + "}"
        curs.execute(quer)
        data = curs.fetchall()[0]
        curs.commit()
        curs.close()
        conn.close()
        return data[0]

    def get_candidate_list_updated(user_id,role_id,cand_stage,app_version):
        conn = pyodbc.connect(conn_str)
        curs = conn.cursor()
        quer = "SELECT TOP (1) version_code FROM [masters].[tbl_mclg_app_version_history] order by id desc"
        curs.execute(quer)
        data=curs.fetchall()
        data = '' if data==[] else data[0][0]
        if int(app_version) < int(data):
            curs.close()
            conn.close()
            out = {'success': False, 'description': "Lower App Version", 'app_status':False}
            return out
        
        aws_location_full = ''
        if cand_stage==1:
            sql = 'exec [candidate_details].[sp_get_candidate_list_stage_M]  ?, ?, ?'
            filenmae = 'candidate_list_'+str(user_id) +'_'+ str(datetime.now().strftime('%Y%m%d_%H%M%S'))+'_M.xml'
            aws_location_full = aws_location+'neo_app/xml_files/'+'mobilization/' +filenmae
        elif cand_stage==2:
            sql = 'exec [candidate_details].[sp_get_candidate_list_stage_R]  ?, ?, ?'
            filenmae = 'candidate_list_'+str(user_id) +'_'+ str(datetime.now().strftime('%Y%m%d_%H%M%S'))+'_R.xml'
            aws_location_full = aws_location+'neo_app/xml_files/'+'registration/' +filenmae
        elif cand_stage==3:
            sql = 'exec [candidate_details].[sp_get_candidate_list_stage_E]  ?, ?, ?'
            filenmae = 'candidate_list_'+str(user_id) +'_'+ str(datetime.now().strftime('%Y%m%d_%H%M%S'))+'_E.xml'
            aws_location_full = aws_location+'neo_app/xml_files/'+'enrollment/' +filenmae
        else:
            out = {'success': False, 'description': "incorrect stage", 'app_status':True}
            return out
        
        values = (user_id,role_id,cand_stage)
        curs.execute(sql,(values))
        columns = [column[0].title() for column in curs.description]
        response = []
        h={}
        for row in curs:
            for i in range(len(columns)):
                h[columns[i]]=row[i]
            response.append(h.copy())
        df = pd.DataFrame(response)
        df = df.fillna('')

        curs.close()
        conn.close()
        df.to_xml(candidate_xmlPath + filenmae)
        
        #mobilization_types=Database.get_user_mobilization_type(user_id)
        #return {'success': True, 'description': "XML Created", 'app_status':True, 'filename':filenmae,'mobilization_types':mobilization_types}

        candidatexml_fullPath = candidate_xmlPath+filenmae
        api_url=COL_URL + "s3_signature?file_name="+aws_location_full+"&file_type=" + 'text/xml'
        requests.get(api_url)
        r = requests.get(api_url)
        json = r.json()
        
        json_data = json['data']
        data = json_data['fields']
        URL = json_data['url']
        raws=''
        with open(candidatexml_fullPath, 'r') as f:
            raws = requests.post(url = URL, data = data, files = {'file':(filenmae,f,'text/xml')})
        os.remove(candidatexml_fullPath)
        if (raws.status_code==200)or(raws.status_code==204):
            mobilization_types=Database.get_user_mobilization_type(user_id)
            out = {'success': True, 'description': "XML Created", 'app_status':True, 'filename':filenmae,'mobilization_types':mobilization_types}
        else:
            out = {'success': False, 'description': "Unable to upload to s3", 'app_status':True}
        return out

    def get_user_mobilization_type(user_id):
        conn = pyodbc.connect(conn_str)
        curs = conn.cursor()
        quer = "EXECUTE [masters].[sp_get_user_mobilization_types] ?"
        values=(user_id,)
        curs.execute(quer,(values))
        columns = [column[0].title() for column in curs.description]
        response = []
        h={}
        for row in curs:
            for i in range(len(columns)):
                h[columns[i]]=row[i]
            response.append(h.copy())
        curs.close()
        conn.close()
        return response

    def get_submit_candidate_mobi(user_id, role_id, xml, latitude, longitude, timestamp, app_version,device_model,imei_num,android_version):
        conn = pyodbc.connect(conn_str)
        curs = conn.cursor()
        quer = "SELECT TOP (1) version_code FROM [masters].[tbl_mclg_app_version_history] order by id desc"
        curs.execute(quer)
        data=curs.fetchall()
        data = '' if data==[] else data[0][0]
        if int(app_version) < int(data):
            curs.close()
            conn.close()
            out = {'success': False, 'description': "Lower App Version", 'app_status':False}
            return out
        try:
            '''
            insert into candidate_details.tbl_candidate_interventions
            (candidate_id,intervention_category,created_on,created_by,is_active)
            OUTPUT inserted.candidate_id
            values
            '''
            quer1 = '''
            insert into candidate_details.tbl_candidates
            (isFresher, salutation, first_name, middle_name, last_name, date_of_birth, isDob, age,primary_contact_no, secondary_contact_no, email_id, gender,marital_status, caste, disability_status, religion, source_of_information, present_pincode,present_district, permanent_district,permanent_pincode,candidate_stage_id, candidate_status_id, created_on, created_by, created_by_role_id, is_active, insert_from,permanent_state,permanent_country,present_state, present_country)
            OUTPUT inserted.candidate_id
            values
            '''
            quer2='''
            insert into candidate_details.tbl_candidate_reg_enroll_details
            (candidate_id,whatsapp_number,mother_tongue,current_occupation,average_annual_income,interested_course,product,candidate_photo,present_address_line1,permanaet_address_line1,created_on,created_by,is_active)
            values
            '''
            quer3='''
            insert into candidate_details.tbl_candidate_reg_enroll_non_mandatory_details
            (candidate_id,present_address_line2,present_village,present_panchayat,present_taluk_block,permanent_address_line2,permanent_village,permanent_panchayat,permanent_taluk_block,created_on,created_by,is_active)
            values
            '''
            #url = candidate_xml_weburl + xml
            url = download_aws_url+aws_location+'neo_app/xml_files/'+'mobilization/' +xml

            r = requests.get(url)
            data = r.text
            root = ET.fromstring(data)
            out = []
            
            for child in root:
                data = child.attrib
                out.append(data)
                #quer1_a + = 
                quer = "({},'{}','{}','{}','{}','{}',{},{},'{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}',1,2,GETDATE(),{},{},1,'m','{}','{}','{}','{}'),".format(1 if data['isFresher']=='true' else 0,data['candSaltn'],data['firstname'],data['midName'],data['lastName'],
                            data['candDob'],1 if data['dobEntered']=='true' else 0,data['candAge'],data['primaryMob'],data['secMob'],data['candEmail'],data['candGender'],data['maritalStatus'],data['candCaste'], data['disableStatus'], data['candReligion'],
                            data['candSource'], data['presPincode'],data['presDistrict'],data['permDistrict'],data['permPincode'],user_id,role_id,data['permState'],data['permCountry'] ,data['presState'],data['presCountry'])
                quer1 += '\n'+quer
            quer1 = quer1[:-1]+';'
            curs.execute(quer1)
            d = list(map(lambda x:x[0],curs.fetchall()))
            curs.commit()

            for i in range(len(d)):
                quer2 += '\n' + "({},'{}','{}','{}','{}','{}','{}','{}','{}','{}',GETDATE(),{},1),".format(d[i],out[i]['whatsapp_number'],out[i]['motherTongue'],out[i]['candOccuptn'],out[i]['annualIncome'],out[i]['interestCourse'],out[i]['candProduct'],out[i]['candPic'],out[i]['presAddrOne'],out[i]['permAddrOne'],user_id)
                quer3 += '\n' + "({},'{}','{}','{}','{}','{}','{}','{}','{}',GETDATE(),{},1),".format(d[i],out[i]['presAddrTwo'],out[i]['presVillage'],out[i]['presPanchayat'],out[i]['presTaluk'],out[i]['permAddrTwo'],out[i]['permVillage'],out[i]['permPanchayat'],out[i]['permTaluk'],user_id)
              
            quer2 = quer2[:-1]+';'
            quer3 = quer3[:-1]+';'
            curs.execute(quer2 + '\n' + quer3)
            curs.commit()
            out = {'success': True, 'description': "Submitted Successfully", 'app_status':True}
        except Exception as e:
            out = {'success': False, 'description': "error: "+str(e), 'app_status':True}
        finally:
            curs.close()
            conn.close()
            return out
    def get_submit_candidate_reg(user_id, role_id, xml, latitude, longitude, timestamp, app_version,device_model,imei_num,android_version):
        conn = pyodbc.connect(conn_str)
        curs = conn.cursor()
        quer = "SELECT TOP (1) version_code FROM [masters].[tbl_mclg_app_version_history] order by id desc"
        curs.execute(quer)
        data=curs.fetchall()
        data = '' if data==[] else data[0][0]
        if int(app_version) < int(data):
            curs.close()
            conn.close()
            out = {'success': False, 'description': "Lower App Version", 'app_status':False}
            return out
        
        try:
            quer1 = '''
            update candidate_details.tbl_candidates set isFresher={},isDob={},years_of_experience='{}',salutation='{}',first_name='{}',middle_name='{}',last_name='{}',date_of_birth='{}',age='{}',primary_contact_no='{}',secondary_contact_no='{}',email_id='{}',gender='{}',marital_status='{}',caste='{}',disability_status='{}',religion='{}',source_of_information='{}',candidate_stage_id=2,candidate_status_id=2,created_on=GETDATE(),created_by='{}',created_by_role_id='{}',is_active=1 where candidate_id='{}';
            '''
            quer2='''
            update candidate_details.tbl_candidate_reg_enroll_details set whatsapp_number='{}',candidate_photo='{}',mother_tongue='{}',current_occupation='{}',average_annual_income='{}',interested_course='{}',product='{}',aadhar_no='{}',identifier_type={},identity_number='{}',document_copy_image_name='{}',employment_type='{}',preferred_job_role='{}',relevant_years_of_experience='{}',current_last_ctc='{}',preferred_location='{}',willing_to_travel='{}',willing_to_work_in_shifts='{}',bocw_registration_id='{}',expected_ctc='{}',created_by='{}',aadhar_image_name='{}',created_on=GETDATE(),is_active=1 where candidate_id='{}';
            '''
            quer3 = '''
            update candidate_details.tbl_candidates set isFresher={}, project_type={},created_by='{}',is_active=1,created_on=getdate() where candidate_id='{}';
            '''
            
            insert_query_she='''
            INSERT INTO [candidate_details].[tbl_candidate_she_details]
                ([candidate_id]
                ,[mobilization_type]
                ,[score]
                ,[result]
                ,[Are you able to read and write local language?]
                ,[Do you have a smart phone?]
                ,[Are you willing to buy a smartphone?]
                ,[Do you own two wheeler?]
                ,[Are you willing to serve the community at this time of COVID-19 pandemic as Sanitization & Hygiene Entrepreneurs (SHE)?]
                ,[Are you willing to work and sign the work contract with LN?]
                ,[Are you willing to adopt digital transactions in your business?]
                ,[Have you availed any loan in the past?]
                ,[Do you have any active loan?]
                ,[Are you willing to take up a loan to purchase tools and consumables?]
                ,[Are you covered under any health insurance?]
                ,[Are you allergic to any chemicals and dust?]
                ,[Are you willing to follow  Environment, Health and Safety Norms in your business?]
                ,[Have you ever been subjected to any legal enquiry for Non ethical work/business?]
                ,[Date of birth (age between 18 to 40)]
                ,[Are you 8th Pass?]
                ,[Do you have any work experience in the past?]
                ,[Will you able to work full time or at least 6 hours a day?]
                ,[Are you willing to travel from one place to another within panchayat?]
                ,[Do you have a bank account?]
                ,[created_on]
                ,[created_by]
                ,[is_active])
            VALUES
            '''
            insert_query_dell='''
            INSERT INTO [candidate_details].[tbl_candidate_dell_details]
                ([candidate_id]
                ,[mobilization_type]
                ,[Educational Marksheet]
                ,[Aspirational District]
                ,[Income Certificate]
                ,[created_on]
                ,[created_by]
                ,[is_active])
            VALUES
            '''

            #url = candidate_xml_weburl + xml
            url = download_aws_url+aws_location+'neo_app/xml_files/'+'registration/' +xml    

            r = requests.get(url)
            data = r.text
            root = ET.fromstring(data)
            query = ""
            she_query=""
            dell_query=""
            for child in root:
                data = child.attrib
                aadhar_image_name=''
                if 'aadhar_image_name' in data:
                    aadhar_image_name=data['aadhar_image_name']
                if 'yrsExp' in data:
                    query += '\n' + quer1.format(1 if data['isFresher']=='true' else 0 ,1 if data['dobEntered']=='true' else 0,data['yrsExp'],data['candSaltn'],data['firstname'],data['midName'],data['lastName'],data['candDob'],data['candAge'],data['primaryMob'],data['secMob'],data['candEmail'],data['candGender'],data['maritalStatus'],data['candCaste'],data['disableStatus'],data['candReligion'],data['candSource'],user_id,role_id,data['cand_id'])
                if 'aadhaarNo' in data:
                    query += '\n' + quer2.format(data['whatsapp_number'],data['candPic'],data['motherTongue'],data['candOccuptn'],data['annualIncome'],data['interestCourse'],data['candProduct'],data['aadhaarNo'],data['idType'],data['idNum'],data['idCopy'],data['empType'],data['prefJob'],data['relExp'],data['lastCtc'],data['prefLocation'],data['willTravel'],data['workShift'],data['bocwId'],data['expectCtc'],user_id,aadhar_image_name,data['cand_id'])
                if int(data['mobilization_type'])==2:
                    she_query="({},{},{},{},'{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}',GETDATE(),{},1),".format(int(data['cand_id']),int(data['mobilization_type']),int(data['score']),int(data['result']),data['read_write_local_lang'],data['smart_phone'],data['buy_smart_phone'],data['own_two_wheeler'],data['serve_as_she'],data['sign_contract_with_LN'],data['adopt_digital_transaction'],data['any_loan'],data['active_loan'],data['loan_for_tools'],data['health_insurance'],data['allergic_to_chemicals'],data['follow_safety_norms'],data['subjected_to_legal_enq'],data['age_18_40'],data['eight_pass'],data['past_work_exp'],data['full_time_work'],data['trvl_within_panchayat'],data['bank_act'],user_id)
                    insert_query_she += '\n'+she_query
                if int(data['mobilization_type'])==4:
                    dell_query="({},{},'{}','{}','{}',GETDATE(),{},1),".format(int(data['cand_id']),int(data['mobilization_type']),data['edu_marsheet'],data['asp_district'],data['dell_income_certi'],user_id)
                    insert_query_dell += '\n'+dell_query
                query += '\n' + quer3.format(1 if data['isFresher']=='true' else 0,int(data['mobilization_type']) ,user_id,data['cand_id'])
                
            if query!="":     
                curs.execute(query)
                curs.commit()
            if she_query!="":
                insert_query_she=insert_query_she[:-1]+';'
                curs.execute(insert_query_she)
                curs.commit()
            if dell_query!="":
                insert_query_dell=insert_query_dell[:-1]+';'
                curs.execute(insert_query_dell)
                curs.commit()

            out = {'success': True, 'description': "Submitted Successfully", 'app_status':True}
        except Exception as e:
            out = {'success': False, 'description': "error: "+str(e), 'app_status':True}
        finally:
            curs.close()
            conn.close()
            return out
            
    def get_submit_candidate_enr(user_id, role_id, xml, latitude, longitude, timestamp, app_version,device_model,imei_num,android_version):
        conn = pyodbc.connect(conn_str)
        curs = conn.cursor()
        quer = "SELECT TOP (1) version_code FROM [masters].[tbl_mclg_app_version_history] order by id desc"
        curs.execute(quer)
        data=curs.fetchall()
        data = '' if data==[] else data[0][0]
        if int(app_version) < int(data):
            curs.close()
            conn.close()
            out = {'success': False, 'description': "Lower App Version", 'app_status':False}
            return out
        
        #url = candidate_xml_weburl + xml
        url = download_aws_url+aws_location+'neo_app/xml_files/'+'enrollment/' +xml   

        r = requests.get(url)
        data = r.text
        root = ET.fromstring(data)

        json_array = []
        for child in root:
            temp_data = child.attrib
            json_array.append({"Candidate_id":temp_data['cand_id'],"batch_id":temp_data['assign_batch']})
        
        sql = 'exec	[masters].[sp_validate_enrollment_m] ?'
        values = (json.dumps(json_array),)
        curs.execute(sql,(values))

        vali = curs.fetchall()[0][0]
        # vali ==0 means correct

        msg = """Sorry, You can't enroll new candidates to the batch.
        Note: The Actual Enrolment count has exceeded the Planned Target."""
        if vali==1:
            out = {'success': False, 'description': msg, 'app_status':True}
            return out
        elif vali==2:
            out = {'success': False, 'description': "Sorry, enrollment process has ended, you cannot enroll candidates to the batch.", 'app_status':True}
            return out

        try:
            # quer1 = '''
            # update candidate_details.tbl_candidates set isFresher={},project_type='{}',isDob={},salutation='{}',first_name='{}',middle_name='{}',last_name='{}',date_of_birth='{}',age='{}',primary_contact_no='{}',secondary_contact_no='{}',email_id='{}',gender='{}',marital_status='{}',caste='{}',disability_status='{}',religion='{}',source_of_information='{}',present_district='{}',present_state='{}',present_pincode='{}',present_country='{}',permanent_district='{}',permanent_state='{}',permanent_pincode='{}',permanent_country='{}',candidate_stage_id=3,candidate_status_id=2,created_on=GETDATE(),created_by='{}',created_by_role_id='{}', is_active=1 where candidate_id='{}';
            # '''
            quer2='''
            update candidate_details.tbl_candidate_reg_enroll_details set whatsapp_number='{}',candidate_photo='{}',mother_tongue='{}',current_occupation='{}',average_annual_income='{}',interested_course='{}',product='{}',present_address_line1='{}',permanaet_address_line1='{}',highest_qualification='{}',stream_specialization='{}',computer_knowledge='{}',technical_knowledge='{}',average_household_income='{}',bank_name='{}',account_number='{}',created_by='{}',created_on=GETDATE(),is_active=1 where candidate_id='{}';
            '''
            quer3='''
            update candidate_details.tbl_candidate_reg_enroll_non_mandatory_details set present_address_line2='{}',present_village='{}',present_panchayat='{}',present_taluk_block='{}',permanent_address_line2='{}',permanent_village='{}',permanent_panchayat='{}',permanent_taluk_block='{}',name_of_institute='{}',university='{}',year_of_pass='{}',percentage='{}',branch_name='{}',branch_code='{}',account_type='{}',attachment_image_name='{}',created_by='{}',created_on=GETDATE(),is_active=1 where candidate_id='{}';
            '''
            quer4='''
            insert into candidate_details.tbl_candidate_interventions
            (candidate_id,intervention_category,created_on,created_by,is_active)
            OUTPUT inserted.candidate_intervention_id
            values
            '''

            quer5='''
            insert into candidate_details.tbl_map_candidate_intervention_skilling
            (intervention_id, course_id, batch_id, intervention_value, created_on,created_by,is_active)
            values
            '''

            quer6='''
            INSERT INTO [candidate_details].[tbl_candidate_family_details]
                ([candidate_id]
                ,[salutation]
                ,[name]
                ,[family_date_of_birth]
                ,[family_age]
                ,[family_primary_contact]
                ,[family_email_address]
                ,[gender]
                ,[relationship]
                ,[education_qualification]
                ,[current_occupation]
                ,[created_by]
                ,[created_on]
                ,[is_active])
            VALUES
            '''
            quer7 = '''
            DELETE FROM [candidate_details].[tbl_candidate_family_details]  where candidate_id='{}';
            '''
            #to restrict ELS data to sync in shiksha
            quer8 = '''
            update candidate_details.tbl_map_candidate_intervention_skilling
            set    shiksha_sync_status=1 
            where batch_id in (	select batch_id 
					from batches.vw_batch_info 
					where bu_name='ELS'
				   );
            '''
            
            update_query_she='''
            UPDATE [candidate_details].[tbl_candidate_she_details] SET
                [Address as per Aadhar Card (incl pin code)]='{}'
                ,[Number of members earning in the family]='{}'
                ,[Rented or own house?]='{}'
                ,[Size of the house]='{}'
                ,[Ration card (APL or BPL)]='{}'
                ,[TV]='{}'
                ,[Refrigerator]='{}'
                ,[Washing Machine]='{}'
                ,[AC /Cooler]='{}'
                ,[Car]='{}'                
                ,[Medical Insurance]='{}'
                ,[Life Insurance]='{}'
                ,[Others]='{}'
                ,[Educational qualification]='{}'
                ,[Age proof]='{}'
                ,[Signed MoU]='{}'
                ,[MoU signed date]='{}'
                ,[Kit given date]='{}'
                ,[Head of the household]='{}'
                ,[Farm land]='{}'
                ,[If yes, acres of land]='{}'
                ,[created_on]=GETDATE()
                ,[created_by]={}
                ,[is_active]=1
                where candidate_id={};
            '''

            que_test='''
                select sp.is_ojt_req & c.is_ojt_req from batches.tbl_batches as b left join masters.tbl_sub_projects as sp on sp.sub_project_id=b.sub_project_id left join masters.tbl_courses as c on c.course_id=b.course_id where 1=1 and coalesce(sp.is_ojt_req,0)=1  and coalesce(c.is_ojt_req,0)=1 and b.batch_id like trim('{}')
                '''

            #root = ET.fromstring(data)
            query = ""
            fam_query=""
            out=[]
            she_query=""
            for child in root:
                data = child.attrib
                out.append(data['assign_batch'])
                
                curs.execute(que_test.format(data['assign_batch']))
                is_obj = curs.fetchall()
                if is_obj!=[]:
                    quer1 = '''
                    update candidate_details.tbl_candidates set isFresher={},project_type='{}',isDob={},salutation='{}',first_name='{}',middle_name='{}',last_name='{}',date_of_birth='{}',age='{}',primary_contact_no='{}',secondary_contact_no='{}',email_id='{}',gender='{}',marital_status='{}',caste='{}',disability_status='{}',religion='{}',source_of_information='{}',present_district='{}',present_state='{}',present_pincode='{}',present_country='{}',permanent_district='{}',permanent_state='{}',permanent_pincode='{}',permanent_country='{}',candidate_stage_id=3,candidate_status_id=2,created_on=GETDATE(),created_by='{}',created_by_role_id='{}', is_active=1,Cand_Password='Password' where candidate_id='{}';
                    '''
                else:
                    quer1 = '''
                    update candidate_details.tbl_candidates set isFresher={},project_type='{}',isDob={},salutation='{}',first_name='{}',middle_name='{}',last_name='{}',date_of_birth='{}',age='{}',primary_contact_no='{}',secondary_contact_no='{}',email_id='{}',gender='{}',marital_status='{}',caste='{}',disability_status='{}',religion='{}',source_of_information='{}',present_district='{}',present_state='{}',present_pincode='{}',present_country='{}',permanent_district='{}',permanent_state='{}',permanent_pincode='{}',permanent_country='{}',candidate_stage_id=3,candidate_status_id=2,created_on=GETDATE(),created_by='{}',created_by_role_id='{}', is_active=1, Cand_Password=null where candidate_id='{}';
                    '''
                if 'mobilization_type' in data:
                    query += '\n' + quer1.format(1 if data['isFresher']=='true' else 0 ,data['mobilization_type'],1 if data['dobEntered']=='true' else 0,data['candSaltn'],data['firstname'],data['midName'],data['lastName'],data['candDob'],data['candAge'],data['primaryMob'],data['secMob'],data['candEmail'],data['candGender'],data['maritalStatus'],data['candCaste'],data['disableStatus'],data['candReligion'],data['candSource'],data['presDistrict'],data['presState'],data['presPincode'],data['presCountry'],data['permDistrict'],data['permState'],data['permPincode'],data['permCountry'],user_id,role_id,data['cand_id'])
                else:
                    query += '\n' + quer1.format(1 if data['isFresher']=='true' else 0 ,1,1 if data['dobEntered']=='true' else 0,data['candSaltn'],data['firstname'],data['midName'],data['lastName'],data['candDob'],data['candAge'],data['primaryMob'],data['secMob'],data['candEmail'],data['candGender'],data['maritalStatus'],data['candCaste'],data['disableStatus'],data['candReligion'],data['candSource'],data['presDistrict'],data['presState'],data['presPincode'],data['presCountry'],data['permDistrict'],data['permState'],data['permPincode'],data['permCountry'],user_id,role_id,data['cand_id'])

                query += '\n' + quer2.format(data['whatsapp_number'],data['candPic'],data['motherTongue'],data['candOccuptn'],data['annualIncome'],data['interestCourse'],data['candProduct'],data['presAddrOne'],data['permAddrOne'],data['highQuali'],data['candStream'],data['compKnow'],data['techKnow'],data['houseIncome'],data['bankName'],data['accNum'],user_id,data['cand_id'])
                query += '\n' + quer3.format(data['presAddrTwo'],data['presVillage'],data['presPanchayat'],data['presTaluk'],data['permAddrTwo'],data['permVillage'],data['permPanchayat'],data['permTaluk'],data['instiName'],data['university'],data['yrPass'],data['percentage'],data['branchName'],data['ifscCode'],data['accType'],data['bankCopy'],user_id,data['cand_id'])
                query += '\n' + quer7.format(data['cand_id'])
                intervention_category="SAE"
                if data['candProduct']=="Placement":
                    intervention_category="EAL"                
                quer = "({},'{}',GETDATE(),{},1),".format(data['cand_id'],intervention_category,user_id)
                #quer = "({},'SAE',GETDATE(),{},1),".format(data['cand_id'],user_id)
                quer4 += '\n'+quer
                for fam in child.findall('family_details'):
                    dt=fam.attrib
                    fam_query+="({},'{}','{}','{}','{}','{}','{}','{}','{}','{}','{}',{},GETDATE(),1),".format(data['cand_id'],dt['memberSal'],dt['memberName'],dt['memberDob'],dt['memberAge'],dt['memberContact'],dt['memberEmail'],dt['memberGender'],dt['memberRelation'],dt['memberQuali'],dt['memberOccuptn'],user_id)
                if 'mobilization_type' in data:
                    if int(data['mobilization_type'])==2:
                        she_query += '\n' + update_query_she.format(data['aadhar_address'],data['family_members'],data['rented_or_own'],data['size_of_house'],data['ration_card'],data['tv'],data['refrigerator'],data['washing_machine'],data['ac_cooler'],data['car'],data['medical_insurance'],data['life_insurance'],data['others'],data['educational_qualification'],data['age_proof'],data['signed_mou'],data['mou_signed_date'],data['kit_given_date'],data['head_of_household'],data['farm_land'],data['acres_of_land'],int(user_id),int(data['cand_id']))
            curs.execute(query)
            curs.commit()
            if she_query!="":
                curs.execute(she_query)
                curs.commit()
            quer4 = quer4[:-1]+';'
            curs.execute(quer4)
            d = list(map(lambda x:x[0],curs.fetchall()))
            curs.commit()
            for i in range(len(d)):
                quer5 += '\n' + "({},(select course_id from batches.tbl_batches where batch_id={}),{},concat('ENR',(NEXT VALUE FOR candidate_details.sq_candidate_enrollment_no)),GETDATE(),{},1),".format(d[i],out[i],out[i],user_id)
            quer5 = quer5[:-1]+';'
            curs.execute(quer5)
            curs.execute(quer8)
            curs.commit()
            
            if fam_query!="":
                quer6 += fam_query[:-1]+';'
                curs.execute(quer6)
                curs.commit()
            response_data=[]
            intervention_string =','.join(map(str, d))
            response_query = 'SELECT c.candidate_id as Candidate_Id,c.first_name as First_Name,COALESCE(middle_name,\'\') as Middle_Name,COALESCE(last_name,\'\') as Last_Name,c.primary_contact_no as Mobile_Number,cis.intervention_value as Enrollment_Id FROM candidate_details.tbl_candidate_interventions ci LEFT JOIN candidate_details.tbl_candidates as c on c.candidate_id=ci.candidate_id LEFT JOIN candidate_details. tbl_map_candidate_intervention_skilling as cis on cis.intervention_id=ci.candidate_intervention_id where ci.candidate_intervention_id IN ('+intervention_string+');'
            curs.execute(response_query)
            columns = [column[0].title() for column in curs.description]
            for row in curs:
                h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[3]+"":row[3],""+columns[4]+"":row[4],""+columns[5]+"":row[5]}
                response_data.append(h)
            out = {'success': True, 'description': "Submitted Successfully", 'app_status':True,'data':response_data}
            curs.close()
            conn.close()
            return out
        except Exception as e:            
            out = {'success': False, 'description': "error: "+str(e), 'app_status':True}
            return out
          
    def get_batch_list_updated(user_id,candidate_id,role_id,mobilization_type):
        conn = pyodbc.connect(conn_str)
        curs = conn.cursor()
        quer = 'exec  [batches].[sp_get_batch_list_for_app]  ?,?,?,?'
        values=(user_id,candidate_id,role_id,mobilization_type)
        curs.execute(quer,(values))
        columns = [column[0].title() for column in curs.description]
        response = []
        h={}
        for row in curs:
            for i in range(len(columns)):
                h[columns[i]]=row[i]
            response.append(h.copy())
        curs.close()
        conn.close()
        out = {'success': True, 'description': "Success", "batches":response}
        return out

    def GetContractProjectTargets(contact_id,user_id,user_role_id,region_id,from_date,to_date):
        response = []
        h={}
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()
        sql = 'exec  [masters].[sp_get_contract_project_target_values]  ?,?,?,?,?,?'
        values = (contact_id,user_id,user_role_id,region_id,from_date,to_date)
        cur2.execute(sql,(values))
        #   print(cur2.fetchall())
        #print(cur2)
        columns = [column[0].title() for column in cur2.description]
        for row in cur2:
            for i in range(len(columns)):
                h[columns[i]]=row[i]           
            response.append(h.copy())
        cur2.close()
        con.close()
        return response

    def sub_project_list(user_id,user_role_id,user_region_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw,entity,customer,p_group,block,practice,bu,product,status,project):
        response = {}
        d = []
        h={}
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [masters].[sp_get_sub_project_list] ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?'
        values = (user_id,user_role_id,user_region_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,entity,customer,p_group,block,practice,bu,product,status,project)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        record="0"
        fil="0"
        for row in cur:
            record=row[len(columns)-1]
            fil=row[len(columns)-2]
            for i in range(len(columns)-2):
                h[columns[i]]=row[i]
            d.append(h.copy())
        response = {"draw":draw,"recordsTotal":record,"recordsFiltered":fil,"data":d}
        cur.close()
        con.close()
        return response
    def mobilization_web_inser(df,user_id,ProjectType):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        try:

            quer_user  = "(select u.user_id from users.tbl_users as u left join users.tbl_user_details as ud on ud.user_id=u.user_id left join users.tbl_partner_users as up on up.user_id=u.user_id where u.is_active=1 and ((ud.email like trim('{}')) OR (up.email like trim('{}'))))"
            
            quer1 = '''
            insert into candidate_details.tbl_candidates
            (isFresher, salutation, first_name, middle_name, last_name, date_of_birth, isDob, age,primary_contact_no, secondary_contact_no, email_id, gender,marital_status, caste, disability_status, religion, source_of_information, present_pincode,present_district, permanent_district,permanent_pincode,candidate_stage_id, candidate_status_id, created_on, created_by, is_active, insert_from,present_state, present_country,permanent_state,permanent_country,project_type)
            OUTPUT inserted.candidate_id
            values
            '''
            quer2='''
            insert into candidate_details.tbl_candidate_reg_enroll_details
            (candidate_id,candidate_photo,present_address_line1,permanaet_address_line1,created_on,created_by,is_active,whatsapp_number)
            values
            '''
            quer3='''
            insert into candidate_details.tbl_candidate_reg_enroll_non_mandatory_details
            (candidate_id,present_address_line2,present_village,present_panchayat,present_taluk_block,permanent_address_line2,permanent_village,permanent_panchayat,permanent_taluk_block,created_on,created_by,is_active)
            values
            '''
            quer4 = '''
            insert into candidate_details.tbl_candidate_dell_details
            (candidate_id, mobilization_type, [Educational Marksheet], [Aspirational District], [Income Certificate],created_on,created_by,is_active)
            values
            '''

            quer5 = '''
            insert into candidate_details.tbl_candidate_she_details
            (candidate_id,mobilization_type,created_by,created_on,is_active)
            values
            '''

            df['Date of Birth*'] = df['Date of Birth*'].astype(str)
            out = df.values.tolist()
            p=0
            if ProjectType==1:#sell
                p=4
            elif ProjectType==2:#she
                p=2
            else:#regular 3
                p=1

            for row in out:
                quer = "({},'{}','{}','{}','{}','{}',{},'{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}',1,2,GETDATE(),{},1,'w',{},'{}',{},'{}',{}),".format(1 if row[0]=='Fresher' else 0,row[2],row[3],row[4],row[5],row[6],
                1 if row[7]=='' else 0,row[7] if row[7]!='' else 0,row[8],row[10],row[11],row[12],row[13],row[14],row[15],row[16],row[17],row[25],row[23],row[32],row[34],quer_user.format(row[36],row[36]),
                "(select state_id from masters.tbl_states where state_name like trim('{}'))".format(row[24]),'1',"(select state_id from masters.tbl_states where state_name like trim('{}'))".format(row[33]),'1',p)
                quer1 += '\n'+quer
            quer1 = quer1[:-1]+';'
            #print(quer1)
            cur.execute(quer1)
            d = list(map(lambda x:x[0],cur.fetchall()))
            cur.commit()
            
            for i in range(len(d)):
                quer2 += '\n' + "({},'{}','{}','{}',GETDATE(),{},1,'{}'),".format(d[i],out[i][1],out[i][18],out[i][27],quer_user.format(out[i][36],out[i][36]),out[i][9])
                quer3 += '\n' + "({},'{}','{}','{}','{}','{}','{}','{}','{}',GETDATE(),{},1),".format(d[i],out[i][19],out[i][20],out[i][21],out[i][22],out[i][28],out[i][29],out[i][30],out[i][31],quer_user.format(out[i][36],out[i][36]))
                quer4 += '\n' + "({},4,'','','',GETDATE(),{},1),".format(d[i],quer_user.format(out[i][36],out[i][36]))
                quer5 +=  '\n' + "({},3,{},GETDATE(),1),".format(d[i],quer_user.format(out[i][36],out[i][36]))

            quer2 = quer2[:-1]+';'
            quer3 = quer3[:-1]+';'
            quer4 = quer4[:-1]+';'
            quer5 = quer5[:-1]+';'

            if ProjectType==1:
                quer =  quer2 + '\n' + quer3 + '\n' + quer4
            elif ProjectType==2:
                quer =  quer2 + '\n' + quer3 + '\n' + quer5
            else:
                quer =  quer2 + '\n' + quer3
            #print(quer)
            cur.execute(quer)
            cur.commit()
            out = {'Status': True, 'message': "Submitted Successfully"}
        except Exception as e:
            out = {'Status': False, 'message': "error: "+str(e)}
        finally:
            cur.close()
            con.close()
            return out
    
    def AllCreatedByBasedOnUser(UserId,UserRoleId):
        response=[]
        h={}
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec	[masters].[sp_get_createdby_based_on_user] ?, ?'
        values = (UserId,UserRoleId)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            for i in range(len(columns)):
                h[columns[i]]=row[i] 
            #h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1]}
            response.append(h.copy())
        cur.commit()
        cur.close()
        con.close()
        return response

    def download_selected_registration_candidate(candidate_ids):
        
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec	[candidate_details].[sp_get_candidate_download_new_R] ?'
        values = (candidate_ids,)
        cur.execute(sql,(values))

        columns = [column[0].title() for column in cur.description]  
        data = list(map(lambda x:list(x),cur.fetchall()))
        cur.close()
        con.close()
        return {'data':data,'columns':columns}

    def registration_web_inser(df,user_id,ProjectType,df_she=[]):
        try:
            con = pyodbc.connect(conn_str)
            cur = con.cursor()
            #print(df.columns)
            #try:
            df['Date of Birth*'] = df['Date of Birth*'].astype(str)
            out = df.values.tolist()

            quer_user  = "(select u.user_id from users.tbl_users as u left join users.tbl_user_details as ud on ud.user_id=u.user_id left join users.tbl_partner_users as up on up.user_id=u.user_id where u.is_active=1 and ((ud.email like trim('{}')) OR (up.email like trim('{}'))))"
            #  quer_user.format(row[36],row[36])
            quer1 = '''
            update candidate_details.tbl_candidates set isFresher={},isDob={},years_of_experience='{}',salutation='{}',first_name='{}',middle_name='{}',last_name='{}',date_of_birth='{}',age='{}',secondary_contact_no='{}',gender='{}',marital_status='{}',caste='{}',disability_status='{}',religion='{}',source_of_information='{}', present_district='{}', present_state=(select state_id from masters.tbl_states where state_name like trim('{}')),present_pincode='{}',present_country=(select country_id from masters.tbl_countries where country_name like trim('{}')),permanent_district='{}',permanent_state=(select state_id from masters.tbl_states where state_name like trim('{}')),permanent_pincode='{}',permanent_country=(select country_id from masters.tbl_countries where country_name like trim('{}')), candidate_stage_id=2,candidate_status_id=2,created_on=GETDATE(),created_by={},is_active=1 where candidate_id='{}';
            '''
            quer2='''
            update candidate_details.tbl_candidate_reg_enroll_details set candidate_photo='{}',mother_tongue='{}',current_occupation='{}',average_annual_income='{}',interested_course='{}',product='{}',aadhar_no='{}',identifier_type=(select identification_id from masters.tbl_identification_type where UPPER(identification_name)=UPPER('{}')),identity_number='{}',document_copy_image_name='{}',employment_type='{}',preferred_job_role='{}',relevant_years_of_experience='{}',current_last_ctc='{}',preferred_location='{}',willing_to_travel='{}',willing_to_work_in_shifts='{}',bocw_registration_id='{}',expected_ctc='{}',present_address_line1='{}',permanaet_address_line1='{}',created_by={},created_on=GETDATE(),is_active=1 ,whatsapp_number='{}',aadhar_image_name='{}' where candidate_id='{}';
            '''
            quer3='''
            update candidate_details.tbl_candidate_reg_enroll_non_mandatory_details set present_address_line2='{}',present_village='{}',present_panchayat='{}',present_taluk_block='{}',permanent_address_line2='{}',permanent_village='{}',permanent_panchayat='{}',permanent_taluk_block='{}',created_by={},created_on=GETDATE(),is_active=1 where candidate_id='{}';
            '''
            quer4 = '''
            update candidate_details.tbl_candidate_dell_details set	[Educational Marksheet]='{}', [Aspirational District]='{}', [Income Certificate]='{}', created_by={}, created_on=GETDATE(), is_active=1 where	candidate_id='{}' 
            '''
            quer7_res=''
            if (ProjectType==2):
                out_she = df_she.values.tolist()
                quer7 = '''
                update candidate_details.tbl_candidate_she_details set [Date of birth (age between 18 to 40)]='{}',[Are you 8th Pass?]='{}',[Are you able to read and write local language?]='{}',[Do you have a smart phone?]='{}',[Are you willing to buy a smartphone?]='{}',
                [Do you own two wheeler?]='{}',[Do you have any work experience in the past?]='{}',[Will you able to work full time or at least 6 hours a day?]='{}',[Are you willing to serve the community at this time of COVID-19 pandemic as Sanitization & Hygiene Entrepreneurs (SHE)?]='{}',
                [Are you willing to travel from one place to another within panchayat?]='{}',[Are you willing to work and sign the work contract with LN?]='{}',[Are you willing to adopt digital transactions in your business?]='{}',[Do you have a bank account?]='{}',
                [Have you availed any loan in the past?]='{}',[Do you have any active loan?]='{}',[Are you willing to take up a loan to purchase tools and consumables?]='{}',[Are you covered under any health insurance?]='{}',[Are you allergic to any chemicals and dust?]='{}',
                [Are you willing to follow  Environment, Health and Safety Norms in your business?]='{}',[Have you ever been subjected to any legal enquiry for Non ethical work/business?]='{}',result='{}'
                where candidate_id={}
                '''
                for row_she in out_she:
                    quer7_res += '\n' + quer7.format(row_she[4],row_she[5],row_she[6],row_she[7],row_she[8],row_she[9],row_she[10],row_she[11],row_she[12],row_she[13],row_she[14],row_she[15],row_she[16],row_she[17],row_she[18],row_she[19],row_she[20],row_she[21],row_she[22],row_she[23],row_she[24],row_she[0])

            query = ""
            if (ProjectType==1):
                for row in out:
                    query += '\n' + quer1.format(1 if str(row[1]).lower()=='true' else 0, 1 if row[8]=='' else 0,row[47],row[3],row[4],row[5],row[6],row[7],row[8],row[10],row[12],row[13],row[14],row[15],row[16],row[20],row[28],row[29],row[30],row[31],row[37],row[38],row[39],row[40],quer_user.format(row[56],row[56]),row[0])
                    query += '\n' + quer2.format(row[2],row[17],row[18],row[19],row[21],row[22],row[41],row[42],row[43],row[44],row[45],row[46],row[48],row[49],row[50],row[51],row[52],row[53],row[54],row[23],row[32],quer_user.format(row[56],row[56]),row[57],row[55],row[0])
                    query += '\n' + quer3.format(row[24],row[25],row[26],row[27],row[33],row[34],row[35],row[36],quer_user.format(row[56],row[56]),row[0])

                    query += '\n' + quer4.format(row[58],row[59],row[60],quer_user.format(row[56],row[56]),row[0])
            else:
                quer2='''
                update candidate_details.tbl_candidate_reg_enroll_details set mother_tongue='{}',current_occupation='{}',average_annual_income='{}',interested_course='{}',product='{}',aadhar_no='{}',identifier_type=(select identification_id from masters.tbl_identification_type where UPPER(identification_name)=UPPER('{}')),identity_number='{}',document_copy_image_name='{}',employment_type='{}',preferred_job_role='{}',relevant_years_of_experience='{}',current_last_ctc='{}',preferred_location='{}',willing_to_travel='{}',willing_to_work_in_shifts='{}',bocw_registration_id='{}',expected_ctc='{}',present_address_line1='{}',permanaet_address_line1='{}',created_by={},created_on=GETDATE(),is_active=1 ,whatsapp_number='{}',aadhar_image_name='{}' where candidate_id='{}';
                '''
                for row in out:
                    query += '\n' + quer1.format(1 if str(row[1]).lower()=='true' else 0, 1 if row[7]=='' else 0,row[46],row[2],row[3],row[4],row[5],row[6],row[7],row[9],row[11],row[12],row[13],row[14],row[15],row[19],row[27],row[28],row[29],row[30],row[36],row[37],row[38],row[39],quer_user.format(row[55],row[55]),row[0])
                    query += '\n' + quer2.format(row[16],row[17],row[18],row[20],row[21],row[40],row[41],row[42],row[43],row[44],row[45],row[47],row[48],row[49],row[50],row[51],row[52],row[53],row[22],row[31],quer_user.format(row[55],row[55]),row[56],row[54],row[0])
                    query += '\n' + quer3.format(row[23],row[24],row[25],row[26],row[32],row[33],row[34],row[37],quer_user.format(row[55],row[55]),row[0])
                    
                if ProjectType==2:
                    query += quer7_res
               
            #print(query)
            cur.execute(query)
            cur.commit()
            out = {'Status': True, 'message': "Submitted Successfully"}
        except Exception as e:
            out = {'Status': False, 'message': "error: "+str(e)}
        finally:
            cur.close()
            con.close()
            return out
            
    def enrollment_web_inser(df,user_id,ProjectType,df_she=[]):
        try:
            conn = pyodbc.connect(conn_str)
            curs = conn.cursor()
            
            df['Date of Birth*'] = df['Date of Birth*'].astype(str)
            out = df.values.tolist()

            quer_user  = "(select u.user_id from users.tbl_users as u left join users.tbl_user_details as ud on ud.user_id=u.user_id left join users.tbl_partner_users as up on up.user_id=u.user_id where u.is_active=1 and ((ud.email like trim('{}')) OR (up.email like trim('{}'))))"
            #  quer_user.format(row[36],row[36])
            quer1 = '''
            update candidate_details.tbl_candidates set isFresher={},isDob={},years_of_experience='{}',salutation='{}',first_name='{}',middle_name='{}',last_name='{}',date_of_birth='{}',age='{}',secondary_contact_no='{}',gender='{}',marital_status='{}',caste='{}',disability_status='{}',religion='{}',source_of_information='{}', present_district='{}', present_state=(select state_id from masters.tbl_states where state_name like trim('{}')),present_pincode='{}',present_country=(select country_id from masters.tbl_countries where country_name like trim('{}')),permanent_district='{}',permanent_state=(select state_id from masters.tbl_states where state_name like trim('{}')),permanent_pincode='{}',permanent_country=(select country_id from masters.tbl_countries where country_name like trim('{}')), candidate_stage_id=3,candidate_status_id=2,created_on=GETDATE(),created_by={},is_active=1 where candidate_id='{}';
            '''
            quer1_OBJ = '''
            update candidate_details.tbl_candidates set isFresher={},isDob={},years_of_experience='{}',salutation='{}',first_name='{}',middle_name='{}',last_name='{}',date_of_birth='{}',age='{}',secondary_contact_no='{}',gender='{}',marital_status='{}',caste='{}',disability_status='{}',religion='{}',source_of_information='{}', present_district='{}', present_state=(select state_id from masters.tbl_states where state_name like trim('{}')),present_pincode='{}',present_country=(select country_id from masters.tbl_countries where country_name like trim('{}')),permanent_district='{}',permanent_state=(select state_id from masters.tbl_states where state_name like trim('{}')),permanent_pincode='{}',permanent_country=(select country_id from masters.tbl_countries where country_name like trim('{}')), candidate_stage_id=3,candidate_status_id=2,created_on=GETDATE(),created_by={},is_active=1,Cand_Password='Password' where candidate_id='{}';
            '''

            quer2='''
            update candidate_details.tbl_candidate_reg_enroll_details set candidate_photo='{}',mother_tongue='{}',current_occupation='{}',average_annual_income='{}',interested_course='{}',product='{}',present_address_line1='{}',permanaet_address_line1='{}',aadhar_no='{}',identifier_type=(select identification_id from masters.tbl_identification_type where UPPER(identification_name)=UPPER('{}')),identity_number='{}',employment_type='{}',preferred_job_role='{}',relevant_years_of_experience='{}',current_last_ctc='{}',preferred_location='{}',willing_to_travel='{}',willing_to_work_in_shifts='{}',bocw_registration_id='{}',expected_ctc='{}',highest_qualification='{}',stream_specialization='{}',computer_knowledge='{}',technical_knowledge='{}',family_salutation='{}',member_name='{}',gender='{}',education_qualification='{}',relationship='{}',occupation='{}',average_household_income='{}',bank_name='{}',account_number='{}',created_by={},created_on=GETDATE(),is_active=1,whatsapp_number='{}' where candidate_id='{}';
            '''
            quer2_dell='''
            update candidate_details.tbl_candidate_reg_enroll_details set mother_tongue='{}',current_occupation='{}',average_annual_income='{}',interested_course='{}',product='{}',present_address_line1='{}',permanaet_address_line1='{}',aadhar_no='{}',identifier_type=(select identification_id from masters.tbl_identification_type where UPPER(identification_name)=UPPER('{}')),identity_number='{}',employment_type='{}',preferred_job_role='{}',relevant_years_of_experience='{}',current_last_ctc='{}',preferred_location='{}',willing_to_travel='{}',willing_to_work_in_shifts='{}',bocw_registration_id='{}',expected_ctc='{}',highest_qualification='{}',stream_specialization='{}',computer_knowledge='{}',technical_knowledge='{}',family_salutation='{}',member_name='{}',gender='{}',education_qualification='{}',relationship='{}',occupation='{}',average_household_income='{}',bank_name='{}',account_number='{}',created_by={},created_on=GETDATE(),is_active=1,whatsapp_number='{}'where candidate_id='{}';
            '''
            quer3='''
            update candidate_details.tbl_candidate_reg_enroll_non_mandatory_details set present_address_line2='{}',present_village='{}',present_panchayat='{}',present_taluk_block='{}',permanent_address_line2='{}',permanent_village='{}',permanent_panchayat='{}',permanent_taluk_block='{}',name_of_institute='{}',university='{}',year_of_pass='{}',percentage='{}',family_date_of_birth='{}',family_age='{}',family_primary_contact='{}',family_email_address='{}',branch_name='{}',branch_code='{}',account_type='{}',attachment_image_name='{}',created_by={},created_on=GETDATE(),is_active=1 where candidate_id='{}';
            '''
            quer4='''
            insert into candidate_details.tbl_candidate_interventions
            (candidate_id,intervention_category,created_on,created_by,is_active)
            OUTPUT inserted.candidate_intervention_id
            values
            '''
            quer5='''
            insert into candidate_details.tbl_map_candidate_intervention_skilling
            (intervention_id, course_id, batch_id, intervention_value, created_on,created_by,is_active)
            values
            '''
            quer6='''
            update	candidate_details.tbl_map_candidate_intervention_skilling set batch_id=(select batch_id from batches.tbl_batches where batch_code=trim('{}')) where intervention_id='{}'
            '''
            quer8='''
            update candidate_details.tbl_candidate_she_details set [Rented or own house?]='{}',[Size of the house]='{}',[Ration card (APL or BPL)]='{}',TV='{}',Refrigerator='{}',[Washing Machine]='{}',[AC /Cooler]='{}',Car='{}',[Medical Insurance]='{}',[Life Insurance]='{}',
            [Farm land]='{}',Others='{}',[Address as per Aadhar Card (incl pin code)]='{}',[Educational qualification]='{}',[Age proof]='{}',[Signed MoU]='{}',[MoU signed date]='{}'
            where candidate_id={}
            '''
            #to restrict sync to shiksha of ELS data
            quer9='''
            update candidate_details.tbl_map_candidate_intervention_skilling
            set    shiksha_sync_status=1 
            where batch_id in (	select batch_id 
					from batches.vw_batch_info 
					where bu_name='ELS'
				   );
            '''
            query = ""
            b=[]
            temp=""
            
            df.columns = df.columns.str.replace('*','')
            df_batch = df.iloc[:,[0,78]] if ProjectType == 1 else df.iloc[:,[0,79]]

            sql = 'exec	masters.[sp_validate_enrollment] ?'
            values = (df_batch.to_json(orient='records'),)
            curs.execute(sql,(values))

            vali = curs.fetchall()[0][0]
            
            # vali ==0 means correct 
            if vali==1:
                out = {'Status': False, 'message': "Sorry, You can't enroll new candidates to the batch, Note: The Actual Enrolment count has exceeded the Planned Target."}
                return out
            # elif vali==2:
            #     out = {'Status': False, 'message': "date issue"}
            #     return out
            # ('[{"Candidate_id":171766,"batch_id":"B-5332-02_Sep_2020"}]',)

            for row in out:

                que='''
                        SELECT		cs.intervention_id 
                        FROM		candidate_details.tbl_candidate_interventions i
                        LEFT JOIN	candidate_details.tbl_map_candidate_intervention_skilling cs on cs.intervention_id= i.candidate_intervention_id 
                        WHERE		i.candidate_id={}
                        AND			cs.intervention_id is NOT NULL
                    '''.format(row[0])
                
                curs.execute(que)
                intervention_id = curs.fetchall()
                if intervention_id!=[]:
                    
                    query += quer6.format(row[78] if ProjectType == 1 else row[79],intervention_id[0][0])
                else:
                    b.append(row[78] if ProjectType == 1 else row[79])
                    temp += '\n' + "({},'SAE',GETDATE(),{},1),".format(row[0],quer_user.format(row[79] if ProjectType == 1 else row[80],row[79] if ProjectType == 1 else row[80]))

                que='''
                select sp.is_ojt_req & c.is_ojt_req from batches.tbl_batches as b left join masters.tbl_sub_projects as sp on sp.sub_project_id=b.sub_project_id left join masters.tbl_courses as c on c.course_id=b.course_id where 1=1 and coalesce(sp.is_ojt_req,0)=1  and coalesce(c.is_ojt_req,0)=1 and batch_code like trim('{}')
                '''
                curs.execute(que.format(row[78] if ProjectType == 1 else row[79]))
                is_obj = curs.fetchall()
                if is_obj!=[]:
                    quer1 = '''
                    update candidate_details.tbl_candidates set isFresher={},isDob={},years_of_experience='{}',salutation='{}',first_name='{}',middle_name='{}',last_name='{}',date_of_birth='{}',age='{}',secondary_contact_no='{}',gender='{}',marital_status='{}',caste='{}',disability_status='{}',religion='{}',source_of_information='{}', present_district='{}', present_state=(select state_id from masters.tbl_states where state_name like trim('{}')),present_pincode='{}',present_country=(select country_id from masters.tbl_countries where country_name like trim('{}')),permanent_district='{}',permanent_state=(select state_id from masters.tbl_states where state_name like trim('{}')),permanent_pincode='{}',permanent_country=(select country_id from masters.tbl_countries where country_name like trim('{}')), candidate_stage_id=3,candidate_status_id=2,created_on=GETDATE(),created_by={},is_active=1,Cand_Password='Password' where candidate_id='{}';
                    '''
                else:
                    quer1 = '''
                    update candidate_details.tbl_candidates set isFresher={},isDob={},years_of_experience='{}',salutation='{}',first_name='{}',middle_name='{}',last_name='{}',date_of_birth='{}',age='{}',secondary_contact_no='{}',gender='{}',marital_status='{}',caste='{}',disability_status='{}',religion='{}',source_of_information='{}', present_district='{}', present_state=(select state_id from masters.tbl_states where state_name like trim('{}')),present_pincode='{}',present_country=(select country_id from masters.tbl_countries where country_name like trim('{}')),permanent_district='{}',permanent_state=(select state_id from masters.tbl_states where state_name like trim('{}')),permanent_pincode='{}',permanent_country=(select country_id from masters.tbl_countries where country_name like trim('{}')), candidate_stage_id=3,candidate_status_id=2,created_on=GETDATE(),created_by={},is_active=1,Cand_Password=null where candidate_id='{}';
                    '''
                    
                if ProjectType==2:
                    query += '\n' + quer8.format(row[82],row[83],row[84],row[85],row[86],row[87],row[88],row[89],row[90],row[91],row[92],row[93],row[94],row[95],row[96],row[97],row[98],row[0])

                    query += '\n' + quer1.format(1 if str(row[1]).lower()=='Fresher' else 0, 1 if row[8]=='' else 0,row[46],row[3],row[4],row[5],row[6],row[7],row[8],row[10],row[12],row[13],row[14],row[15],row[16],row[20],row[28],row[29],row[30],row[31],row[37],row[38],row[39],row[40],quer_user.format(row[80],row[80]),row[0])
                    query += '\n' + quer2.format(row[2],row[17],row[18],row[19],row[21],row[22],row[23],row[32],row[41],row[42],row[43],row[44],row[45],row[47],row[48],row[49],row[50],row[51],row[52],row[53],row[54],row[55],row[60],row[61],row[62],row[63],row[68],row[69],row[70],row[71],row[72],row[73],row[77],quer_user.format(row[80],row[80]),row[81],row[0])
                    query += '\n' + quer3.format(row[24],row[25],row[26],row[27],row[33],row[34],row[35],row[36],row[56],row[57],row[58],row[59],row[64],row[65],row[66],row[67],row[74],row[75],row[76],row[78],quer_user.format(row[80],row[80]),row[0])
                elif ProjectType==1:
                    query += '\n' + quer1.format(1 if str(row[1]).lower()=='Fresher' else 0, 1 if row[7]=='' else 0,row[45],row[2],row[3],row[4],row[5],row[6],row[7],row[9],row[11],row[12],row[13],row[14],row[15],row[19],row[27],row[28],row[29],row[30],row[36],row[37],row[38],row[39],quer_user.format(row[79],row[79]),row[0])
                    query += '\n' + quer2_dell.format(row[16],row[17],row[18],row[20],row[21],row[22],row[31],row[40],row[41],row[42],row[43],row[44],row[46],row[47],row[48],row[49],row[50],row[51],row[52],row[53],row[54],row[59],row[60],row[61],row[62],row[67],row[68],row[69],row[70],row[71],row[72],row[76],quer_user.format(row[79],row[79]),row[80],row[0])
                    query += '\n' + quer3.format(row[23],row[24],row[25],row[26],row[32],row[33],row[34],row[35],row[55],row[56],row[57],row[58],row[63],row[64],row[65],row[66],row[73],row[74],row[75],row[77],quer_user.format(row[79],row[79]),row[0])
                else:
                    query += '\n' + quer1.format(1 if str(row[1]).lower()=='Fresher' else 0, 1 if row[8]=='' else 0,row[46],row[3],row[4],row[5],row[6],row[7],row[8],row[10],row[12],row[13],row[14],row[15],row[16],row[20],row[28],row[29],row[30],row[31],row[37],row[38],row[39],row[40],quer_user.format(row[80],row[80]),row[0])
                    query += '\n' + quer2.format(row[2],row[17],row[18],row[19],row[21],row[22],row[23],row[32],row[41],row[42],row[43],row[44],row[45],row[47],row[48],row[49],row[50],row[51],row[52],row[53],row[54],row[55],row[60],row[61],row[62],row[63],row[68],row[69],row[70],row[71],row[72],row[73],row[77],quer_user.format(row[80],row[80]),row[81],row[0])
                    query += '\n' + quer3.format(row[24],row[25],row[26],row[27],row[33],row[34],row[35],row[36],row[56],row[57],row[58],row[59],row[64],row[65],row[66],row[67],row[74],row[75],row[76],row[78],quer_user.format(row[80],row[80]),row[0])

            #print(query)
            curs.execute(query)
            curs.commit()

            d=[]
            if temp!="":
                #print(temp)  
                quer4 =quer4 + temp[:-1]+';'                          
                curs.execute(quer4)
                d = list(map(lambda x:x[0],curs.fetchall()))
                curs.commit()
            
            temp2=""
            for i in range(len(d)):
                temp2 += '\n' + "({},(select course_id from batches.tbl_batches where batch_code=trim('{}')),(select batch_id from batches.tbl_batches where batch_code=trim('{}')),concat('ENR',(NEXT VALUE FOR candidate_details.sq_candidate_enrollment_no)),GETDATE(),{},1),".format(d[i],b[i],b[i],user_id)
            if temp2!="":
                quer5 = quer5+ temp2[:-1]+';'
                #print(quer5)
                curs.execute(quer5)
                curs.execute(quer9)
                curs.commit()

            out = {'Status': True, 'message': "Submitted Successfully"}
        except Exception as e:
            out = {'Status': False, 'message': "error: "+str(e)}
        finally:
            curs.close()
            conn.close()
            return out

    def SaveCandidateActivityStatus(json_string,user_id,role_id,latitude,longitude,timestamp,app_version,device_model,imei_num,android_version):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec	[candidate_details].[sp_store_sub_candidate_activity_status]  ?, ?,?,?,?,?,?,?,?,?'
        values = (json_string,user_id,role_id,latitude,longitude,timestamp,app_version,device_model,imei_num,android_version)
        cur.execute(sql,(values))
        for row in cur:
            success=row[0]
            description=row[1]
        cur.commit()
        cur.close()
        con.close()
        return {"success":success,"description":description}


    def download_selected_enrolled_candidate(candidate_ids):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec	[candidate_details].[sp_get_candidate_download_new_E] ?'
        values = (candidate_ids,)
        
        cur.execute(sql,(values))

        columns = [column[0].title() for column in cur.description]  
        data = list(map(lambda x:list(x),cur.fetchall()))
        cur.close()
        con.close()
        return {'data':data,'columns':columns}

    def download_selected_candidate_certification(batch_id,enrollment_ids):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec	[assessments].[sp_get_candidate_download_certification] ?,?'
        values = (batch_id,enrollment_ids)
        cur.execute(sql,(values))

        columns = [column[0].title() for column in cur.description]  
        data = list(map(lambda x:list(x),cur.fetchall()))
        cur.close()
        con.close()
        return {'data':data,'columns':columns}
        
    def get_center_details(center_id):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        h={}
        sql = "[masters].[sp_get_center_details] ?"
        values = (center_id,)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            for i in range(len(columns)):
                h[columns[i]]=row[i]
            #h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[3]+"":row[3],""+columns[4]+"":row[4],""+columns[5]+"":row[5],""+columns[6]+"":row[6],""+columns[7]+"":row[7],""+columns[8]+"":row[8],""+columns[9]+"":row[9],""+columns[10]+"":row[10],""+columns[11]+"":row[11],""+columns[12]+"":row[12],""+columns[13]+"":row[13],""+columns[14]+"":row[14],""+columns[15]+"":row[15]}
        cur.close()
        con.close()
        return h

    def GetPartnerTypes():
        response = []
        h={}
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()
        cur2.execute("exec [masters].[sp_get_partner_types]")
        columns = [column[0].title() for column in cur2.description]
        for row in cur2:
            for i in range(len(columns)):
                h[columns[i]]=row[i]           
            response.append(h.copy())
        cur2.close()
        con.close()
        return response
    def GetAssessmentPartnerTypes():
        response = []
        h={}
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()
        cur2.execute("exec [masters].[sp_get_assessment_partner_types]")
        columns = [column[0].title() for column in cur2.description]
        for row in cur2:
            for i in range(len(columns)):
                h[columns[i]]=row[i]           
            response.append(h.copy())
        cur2.close()
        con.close()
        return response    
    def partner_list(partner_type_ids,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        response = {}
        d = []
        h={}
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [masters].[sp_get_partner_list] ?, ?, ?, ?, ?, ?'
        values = (partner_type_ids,start_index,page_length,search_value,order_by_column_position,order_by_column_direction)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        record="0"
        fil="0"
        for row in cur:
            record=row[len(columns)-1]
            fil=row[len(columns)-2]
            for i in range(len(columns)-2):
                h[columns[i]]=row[i]
            d.append(h.copy())
        response = {"draw":draw,"recordsTotal":record,"recordsFiltered":fil,"data":d}
        cur.close()
        con.close()
        return response
    def add_partner_details(partner_name,user_id,is_active,partner_type_id,assessment_partner_type_id,address,partner_id):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec	[masters].[sp_add_edit_partner] ?, ?, ?, ?,?, ?, ?'
        values = (partner_name,user_id,is_active,partner_type_id,assessment_partner_type_id,address,partner_id)
        cur.execute(sql,(values))
        for row in cur:
            pop=row[1]
        cur.commit()
        cur.close()
        con.close()
        if pop ==1:
            msg={"message":"Updated"}
        else:
            msg={"message":"Created"}
        return msg
    def get_partner_details(partner_id):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        h={}
        sql = "[masters].[sp_get_partner_details] ?"
        values = (partner_id,)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            for i in range(len(columns)):
                h[columns[i]]=row[i]
        cur.close()
        con.close()
        return h
    def GetPartnerUsers(partner_id):
        response = []
        h={}
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()
        sql = 'exec [masters].[sp_get_partner_users]  ?'
        values = (partner_id,)
        cur2.execute(sql,(values))
        columns = [column[0].title() for column in cur2.description]
        for row in cur2:
            for i in range(len(columns)):
                h[columns[i]]=row[i]           
            response.append(h.copy())
        cur2.close()
        con.close()
        return response
        con.close()       
        return response
    def add_edit_partner_user(UserName,user_id,is_active,Email,Mobile,PartnerId,PartnerUserId):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec	[users].[sp_add_edit_partner_user] ?, ?, ?, ?, ?, ?,?'
        values = (UserName,user_id,is_active,Email,Mobile,PartnerId,PartnerUserId)
        print(values)
        #print(values)
        cur.execute(sql,(values))
        for row in cur:
            pop=row[1]
        cur.commit()
        cur.close()
        con.close()
        if pop ==1:
            msg={"message":"Updated"}
        else:
            msg={"message":"Created"}
        return msg
    def GetPartners(PartnerTypeId):
        response = []
        h={}
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()
        sql = 'exec [masters].[sp_get_partners] ?'
        values = (PartnerTypeId,)
        cur2.execute(sql,(values))
        columns = [column[0].title() for column in cur2.description]
        for row in cur2:
            for i in range(len(columns)):
                h[columns[i]]=row[i]           
            response.append(h.copy())
        cur2.close()
        con.close()
        return response 
    def GetAssessmentCandidateResultUploadTemplate(AssessmentId,BatchId):
        try:
            col=[]
            response={}
            con = pyodbc.connect(conn_str)
            cur = con.cursor()
            sql = 'exec [assessments].[sp_get_candidate_result_upload_template_data] ?,?'
            values=(AssessmentId,BatchId)            
            cur.execute(sql,(values))
            col = [column[0].title() for column in cur.description]
            data=cur.fetchall()   
            out = []
            for i in data:
                out.append(list(i))        
            df=pd.DataFrame(out)       
            cur.close()
            con.close()
            response= {"columns":col,"data":df}
            return response
        except Exception as e:
            print(str(e))
        return out
    def upload_assessment_result(df,user_id,assessment_id,batch_id,stage_id):
        try: 
            # print(str(df.to_json(orient='records')))
            con = pyodbc.connect(conn_str)
            cur = con.cursor()            
            json_str=df.to_json(orient='records')
            sql = 'exec	[assessments].[sp_upload_assessment_result]  ?,?, ?, ?,?'
            values = (json_str,user_id,assessment_id,batch_id,stage_id)
            cur.execute(sql,(values))
            for row in cur:
                pop=row[0]

            cur.commit()
            cur.close()
            con.close()
            if pop >0 :
                Status=True
                msg="Uploaded Successfully"
            elif pop==-1:
                msg="Only one batch data allowed at a time"
                Status=False
            elif pop==-2:
                msg="Wrong batch to upoload assesment"
                Status=False
            else:
                msg="Wrong Batch code/Enrollment Id"
                Status=False
            return {"Status":Status,'message':msg}
        except Exception as e:
            # print(str(e))
            return {"Status":False,'message': "error: "+str(e)}
    def upload_assessment_certificate_number(df,user_id,assigned_user_id,batch_code,batch_id,enrollment_ids):
        try: 
            # print(str(df.to_json(orient='records')))
            response = []
            con = pyodbc.connect(conn_str)
            cur = con.cursor()            
            json_str=df.to_json(orient='records')
            sql = 'exec	[assessments].[sp_upload_assessment_certificate_number]  ?,?,?'
            values = (json_str,user_id,assigned_user_id)
            cur.execute(sql,(values))
            for row in cur:
                pop=row[0]

            cur.commit()
            
            if pop >0 :
                assigned_by_email_id=''
                assigned_to_email_id=''
                assigned_to_name=''
                Status=True
                sql = 'select top(1) first_name, email from users.tbl_user_details where user_id='+ str(assigned_user_id) +' and is_active=1'
                cur.execute(sql)
                for row in cur:
                    assigned_to_name=row[0]
                    assigned_to_email_id=row[1]
                sql = 'select top(1) email from users.tbl_user_details where user_id='+ str(user_id) +' and is_active=1'
                cur.execute(sql)
                for row in cur:
                    assigned_by_email_id=row[0]
                #sql = 'exec [candidate_details].[sp_get_candidate_details_for_certification] ?,?'
                #values = (batch_id,enrollment_ids)
                #cur.execute(sql,(values))
                #columns = [column[0].title() for column in cur.description]                   
                #for row in cur:
                    #for i in range(len(columns)):
                        #h[columns[i]]=row[i]
                    #response.append(h.copy())
                #attachment_file=Database.create_assessment_candidate_file(response,columns,batch_code,'certification')
                sent_mail.certification_stage_change_mail(1,assigned_to_email_id,assigned_to_name,assigned_by_email_id,batch_code,'')
                msg="Uploaded Successfully"
           
            else:
                msg="Unable To Upload"
                Status=False
            cur.close()
            con.close()
            return {"Status":Status,'message':msg}
        except Exception as e:
            # print(str(e))
            return {"Status":False,'message': "error: "+str(e)}
    
    def UAP_upload_assessment_result(batch_id,stage_id,batch_attempt_number,result_json):
        try: 
            # print(str(df.to_json(orient='records')))
            con = pyodbc.connect(conn_str)
            cur = con.cursor()            
            sql = 'exec	[assessments].[sp_upload_assessment_result_from_UAP]  ?,?, ?, ?'
            values = (result_json,batch_id,3,batch_attempt_number)
            cur.execute(sql,(values))
            for row in cur:
                pop=row[0]

            cur.commit()
            cur.close()
            con.close()
            if pop >0 :
                Status=True
                msg="Uploaded Successfully"
            elif pop==-1:
                msg="Only one batch data allowed at a time"
                Status=False
            elif pop==-2:
                msg="Wrong batch to upoload assesment"
                Status=False
            else:
                msg="Wrong Batch code/Enrollment Id"
                Status=False
            return {"Status":Status,'message':msg}
        except Exception as e:
            # print(str(e))
            return {"Status":False,'message': "error: "+str(e)}
    
    def GetQpWiseReportData(user_id,user_role_id,customer_ids,contract_ids,from_date,to_date):
        response = []
        h={}
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()
        sql = 'exec [reports].[sp_get_qp_wise_report_data]   ?,?,?,?,?,?'
        values = (user_id,user_role_id,customer_ids,contract_ids,from_date,to_date)
        print(values)
        cur2.execute(sql,(values))
        columns = [column[0].title() for column in cur2.description]
        for row in cur2:
            for i in range(len(columns)):
                h[columns[i]]=row[i]           
            response.append(h.copy())
        cur2.close()
        con.close()
        return response
    def GetQpWiseRegionLevelData(user_id,user_role_id,customer_ids,contract_ids,from_date,to_date,qp_id):
        response = []
        h={}
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()
        sql = 'exec [reports].[sp_get_qp_wise_region_level_report_data]   ?,?,?,?,?,?,?'
        values = (user_id,user_role_id,customer_ids,contract_ids,from_date,to_date,qp_id)
        print(values)
        cur2.execute(sql,(values))
        columns = [column[0].title() for column in cur2.description]
        for row in cur2:
            for i in range(len(columns)):
                h[columns[i]]=row[i]           
            response.append(h.copy())
        cur2.close()
        con.close()
        return response
    def GetQpWiseRegionWiseBatchLevelData(user_id,user_role_id,customer_ids,contract_ids,from_date,to_date,qp_id,region_id):
        response = []
        h={}
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()
        sql = 'exec [reports].[sp_get_qp_wise_region_wise_batch_report_data]    ?,?,?,?,?,?,?,?'
        values = (user_id,user_role_id,customer_ids,contract_ids,from_date,to_date,qp_id,region_id)
        print(values)
        cur2.execute(sql,(values))
        columns = [column[0].title() for column in cur2.description]
        for row in cur2:
            for i in range(len(columns)):
                h[columns[i]]=row[i]           
            response.append(h.copy())
        cur2.close()
        con.close()
        return {"response":response,"columns":columns}

    def GetQpWiseDownloadData(user_id,user_role_id,customer_ids,contract_ids):
        response = []
        h={}
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()
        sql = 'exec [reports].[sp_get_qp_wise_report_data_download]   ?,?,?,?'
        values = (user_id,user_role_id,customer_ids,contract_ids)
        print(values)
        cur2.execute(sql,(values))
        columns = [column[0].title() for column in cur2.description]
        for row in cur2:
            for i in range(len(columns)):
                h[columns[i]]=row[i]           
            response.append(h.copy())
        cur2.close()
        con.close()
        return response
    def GetRegionWiseDownloadData(user_id,user_role_id,customer_ids,contract_ids):
        response = []
        h={}
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()
        sql = 'exec [reports].[sp_get_region_wise_report_data_download]   ?,?,?,?'
        values = (user_id,user_role_id,customer_ids,contract_ids)
        print(values)
        cur2.execute(sql,(values))
        columns = [column[0].title() for column in cur2.description]
        for row in cur2:
            for i in range(len(columns)):
                h[columns[i]]=row[i]           
            response.append(h.copy())
        cur2.close()
        con.close()
        return response        
    def GetALLTrainingPartnerdb():
        try:            
            con = pyodbc.connect(conn_str)
            cur = con.cursor()            
            sql = 'select partner_id, partner_name from masters.tbl_partners where partner_type_id=1 and is_active=1'
            cur.execute(sql)
            columns = [column[0].title() for column in cur.description]
            d=[]
            h={}
            for row in cur:
                for i in range(len(columns)):
                    h[columns[i]]=row[i]
                d.append(h.copy())
            cur.commit()
            cur.close()
            con.close()
            return d
        except Exception as e:
            print(str(e))
            return {"Status":False,'message': "error: "+str(e)}

    def add_ex_triner_details(first_name, last_name, email, mobile, trainer_tyoe, Partner, is_active, created_id):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec	[users].[sp_add_edit_ex_treiner] ?, ?, ?, ?, ?, ?, ?, ?'
        values = (first_name, last_name, email, mobile, trainer_tyoe, Partner, is_active, created_id)
        cur.execute(sql,(values))
        for row in cur:
            pop=row[1]
            UserId=row[0]
        cur.commit()
        cur.close()
        con.close()
        if pop ==1:
            msg={"message":"Updated" , "UserId": UserId}
        else: 
            if pop==0:
                msg={"message":"Created", "UserId": UserId}
            else:
                if pop==2:
                    msg={"message":"User with the email id already exists", "UserId": UserId}
        return msg

    def web_verification(mobile,otp):
        try:
            con = pyodbc.connect(conn_str)
            cur = con.cursor()
            sql = 'exec	[masters].[sp_mobile_web_verification] ?, ?'
            values = (mobile,otp)
            cur.execute(sql,(values))
            for row in cur:
                pop=row[0]
            cur.commit()
            cur.close()
            con.close()
            if pop ==1:
               return {"msg":"Your mobile number is verified."}
            else: 
               return {"msg":"Mobile number verification Failed."}
        except Exception as e:
            return {"msg":"Error"+str(e)}

    def app_mobile_validation(mob_no):
        conn = pyodbc.connect(conn_str)
        curs = conn.cursor()
        quer = "select count(*) as mob_count from candidate_details.tbl_candidates where coalesce(primary_contact_no,'')!='' and primary_contact_no like '{}'".format(mob_no)
        #quer = "{"+ quer + "}"
        curs.execute(quer)
        out = curs.fetchall()[0][0]<=0
        #print(out)
        return out

    def app_email_validation(email, candidate_id=0):
        conn = pyodbc.connect(conn_str)
        curs = conn.cursor()
        quer = "EXEC [candidate_details].[sp_app_email_validation] ?,?"
        #quer = "{"+ quer + "}"
        values=(email, candidate_id)
        curs.execute(quer,values)
        return curs.fetchall()[0][0]<=0


    def all_email_validation(cand_stage):
        if cand_stage =='3':
            quer = """
                    select		distinct
                                coalesce(ud.email,'') as email
                    from		users.tbl_users as u
                    left join	users.tbl_user_details as ud on ud.user_id=u.user_id
                    left join   users.tbl_map_User_UserRole as ur on ur.user_id=u.user_id
                    where		ur.user_role_id in (24,5,38)
                    and         coalesce(ur.is_active,0)=1
                    and         u.is_active=1
                    UNION
                    select		distinct
                                coalesce(ud.email,'') as email
                    from		users.tbl_users as u
                    left join	users.tbl_partner_users as ud on ud.user_id=u.user_id
                    left join   users.tbl_map_User_UserRole as ur on ur.user_id=u.user_id
                    where		ur.user_role_id in (24,5,38)
                    and         coalesce(ur.is_active,0)=1
                    and         u.is_active=1
                    """
        else:
            quer = """
                    select		distinct
                                coalesce(ud.email,'') as email
                    from		users.tbl_users as u
                    left join	users.tbl_user_details as ud on ud.user_id=u.user_id
                    left join   users.tbl_map_User_UserRole as ur on ur.user_id=u.user_id
                    where		ur.user_role_id in (2,24,5,38)
                    and         coalesce(ur.is_active,0)=1
                    and         u.is_active=1
                    UNION
                    select		distinct
                                coalesce(ud.email,'') as email
                    from		users.tbl_users as u
                    left join	users.tbl_partner_users as ud on ud.user_id=u.user_id
                    left join   users.tbl_map_User_UserRole as ur on ur.user_id=u.user_id
                    where		ur.user_role_id in (2,24,5,38)
                    and         coalesce(ur.is_active,0)=1
                    and         u.is_active=1
                    """
        conn = pyodbc.connect(conn_str)
        curs = conn.cursor()
        curs.execute(quer)
        return list(map(lambda x:str.lower(x[0]), curs.fetchall()))
    
    def all_state_validation():
        quer = """ select distinct state_name from masters.tbl_states """
        conn = pyodbc.connect(conn_str)
        curs = conn.cursor()
        curs.execute(quer)
        return list(map(lambda x:str.lower(x[0]), curs.fetchall()))

    def DownloadBatchStatusReport(user_id,user_role_id,customer_ids,contract_ids,contract_status,batch_status,from_date,to_date):
        response = []
        h={}
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()
        sql = 'exec [reports].[sp_get_batch_status_report_data]    ?,?,?,?,?,?,?,?'
        values = (user_id,user_role_id,customer_ids,contract_ids,contract_status,batch_status,from_date,to_date)
        #print(values)
        cur2.execute(sql,(values))
        columns = [column[0].title() for column in cur2.description]
        for row in cur2:
            for i in range(len(columns)):
                h[columns[i]]=row[i]           
            response.append(h.copy())
        cur2.close()
        con.close()
        return response
    def GetBatchStatusReportDataList(user_id,user_role_id,customer_ids,contract_ids,contract_status,batch_status,from_date,to_date,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        response = {}
        d = []
        h={}
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [reports].[sp_get_batch_status_date_list] ?,?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?'
        values = (user_id,user_role_id,customer_ids,contract_ids,contract_status,batch_status,from_date,to_date,start_index,page_length,search_value,order_by_column_position,order_by_column_direction)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        record="0"
        fil="0"
        for row in cur:
            record=row[len(columns)-1]
            fil=row[len(columns)-2]
            for i in range(len(columns)-2):
                h[columns[i]]=row[i]
            d.append(h.copy())
        response = {"draw":draw,"recordsTotal":record,"recordsFiltered":fil,"data":d}
        cur.close()
        con.close()
        return response

    def upload_batch_target_plan(df,user_id,user_role_id):
        try:            
            #print(str(df.to_json(orient='records')))
            con = pyodbc.connect(conn_str)
            cur = con.cursor()
            h=[]           
            d={} 
            json_str=df.to_json(orient='records')
            sql = 'exec	[masters].[sp_validate_upload_batch_target_plan]  ?,?,?'
            values = (json_str,user_id,user_role_id)
            cur.execute(sql,(values))
            columns = [column[0].title() for column in cur.description]
            col_len=len(columns)
            pop=0
            for row in cur:
                pop=row[0]
                for i in range(col_len):
                    d[columns[i]]=row[i]
                h.append(d.copy())
            cur.commit()
            if pop==0 :
                Status=False
                msg="Error"
                return {"Status":Status,'message':msg,'data':h}
            else:
                msg="Uploaded Successfully"
                Status=True
                return {"Status":Status,'message':msg}
            cur.close()
            con.close()
        except Exception as e:
            print(str(e))
            return {"Status":False,'message': "error: "+str(e)}
            
    def upload_user(df,user_id,user_role_id):
        try:   
            con = pyodbc.connect(conn_str)
            cur = con.cursor()
            h=[]           
            d={} 
            json_str=df.to_json(orient='records')
            #print(json_str)
            sql = 'exec	[users].[sp_validate_upload_user]  ?,?,?'
            values = (json_str,user_id,user_role_id)
            cur.execute(sql,(values))
            columns = [column[0].title() for column in cur.description]
            col_len=len(columns)
            pop=0
            for row in cur:
                pop=row[0]
                for i in range(col_len):
                    d[columns[i]]=row[i]
                h.append(d.copy())
            cur.commit()
            if pop==0 :
                Status=False
                msg="Error"
                return {"Status":Status,'message':msg,'data':h}
            else:
                msg="Uploaded Successfully"
                Status=True
                return {"Status":Status,'message':msg}
            cur.close()
            con.close()
        except Exception as e:
            print(str(e))
            return {"Status":False,'message': "error: "+str(e)}
    def GetSubProjectPlannedBatches(sub_project_id,course_id,is_assigned,planned_batch_id):
        response = []
        h={}
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()
        sql = 'exec [masters].[sp_get_sub_project_planned_batches]  ?,?,?,?'
        values = (sub_project_id,course_id,is_assigned,planned_batch_id)
        cur2.execute(sql,(values))
        columns = [column[0].title() for column in cur2.description]
        is_ojt=0
        for row in cur2:
            for i in range(len(columns)-1):
                h[columns[i]]=row[i]           
            response.append(h.copy())
            is_ojt=row[-1]
        cur2.close()
        con.close()
        return {"PlannedBatches":response,"is_ojt":is_ojt}
    def Getcenterroom(center_id):
        response = []
        h={}
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()
        sql = 'exec [masters].[sp_get_center_room]  ?'
        values = (center_id,)
        cur2.execute(sql,(values))
        columns = [column[0].title() for column in cur2.description]
        for row in cur2:
            for i in range(len(columns)):
                h[columns[i]]=row[i] 
            #h["Course_Ids"] = row[i] # .split(',')#list(map(lambda x : int(x), row[i].split(',')))  
            response.append(h.copy())
        cur2.close()
        con.close()
        return response
    def add_edit_center_room(Room_Name, user_id, is_active, Room_Type, Room_Size, Room_Capacity, center_id, room_id, file_name, course_ids):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec	[masters].[sp_add_edit_center_room] ?, ?, ?, ?, ?, ?,?, ?, ?, ?'
        values = (Room_Name, user_id, is_active, Room_Type, Room_Size, Room_Capacity, center_id, room_id, file_name, course_ids)
        cur.execute(sql,(values))
        for row in cur:
            pop=row[1]
        cur.commit()
        cur.close()
        con.close()
        if pop ==1:
            msg={"message":"Updated", "status":True}
        else:
            msg={"message":"Created", "status":True}
        return msg

    def get_enrolled_candidates_for_multiple_intervention(user_id,app_version,cand_name,cand_mobile,cand_email,candidate_id):
        conn = pyodbc.connect(conn_str)
        curs = conn.cursor()
        quer = "SELECT TOP (1) version_code FROM [masters].[tbl_mclg_app_version_history] order by id desc"
        curs.execute(quer)
        data=curs.fetchall()
        data = '' if data==[] else data[0][0]
        if int(app_version) < int(data):
            curs.close()
            conn.close()
            out = {'success': False, 'description': "Lower App Version", 'app_status':False}
            return out
        sql = 'exec [candidate_details].[sp_get_enrolled_candidates_for_mutiple_intervention]  ?, ?,?,?,?'        
        values = (user_id,cand_name,cand_mobile,cand_email,candidate_id)
        curs.execute(sql,(values))
        columns = [column[0].title() for column in curs.description]
        response = []
        h={}
        for row in curs:
            for i in range(len(columns)):
                h[columns[i]]=row[i]
            response.append(h.copy())
        curs.close()
        conn.close()
        out = {'success': True, 'description': "Successful", 'app_status':True, 'candidates':response}
        return out
    def get_candidate_details(user_id,candidate_id):
        conn = pyodbc.connect(conn_str)
        curs = conn.cursor()
        sql = 'exec [candidate_details].[sp_get_candidate_details]  ?, ?'
        filenmae = 'candidate_detail_'+str(candidate_id) +'_'+ str(datetime.now().strftime('%Y%m%d_%H%M%S'))+'.xml'
        
        values = (user_id,candidate_id)
        curs.execute(sql,(values))
        columns = [column[0].title() for column in curs.description]
        response = []
        h={}
        for row in curs:
            for i in range(len(columns)):
                h[columns[i]]=row[i]
            response.append(h.copy())
        df = pd.DataFrame(response)
        df = df.fillna('')
        curs.close()
        conn.close()
        df.to_xml(candidate_xmlPath + filenmae)

        #return {'success': True, 'description': "XML Created", 'app_status':True, 'filename':filenmae}
        aws_location_full = aws_location+'neo_app/xml_files/'+'enrollment/' +filenmae
        candidatexml_fullPath = candidate_xmlPath + filenmae
        api_url=COL_URL + "s3_signature?file_name="+aws_location_full+"&file_type=" + 'text/xml'
        requests.get(api_url)
        r = requests.get(api_url)
        json = r.json()
        
        json_data = json['data']
        data = json_data['fields']
        URL = json_data['url']
        raws=''
        with open(candidatexml_fullPath, 'r') as f:
            raws = requests.post(url = URL, data = data, files = {'file':(filenmae,f,'text/xml')})
        os.remove(candidatexml_fullPath)
        if (raws.status_code==200)or(raws.status_code==204):
            out = {'success': True, 'description': "XML Created", 'app_status':True, 'filename':filenmae}
        else:
            out = {'success': False, 'description': "Unable to upload to s3", 'app_status':True}
        return out

    def GetUserTarget(user_id):
        response = []
        h={}
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()
        sql = 'exec users.[sp_get_user_target]  ?'
        values = (user_id,)
        cur2.execute(sql,(values))
        columns = [column[0].title() for column in cur2.description]
        for row in cur2:
            for i in range(len(columns)):
                h[columns[i]]=row[i] 
            #h["Course_Ids"] = row[i] # .split(',')#list(map(lambda x : int(x), row[i].split(',')))  
            response.append(h.copy())
        cur2.close()
        con.close()
        return response
    
    def add_edit_user_targer(created_by, From_Date, To_Date, product, target, is_active, user_id, user_target_id):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec	[users].[sp_add_edit_user_target] ?, ?, ?, ?, ?, ?, ?,?'
        values = (created_by, From_Date, To_Date, product, int(target), is_active, int(user_id), int(user_target_id))
        cur.execute(sql,(values))
        for row in cur:
            pop=row[1]
        cur.commit()
        cur.close()
        con.close()
        if pop ==2:
            msg={"message":"Duplicate Month Target", "status":False}
        elif pop ==1:
            msg={"message":"Updated", "status":True}
        else:
            msg={"message":"Created", "status":True}
        return msg
    
    @classmethod
    def AllCourse_basedon_rooms_db(cls, user_id,user_role_id,center_id, room_ids):
        response=[]
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [masters].[sp_course_basedon_rooms] ?,?,?,?'
        values = (user_id,user_role_id,center_id, room_ids)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1]}
            response.append(h)
        cur.commit()
        cur.close()
        con.close()       
        return response

    def GetMobilizerReportData(user_id,user_role_id,Role, Date):
        response = []
        h={}
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()
        sql = 'exec [reports].[sp_get_mobilization_report_data] ?, ?, ?, ?'
        values = (user_id,user_role_id,Role, Date)
        #print(values)
        cur2.execute(sql,(values))
        columns = [column[0].title() for column in cur2.description]
        for row in cur2:
            for i in range(len(columns)):
                h[columns[i]]=row[i]           
            response.append(h.copy())
        cur2.close()
        con.close()
        return {"Data":response}
    
    def DownloadOpsProductivityReport(customer_ids,contract_ids,month,role_id,user_id,user_role_id):
        con = pyodbc.connect(conn_str)
        curs = con.cursor()
        sheet1=[]
        sheet1_columns=[]
        sheet2=[]
        sheet2_columns=[]
        sheet3=[]
        sheet3_columns=[]
        sql=''
        sql1=''
        sql2=''
        if int(role_id)==11:
            sql = 'exec [reports].[sp_get_ops_productivity_report_data_coo] ?, ?, ?,?,?'
            sql1 = 'exec [reports].[sp_get_ops_productivity_report_data_coo_sub_project] ?, ?, ?,?,?'
            sql2 = 'exec [reports].[sp_get_ops_productivity_report_data_coo_course] ?, ?, ?,?,?'
        if int(role_id)==14:
            sql = 'exec [reports].[sp_get_ops_productivity_report_data_territory_manager] ?, ?, ?,?,?'
            sql1 = 'exec [reports].[sp_get_ops_productivity_report_data_territory_manager_sub_project] ?, ?, ?,?,?'
            sql2 = 'exec [reports].[sp_get_ops_productivity_report_data_territory_manager_course] ?, ?, ?,?,?'
        if int(role_id)==5:
            sql = 'exec [reports].[sp_get_ops_productivity_report_data_center_manager] ?, ?, ?,?,?'
            sql1 = 'exec [reports].[sp_get_ops_productivity_report_data_center_manager_sub_project] ?, ?, ?,?,?'
            sql2 = 'exec [reports].[sp_get_ops_productivity_report_data_center_manager_course] ?, ?, ?,?,?'
        values = (customer_ids, contract_ids, month,user_id,user_role_id)
        
        curs.execute(sql,(values))
        sheet1_columns = [column[0].title() for column in curs.description]        
        data = curs.fetchall()
        sheet1 = list(map(lambda x:list(x), data))
        

        curs.execute(sql1,(values))
        sheet2_columns = [column[0].title() for column in curs.description]        
        data = curs.fetchall()
        sheet2 = list(map(lambda x:list(x), data))

        curs.execute(sql2,(values))
        sheet3_columns = [column[0].title() for column in curs.description]        
        data = curs.fetchall()
        sheet3 = list(map(lambda x:list(x), data))
        return {'sheet1':sheet1,'sheet2':sheet2,'sheet3':sheet3,'sheet1_columns':sheet1_columns,'sheet2_columns':sheet2_columns,'sheet3_columns':sheet3_columns}
        cur2.close()
        con.close()    
    def DownloadClientReport(user_id, user_role_id, client_id, funding_sources, customer_groups, category_type_ids):
        con = pyodbc.connect(conn_str)
        curs = con.cursor()
        sheet1=[]
        sheet1_columns=[]
        sheet2=[]
        sheet2_columns=[]
       
        sql=''
        sql1=''
        sql = 'exec [reports].[sp_get_customer_download] ?, ?, ?,?,?,?'
        sql1 = 'exec [reports].[sp_get_customer_poc_download] ?, ?, ?,?,?,?'
        
        values = (user_id, user_role_id, client_id, funding_sources, customer_groups, category_type_ids)
        curs.execute(sql,(values))
        sheet1_columns = [column[0].title() for column in curs.description]        
        data = curs.fetchall()
        sheet1 = list(map(lambda x:list(x), data))
        

        curs.execute(sql1,(values))
        sheet2_columns = [column[0].title() for column in curs.description]        
        data = curs.fetchall()
        sheet2 = list(map(lambda x:list(x), data))        
        return {'sheet1':sheet1,'sheet2':sheet2,'sheet1_columns':sheet1_columns,'sheet2_columns':sheet2_columns}
        curs.close()
        con.close()    
    def DownloadContractReport(user_id, user_role_id, contract_id, customer_ids, stage_ids, from_date,to_date,entity_ids,sales_category_ids):
        con = pyodbc.connect(conn_str)
        curs = con.cursor()
        sheet1=[]
        sheet1_columns=[]
      
        sql=''
        sql = 'exec [reports].[sp_get_contract_download] ?, ?, ?,?,?,?,?,?,?'
        values = (user_id, user_role_id, contract_id, customer_ids, stage_ids, from_date,to_date,entity_ids,sales_category_ids)
        curs.execute(sql,(values))
        sheet1_columns = [column[0].title() for column in curs.description]        
        data = curs.fetchall()
        sheet1 = list(map(lambda x:list(x), data))
        return {'sheet1':sheet1,'sheet1_columns':sheet1_columns}
        curs.close()
        con.close()    
    
    def DownloadAssessmentProductivityReport(customer_ids,contract_ids,project_ids,sub_project_ids,regions,month,user_id,user_role_id):
        con = pyodbc.connect(conn_str)
        curs = con.cursor()
        sheet1=[]
        sheet1_columns=[]
        
        sql = 'exec [reports].[sp_get_assessment_productivity_report_data] ?,?,?,?, ?, ?,?,?'
        
        values = (customer_ids, contract_ids,project_ids,sub_project_ids,regions, month,user_id,user_role_id)
        
        curs.execute(sql,(values))
        sheet1_columns = [column[0].title() for column in curs.description]        
        data = curs.fetchall()
        sheet1 = list(map(lambda x:list(x), data))        
        return {'sheet1':sheet1,'sheet1_columns':sheet1_columns}
        cur2.close()
        con.close()    
    
    def DownloadRegionProductivityReport(customer_ids,contract_ids,month,region_ids,user_id,user_role_id):
        con = pyodbc.connect(conn_str)
        curs = con.cursor()
        sheet1=[]
        sheet1_columns=[]
        sheet2=[]
        sheet2_columns=[]
        sheet3=[]
        sheet3_columns=[]
        sql=''
        sql1=''
        sql2=''
        
        sql = 'exec [reports].[sp_get_region_productivity_report_data] ?, ?, ?,?,?,?'
        sql1 = 'exec [reports].[sp_get_region_productivity_report_data_batch] ?, ?, ?,?,?,?'
        sql2 = 'exec [reports].[sp_get_region_productivity_report_data_customer] ?, ?, ?,?,?,?'
        values = (customer_ids, contract_ids, region_ids,month,user_id,user_role_id)
        #print(values)
        curs.execute(sql,(values))
        sheet1_columns = [column[0].title() for column in curs.description]        
        data = curs.fetchall()
        sheet1 = list(map(lambda x:list(x), data))
        #print(data)

        curs.execute(sql1,(values))
        sheet2_columns = [column[0].title() for column in curs.description]        
        data = curs.fetchall()
        sheet2 = list(map(lambda x:list(x), data))

        curs.execute(sql2,(values))
        sheet3_columns = [column[0].title() for column in curs.description]        
        data = curs.fetchall()
        sheet3 = list(map(lambda x:list(x), data))
        return {'sheet1':sheet1,'sheet2':sheet2,'sheet3':sheet3,'sheet1_columns':sheet1_columns,'sheet2_columns':sheet2_columns,'sheet3_columns':sheet3_columns}
        cur2.close()
        con.close()
        con.close()

    def DownloadCustomerTargetReport(customer_ids,contract_ids,month,region_ids,user_id,user_role_id):
        con = pyodbc.connect(conn_str)
        curs = con.cursor()
        sheet1=[]
        sheet1_columns=[]
        sheet2=[]
        sheet2_columns=[]
        sheet3=[]
        sheet3_columns=[]
        sql=''
        sql1=''
        sql2=''
        
        sql = 'exec [reports].[sp_get_monthly_target_report_data] ?, ?, ?,?,?,?'
        sql1 = 'exec [reports].[sp_get_monthly_target_report_data_customerwise] ?, ?, ?,?,?,?'
        sql2 = 'exec [reports].[sp_get_monthly_target_report_data_customerwise_batches] ?, ?, ?,?,?,?'
        values = (customer_ids, contract_ids, region_ids,month,user_id,user_role_id)
        #print(values)
        curs.execute(sql,(values))
        sheet1_columns = [column[0].title() for column in curs.description]        
        data = curs.fetchall()
        sheet1 = list(map(lambda x:list(x), data))
        #print(data)

        curs.execute(sql1,(values))
        sheet2_columns = [column[0].title() for column in curs.description]        
        data = curs.fetchall()
        sheet2 = list(map(lambda x:list(x), data))

        curs.execute(sql2,(values))
        sheet3_columns = [column[0].title() for column in curs.description]        
        data = curs.fetchall()
        sheet3 = list(map(lambda x:list(x), data))

      
        return {'sheet1':sheet1,'sheet2':sheet2,'sheet3':sheet3,'sheet1_columns':sheet1_columns,'sheet2_columns':sheet2_columns,'sheet3_columns':sheet3_columns}
        cur2.close()
        con.close()
        con.close()


    def All_role_user(email_id,password,user_id):
        response = []
        h={}
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()
        sql = 'exec [users].All_role_user ?, ?, ?'
        values = (email_id,password,user_id)
        cur2.execute(sql,(values))
        columns = [column[0].title() for column in cur2.description]
        for row in cur2:
            for i in range(len(columns)):
                h[columns[i]]=row[i]           
            response.append(h.copy())
        cur2.close()
        con.close()
        return {"User":response} if response!=[] else None

    def GetCoursesBasedOnSubProjects(sub_project_ids):
        #print(sub_project_ids)
        response = []
        h={}
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()
        sql = "exec [masters].[sp_get_courses_based_on_sub_projects]  ? "
        values = (sub_project_ids,)
        cur2.execute(sql,(values))
        columns = [column[0].title() for column in cur2.description]
        for row in cur2:
            for i in range(len(columns)):
                h[columns[i]]=row[i]           
            response.append(h.copy())
        cur2.close()
        con.close()
        return response

    def AllTrainersOnSubProjects(sub_project_id):
        trainers = []
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()
        sql = "exec [masters].[sp_get_trainer_based_on_sub_projects] ?"
        values = (str(sub_project_id.replace('\'','')),)
        cur2.execute(sql,(values))
        columns = [column[0].title() for column in cur2.description]
        for r in cur2:
            h = {""+columns[0]+"":r[0],""+columns[1]+"":r[1]}
            trainers.append(h)
        cur2.close()
        con.close()
        return trainers
    
    def SyncShikshaAttendanceData():
        max_attendance_id = 0
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()        
        quer = "Select COALESCE(MAX(attendance_id),0) as max_id from [masters].[tbl_shiksha_attendance];"
        cur2.execute(quer)
        data=cur2.fetchall()
        data = '' if data==[] else data[0][0]
        max_attendance_id=int(data)        
        cur2.close()
        con.close()
        return max_attendance_id
    
    def GetShikshaLastSyncDate():
        last_sync_date = ''
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()        
        quer = "Select COALESCE(cast(MAX(last_sync_date) as date),cast('2019-04-01' as date)) as last_sync_date from [masters].[tbl_shiksha_candidate_data];"
        cur2.execute(quer)
        data=cur2.fetchall()
        data = '' if data==[] else data[0][0]
        last_sync_date = datetime.strptime(str(data),'%Y-%m-%d').strftime('%Y-%m-%d')
        cur2.close()
        con.close()        
        return last_sync_date
    
    def UploadShikshaAttendanceData(attandance_data):
        try: 
            # print(str(df.to_json(orient='records')))
            con = pyodbc.connect(conn_str)
            cur = con.cursor()            
            sql = 'exec	[masters].[sp_sync_shiksha_attandance]  ?'
            values = (attandance_data,)
            cur.execute(sql,(values))
            for row in cur:
                pop=row[0]
            cur.commit()
            cur.close()
            con.close()
            if pop >0 :
                Status=True
                msg="Synced Successfully"
            else:
                msg="Error in Syncing"
                Status=False
            return {"Status":Status,'Message':msg}
        except Exception as e:
            # print(str(e))
            return {"Status":False,'message': "error: "+str(e)}

    def SyncShikshaCandidateData(candidate_data):
        try: 
            # print(str(df.to_json(orient='records')))
            con = pyodbc.connect(conn_str)
            cur = con.cursor()            
            sql = 'exec	[masters].[sp_sync_shiksha_candidate_report]  ?'
            values = (candidate_data,)
            cur.execute(sql,(values))
            for row in cur:
                pop=row[0]
            cur.commit()
            cur.close()
            con.close()
            if pop >0 :
                Status=True
                msg="Synced Successfully"
            else:
                msg="Error in Syncing"
                Status=False
            return {"Status":Status,'Message':msg}
        except Exception as e:
            # print(str(e))
            return {"Status":False,'message': "error: "+str(e)}


    def app_get_release_date_msg():
        res = []
        h={}
        conn = pyodbc.connect(conn_str)
        curs = conn.cursor()
        quer = "EXEC [masters].[sp_get_app_release_date_message]"
        curs.execute(quer)
        columns = [column[0].title() for column in curs.description]
        for r in curs:
            h = {"success":r[0],"description":r[1]}
            res.append(h)
        curs.close()
        conn.close()
        return h
    def DownloadCandidateData(candidate_id, user_id, user_role_id, project_types, customer, project, sub_project, batch, region, center, created_by, Contracts, candidate_stage, from_date, to_date):
        con = pyodbc.connect(conn_str)
        curs = con.cursor()
        sheet1=[]
        sheet1_columns=[]
        sql = 'exec [candidate_details].[sp_get_candidate_data] ?,?,?,?,?,?,?,?,?,?,?,?'
        values = (customer,Contracts,project, sub_project, batch,project_types,created_by,from_date,to_date,candidate_stage ,user_id, user_role_id)
        curs.execute(sql,(values))
        sheet1_columns = [column[0].title() for column in curs.description]  
        data = curs.fetchall()
        sheet1 = list(map(lambda x:list(x), data))

        curs.close()
        con.close()
        return {'sheet1':sheet1,'sheet1_columns':sheet1_columns}
        

    def AllTrainerBasedOnUserRegions(RegionIds, status, UserId,UserRoleId):
        response=[]
        h={}
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec	[masters].[sp_get_trainer_based_on_user_regions] ?, ?, ?, ?'
        values = (RegionIds, status, UserId,UserRoleId)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            for i in range(len(columns)):
                h[columns[i]]=row[i] 
            #h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1]}
            response.append(h.copy())
        cur.commit()
        cur.close()
        con.close()
        return response

    def GetCustomerSpoc(customer_id):
        response = []
        h={}
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()
        sql = 'exec [masters].[sp_get_customer_spoc] ?'  
        values=(customer_id,)
        cur2.execute(sql,(values))
        columns = [column[0].title() for column in cur2.description]
        for row in cur2:
            for i in range(len(columns)):
                h[columns[i]]=row[i]      
            response.append(h.copy())
        cur2.close()
        con.close()
        return response

    def GetPOCForCustomer(customer_id):
        response = []
        h={}
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()

        sql = 'exec [masters].[sp_get_POC_for_Customer]  ?'
        values = (customer_id,)
        cur2.execute(sql,(values))
        columns = [column[0].title() for column in cur2.description]
        for row in cur2:
            for i in range(len(columns)):
                h[columns[i]]=row[i]           
            response.append(h.copy())
        cur2.close()
        con.close()
        return response
        
    def get_qp_for_sector(sector_ids):
        response = []
        h={}
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()
        sql = 'exec [content].[sp_qp_basedon_sectors]  ?'
        values = (sector_ids,)
        cur2.execute(sql,(values))
        columns = [column[0].title() for column in cur2.description]
        for row in cur2:
            for i in range(len(columns)):
                h[columns[i]]=row[i]           
            response.append(h.copy())
        cur2.close()
        con.close()
        return response
    def GetAllParentCourse():
        response = []
        h={}
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()
        sql = 'exec [content].[sp_get_parent_courses]'
        cur2.execute(sql)
        columns = [column[0].title() for column in cur2.description]
        for row in cur2:
            for i in range(len(columns)):
                h[columns[i]]=row[i]           
            response.append(h.copy())
        cur2.close()
        con.close()
        return response

    def get_allcandidate_images(user_id,user_role_id,candidate_id):
        h={}
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()
        values=(user_id,user_role_id,candidate_id)
        sql = 'exec candidate_details.sp_get_allcandidate_images ?,?,?'
        cur2.execute(sql,values)
        columns = [column[0].title() for column in cur2.description]
        for row in cur2:
            for i in range(len(columns)):
                h[columns[i]]=row[i]
        cur2.close()
        con.close()
        return h.copy()

    def get_batchid_from_batch_code(batch_code):
        
        response=''
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = "SELECT   distinct [batch_id] FROM  [batches].[tbl_batches]  WHERE batch_code = '{}'".format(str(batch_code))
        cur.execute(sql)
        for row in cur:
            response=row[0]
        cur.close()
        con.close()  
        return str(response)

    def reupload_candidate_image_web_ui(user_id,user_role_id,filename,c_id,candidate_id):
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()
        quer = ""
        quer1 = "update candidate_details.tbl_candidate_reg_enroll_details set candidate_photo='{}' where candidate_id={}"
        quer2 = "update candidate_details.tbl_candidate_reg_enroll_details set aadhar_image_name='{}' where candidate_id = {}"
        quer3 = "update candidate_details.tbl_candidate_reg_enroll_details set document_copy_image_name = '{}' where candidate_id = {}"
        quer4 = "update candidate_details.tbl_candidate_dell_details set [Educational Marksheet]='{}' where candidate_id={}"
        quer5 = "update candidate_details.tbl_candidate_dell_details set [Income Certificate]='{}' where candidate_id={}"
        quer6 = "update candidate_details.tbl_candidate_reg_enroll_non_mandatory_details set attachment_image_name='{}' where candidate_id={}"
        quer7 = "update candidate_details.tbl_candidate_she_details set [Educational qualification]='{}' where candidate_id={}"
        quer8 = "update candidate_details.tbl_candidate_she_details set [Age proof]='{}' where candidate_id={}"
        quer9 = "update candidate_details.tbl_candidate_she_details set [Signed MoU]='{}' where candidate_id={}"

        query = eval('quer'+str(c_id))
        query = query.format(filename,candidate_id)

        cur2.execute(query)
        cur2.commit()
        cur2.close()
        con.close()
        out = {'Status': True, 'message': "Submitted Successfully"}
        return out

    def GetOJTBatchCurrentStageDetails(batch_id,user_id,user_role_id):
        con = pyodbc.connect(conn_str)
        curs = con.cursor()
        quer = "call [masters].[sp_ojt_get_batch_current_stage_detail]({},{},{})".format(user_id, user_role_id,  batch_id)
        quer = "{"+ quer + "}"
        curs.execute(quer)
        data = curs.fetchall()
        
        StageId=0
        if data!=[]:
            StageId=data[0][0]
        curs.close()
        con.close()
        return StageId

    def LogOBJStageDetails(user_id, batch_id, stage_id, latitude, longitude, timestamp, filename, app_version, device_model, imei_num, android_version):
        con = pyodbc.connect(conn_str)
        curs = con.cursor()
        if Database.AppVersionCheck(curs, app_version):
            quer = "call [masters].[sp_OBJ_log_stage_details]({},{},{},'{}','{}','{}','{}','{}','{}','{}')".format(user_id, batch_id, stage_id, latitude, longitude, timestamp, filename, device_model, imei_num, android_version)
            quer = "{"+ quer + "}"
            curs.execute(quer)
            data = curs.fetchall()
            
            if len(data)==0:
                res = {'success': False, 'description':'Not able to log','app_status':True}
            else:
                res = {'success': True, 'description':'Success','app_status':True}
        else:
            res = {'success': True, 'description':'Failed lower app version','app_status':False}

        curs.commit()
        curs.close()
        con.close()
        return res
    
    def GetsubprojectbyCustomer(user_id, user_role_id, customer_id):
        response = []
        h={}
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()
        sql = 'exec [masters].[sp_get_sub_projects_based_on_customer] ?, ?, ?'
        values = (user_id, user_role_id, customer_id)
        cur2.execute(sql,(values))
        columns = [column[0].title() for column in cur2.description]
        for row in cur2:
            for i in range(len(columns)):
                h[columns[i]]=row[i]           
            response.append(h.copy())
        cur2.close()
        con.close()
        return response

    def download_ojt_report(user_id, user_role_id, customer_ids, sub_project_ids, course_ids, batch_code, date_stage, BatchStartFromDate,BatchStartToDate,BatchEndFromDate,BatchEndToDate,OJTStartFromDate,OJTStartToDate,OJTEndFromDate,OJTEndToDate):
        
        cnxn=pyodbc.connect(conn_str)
        curs = cnxn.cursor()
        sql = 'exec [masters].[sp_OJT_report__stagelog] ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?'
        values = (user_id, user_role_id, customer_ids, sub_project_ids, course_ids, batch_code, date_stage, BatchStartFromDate,BatchStartToDate,BatchEndFromDate,BatchEndToDate,OJTStartFromDate,OJTStartToDate,OJTEndFromDate,OJTEndToDate)
        curs.execute(sql,(values))
        columns = [column[0].title() for column in curs.description]
        data = curs.fetchall()
        data = list(map(lambda x:list(x), data))
        
        curs.close()
        cnxn.close()
        return (data,columns)

    def GetSessionsForCourse(CourseId):
        response=[]
        h={}
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [masters].[sp_get_session_for_course]  ?'
        values = (CourseId,)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            for i in range(len(columns)):
                h[columns[i]]=row[i]
            response.append(h.copy())
        out = {'Sessions':response}
        cur.commit()
        cur.close()
        con.close()       
        return out

    def GetPartnerCenters(partner_id):
        response = []
        h={}
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()
        sql = 'exec [masters].[sp_get_partner_centers]  ?'
        values = (partner_id,)
        cur2.execute(sql,(values))
        columns = [column[0].title() for column in cur2.description]
        for row in cur2:
            for i in range(len(columns)):
                h[columns[i]]=row[i]           
            response.append(h.copy())
        cur2.close()
        con.close()
        return response

    def download_centers_list(center_id, user_id, user_role_id, user_region_id, center_type_ids, bu_ids, status, regions, clusters, courses):
        
        cnxn=pyodbc.connect(conn_str)
        curs = cnxn.cursor()
        sql = 'exec [masters].[sp_get_centers_download] ?, ?, ?, ?, ?, ?, ?, ?, ?'
        values = (center_id, user_id, user_role_id, user_region_id, center_type_ids, bu_ids, status, regions, courses)
        curs.execute(sql,(values))
        columns = [column[0].title() for column in curs.description]
        data = curs.fetchall()
        data = list(map(lambda x:list(x), data))
        
        curs.close()
        cnxn.close()
        return (data,columns)

    def download_emp_target_template(user_id, user_role_id, date):
        cnxn=pyodbc.connect(conn_str)
        curs = cnxn.cursor()
        sql = 'exec [reports].[sp_get_emp_target_download] ?, ?, ?'
        values = (user_id, user_role_id, date)
        curs.execute(sql,(values))
        columns = [column[0].title() for column in curs.description]
        data = curs.fetchall()
        data = list(map(lambda x:list(x), data))
        curs.close()
        cnxn.close()
        return (data,columns)

    def upload_employee_target_plan(df,user_id,user_role_id):
        try:            
            #print(str(df.to_json(orient='records')))
            con = pyodbc.connect(conn_str)
            cur = con.cursor()
            #print(len(df))
            json_str=df.to_json(orient='records')
            sql = 'exec	[masters].[sp_upload_employee_target] ?,?,?'
            values = (json_str,user_id,user_role_id)
            cur.execute(sql,(values))
            
            cur.commit()
            cur.close()
            con.close()
            return {"Status":True,'message': "Uploaded successfully"}
        except Exception as e:
            return {"Status":False,'message': "error: "+str(e)}

    def download_Assessment_report(user_id,user_role_id,customer,project,sub_project,region,centers,Batches,FromDate,ToDate):
        cnxn=pyodbc.connect(conn_str)
        curs = cnxn.cursor()
        sql = 'exec [reports].[sp_get_assesment_report] ?, ?, ?, ?, ?, ?, ?, ?, ?, ?'
        values = (user_id,user_role_id,customer,project,sub_project,region,centers,Batches,FromDate,ToDate)
        curs.execute(sql,(values))
        columns = [column[0].title() for column in curs.description]
        data = curs.fetchall()
        data = list(map(lambda x:list(x), data))
        
        curs.close()
        cnxn.close()
        return (data,columns)

    def download_Certification_Distribution_Report(user_id,user_role_id,customer,project,sub_project,region,centers,Batches,FromDate,ToDate):
        cnxn=pyodbc.connect(conn_str)
        curs = cnxn.cursor()
        sql = 'exec [reports].[sp_get_certification_distribution_report] ?, ?, ?, ?, ?, ?, ?, ?, ?, ?'
        values = (user_id,user_role_id,customer,project,sub_project,region,centers,Batches,FromDate,ToDate)
        curs.execute(sql,(values))
        columns = [column[0].title() for column in curs.description]
        data = curs.fetchall()
        data = list(map(lambda x:list(x), data))
        
        curs.close()
        cnxn.close()
        return (data,columns)
    
    def DownloadCertificate_distributionProductivityReport(month, customer_ids, project_ids, sub_project_ids, regions, user_id, user_role_id):
        cnxn=pyodbc.connect(conn_str)
        curs = cnxn.cursor()

        sheet1=[]
        sheet1_columns=[]

        sql = 'exec [reports].[sp_get_certificate_distribution_productivity_report] ?, ?, ?,?,?, ?, ?'
        values = (month, customer_ids, project_ids, sub_project_ids, regions, user_id, user_role_id)
        
        curs.execute(sql,(values))
        sheet1_columns = [column[0].title() for column in curs.description]        
        data = curs.fetchall()
        sheet1 = list(map(lambda x:list(x), data))        
        curs.close()
        cnxn.close()    
        return {'sheet1':sheet1,'sheet1_columns':sheet1_columns}
        