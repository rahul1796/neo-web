import pypyodbc as pyodbc
#import pyodbc
from .config import *
#from Database import config
import pandas as pd
from datetime import datetime
from flask import request,make_response
import requests
import xml.etree.ElementTree as ET
import requests
import io
import csv


def to_xml(df, filename=None, mode='w'):
    if len(df)>0:
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

    def row_to_xml(row):
        xml = ['  <candidate>']
        for i, col_name in enumerate(row.index):
            xml.append('    <field name="{0}">{1}</field>'.format(col_name, row.iloc[i]))
        df3=df1.loc[(df1['Candidate_Id'] == row['Candidate_Id']) & (df1['Activity_Status_Id']>0)]
        #print(df3.dtypes)
        xml.append('    <statushistory>')
        xml.append('\n'.join(df3.apply(nested_row_to_xml, axis=1)))
        xml.append('    </statushistory>')
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
    def Login(email,passw):
        tr =[]
        h={}
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [users].[sp_user_login] ?, ?'
        values = (email,passw)
        print(values)
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
        print(practiceforuser)
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
            print(course_json)
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
    
    def add_subproject_details(SubProjectName, SubProjectCode, Region, State, Centers, Course, PlannedStartDate, PlannedEndDate, ActualStartDate, ActualEndDate, user_id, subproject_id, project_code, isactive):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec	[masters].[sp_add_edit_subproject] ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?'
        values = (SubProjectName, SubProjectCode, Region, State, Centers, Course, PlannedStartDate, PlannedEndDate, ActualStartDate, ActualEndDate, user_id, subproject_id, project_code, isactive)
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
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = "exec	[masters].[sp_GetsubprojectDetails] ?"
        values = (glob_project_id,)
        print(values)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[3]+"":row[3],""+columns[4]+"":row[4],""+columns[5]+"":row[5],""+columns[6]+"":row[6],""+columns[7]+"":row[7],""+columns[8]+"":row[8],""+columns[9]+"":row[9].split(','),""+columns[10]+"":row[10].split(','),""+columns[11]+"":row[11],""+columns[12]+"":row[12]}
        cur.close()
        con.close()
        return h
    
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

    def add_center_details(center_name,user_id,is_active,center_id,center_type_id,country_id,satet_id,location_name,address,pincode,District,partner_id):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec	[masters].[sp_add_edit_centers] ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?,?'
        values = (center_name,user_id,is_active,center_id,center_type_id,country_id,satet_id,location_name,address,pincode,District,partner_id)
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
        print(cluster)
        return cluster
    def GetCountry():
        countries = []
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()
        cur2.execute("SELECT * FROM [masters].[tbl_countries]")
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
    def add_course_details(course_name,project_id,user_id,is_active,center_ids,qp_id,course_id,items,course_code):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec	[content].[sp_add_edit_course] ?, ?, ?, ?, ?, ?, ?, ?,?'
        values = (course_name,project_id,user_id,is_active,center_ids,qp_id,course_id,items,course_code)
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
    def get_course_details(course_id):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [content].[sp_get_course_detail] ?'
        values = (course_id)
        cur.execute(sql,(values,))
        columns = [column[0].title() for column in cur.description]
        response=[]
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[3]+"":row[3],""+columns[4]+"":row[4],""+columns[5]+"":row[5],""+columns[6]+"":row[6]}
            response.append(h)
        data = {"CourseDetail":response,""+columns[7]+"":row[7],""+columns[8]+"":row[8],""+columns[9]+"":row[9]}
        cur.close()
        con.close()
        return data

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
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        record="0"
        fil="0"
        for row in cur:
            record=row[19]
            fil=row[18]
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[3]+"":row[3],""+columns[4]+"":row[4],""+columns[5]+"":row[5],""+columns[6]+"":row[6],""+columns[7]+"":row[7],""+columns[8]+"":row[8],""+columns[9]+"":row[9],""+columns[10]+"":row[10],""+columns[11]+"":row[11],""+columns[12]+"":row[12],""+columns[13]+"":row[13],""+columns[14]+"":row[14],""+columns[15]+"":row[15],""+columns[16]+"":row[16],""+columns[17]+"":row[17]}
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
        #print(values)
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
        
    def batch_list_updated(batch_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw,user_id,user_role_id, status, customer, project, sub_project, region, center, center_type,course_ids, BU, Planned_actual, StartFromDate, StartToDate, EndFromDate, EndToDate):
        #print(status, customer, project, course, region, center)
        content = {}
        d = []
        h={}
        con = pyodbc.connect(conn_str)
        cur = con.cursor()

        sql = 'exec [batches].[sp_get_batch_list_updatd] ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?, ?, ?, ?, ?, ?'

        values = (batch_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,user_id,user_role_id, status, customer, project, sub_project, region, center, center_type, BU,course_ids, Planned_actual, StartFromDate, StartToDate, EndFromDate, EndToDate) #

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

    def add_batch_details(BatchName, Product, Center, Course, SubProject, Cofunding, Trainer, isactive, PlannedStartDate, PlannedEndDate, ActualStartDate, ActualEndDate, StartTime, EndTime, BatchId, user_id):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec	batches.sp_add_edit_batches ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?'
        values = (BatchName, Product, Center, Course, SubProject, Cofunding, Trainer, isactive, PlannedStartDate, PlannedEndDate, ActualStartDate, ActualEndDate, StartTime, EndTime, BatchId, user_id)
        cur.execute(sql,(values))
        for row in cur:
            pop=row[1]
        cur.commit()
        cur.close()
        con.close()
        if pop ==1:
            msg={"message":"Updated Successfully","batch_flag":1}
        else: 
                if pop==0:
                    msg={"message":"Created Successfully","batch_flag":0}
                else:
                    if pop==2:
                        msg={"message":"Batch with the Batch code already exists","batch_flag":2}
        return msg

    def get_batch_details(batch_id):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'select batch_name, product_id, center_id, course_id, sub_project_id, coalesce(co_funding_project_id,-1) as co_funding_project_id, trainer_id, actual_start_date, actual_end_date, training_start_time, training_end_time, is_active, planned_start_date, planned_end_date from batches.tbl_batches where batch_id =?'
        values = (batch_id,)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[3]+"":row[3],""+columns[4]+"":row[4],""+columns[5]+"":row[5],""+columns[6]+"":row[6],""+columns[7]+"":row[7],""+columns[8]+"":row[8],""+columns[9]+"":row[9],""+columns[10]+"":row[10],""+columns[12]+"":row[12],""+columns[11]+"":row[11],""+columns[13]+"":row[13]}
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
        for r in cur2:
            h = {""+columns[0]+"":r[0],""+columns[1]+"":r[1]}
            trainers.append(h)
        cur2.close()
        con.close()
        return trainers
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
    def add_qp_details(qp_name,qp_code,user_id,is_active,qp_id):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec	masters.sp_add_edit_qp ?, ?, ?, ?, ?'
        values = (qp_id,qp_name,qp_code,user_id,is_active)
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
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[4]+"":row[4],""+columns[5]+"":row[5]}
        cur.close()
        con.close()
        return h

    def candidate_list(candidate_id,customer,project,sub_project,region,center,center_type,status,user_id,user_role_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw, Contracts, candidate_stage, from_date, to_date):
        content = {}
        d = []
        h={}
        
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [candidate_details].[sp_get_candidate_web_list_new] ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?,?,?,?,?,?'
        values = (candidate_id,customer,project,sub_project,region,center,center_type,status,user_id,user_role_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,Contracts, candidate_stage, from_date, to_date)
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
        print(d)
        return content
           
    def mobilized_list(candidate_id,region_ids, state_ids, MinAge, MaxAge, user_id, user_role_id, start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        content = {}
        d = []
        h={}
        
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [candidate_details].[sp_get_candidate_web_list_new_M] ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?'
        values = (candidate_id,region_ids, state_ids, MinAge, MaxAge, user_id, user_role_id, start_index,page_length,search_value,order_by_column_position,order_by_column_direction)
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
    def add_client_details(client_name,client_code,user_id,is_active,client_id,FundingSource, CustomerGroup, IndustryType, CategoryType):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec	[masters].[sp_add_edit_client] ?, ?, ?, ?, ?, ?, ?, ?, ?'
        values = (client_name,client_code,user_id,is_active,client_id,FundingSource, CustomerGroup, IndustryType, CategoryType)
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
        sql = "select contract_name, contract_code, coalesce(customer_id,'') as customer_id, coalesce(entity_id,'') as entity_id, coalesce(sales_category_id,'') as sales_category_id, coalesce(start_date,'') as start_date, coalesce(end_date,'') as end_date, is_active, coalesce(value,'') as value, coalesce(sales_manager_id,'') as sales_manager_id  from masters.tbl_contract where contract_id=?"
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
        sql = 'SELECT * FROM [masters].[tbl_region] where is_active=1;'
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
        sql = 'SELECT * FROM [content].[tbl_session_plans] AS sp LEFT JOIN [content].[tbl_map_session_plan_course] AS map ON map.session_plan_id=sp.session_plan_id where map.course_id=?'
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
        sql = 'SELECT * FROM [content].[tbl_modules] where session_plan_id=?'
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

    def TrainerDeploymentBatches(region_id,center_id,course_ids,trainer_ids,from_date,to_date,batch_stage_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        batch = {}
        d = []
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [batches].[sp_tma_web_batch_detail_list] ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?'
        values = (region_id,center_id,course_ids,trainer_ids,batch_stage_id,from_date,to_date,start_index,page_length,search_value,order_by_column_position,order_by_column_direction)
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
    def ReportAttendanceBatches(region_id,center_id,course_ids,trainer_ids,from_date,to_date,batch_stage_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        batch = {}
        d = []
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [batches].[sp_tma_batch_list_for_attendance_report] ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?'
        values = (region_id,center_id,course_ids,trainer_ids,batch_stage_id,from_date,to_date,start_index,page_length,search_value,order_by_column_position,order_by_column_direction)
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
    def GetBatchAssessments(BatchId):
        response=[]
        h={}
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [assessments].[get_batch_assessments] ?'
        values = (BatchId,)
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
    def ScheduleAssessment(batch_id,user_id,requested_date,scheduled_date,assessment_date,assessment_type_id,assessment_agency_id,assessment_id,partner_id,current_stage_id):
        try:
            response=[]
            h={}
            con = pyodbc.connect(conn_str)
            cur = con.cursor()
            sql = 'exec [assessments].[sp_add_edit_batch_assessment] ?,?,?,?,?,?,?,?,?,?'
            values = (batch_id,user_id,requested_date,scheduled_date,assessment_date,assessment_type_id,assessment_agency_id,assessment_id,partner_id,current_stage_id)
            print(values)
            cur.execute(sql,(values))
            columns = [column[0].title() for column in cur.description]
            for row in cur:
                pop=row[0]
                msg=row[1]
            cur.commit()
            cur.close()
            con.close() 
            if pop>0:
                out={"message":msg,"success":1,"assessment_id":pop}
            else:
                out={"message":"Error scheduling assessment","success":0,"assessment_id":pop}
            return out
        except Exception as e:
            return {"message":"Error changing assessment stage","success":0,"assessment_id":0}
    def GetAssessmentCandidateResults(AssessmentId):
        try:
            col=[]
            response={}
            con = pyodbc.connect(conn_str)
            cur = con.cursor()
            sql = 'exec [assessments].[sp_get_candidate_result] ?'
            values=(AssessmentId,)            
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
            for i in range(len(columns)-4):
                h[columns[i]]=row[i]
            #h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[3]+"":row[3],""+columns[4]+"":row[4],""+columns[5]+"":row[5],""+columns[6]+"":row[6]}
            response.append(h.copy())
        out = {"candidates":response,"batch_name":row[9],"center_name":row[10],"course_name":row[11]}
        cur.close()
        con.close()       
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

    def GetECPReportData(user_id,user_role_id,customer_ids,contract_ids,region_ids,from_date,to_date):
        response = []
        h={}
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()
        sql = 'exec [reports].[sp_get_ecp_report_data ]  ?,?,?,?,?,?,?'
        values = (user_id,user_role_id,customer_ids,contract_ids,region_ids,from_date,to_date)
        print(values)
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
        print(values)
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
                return {'app_status':True, 'success': True, 'description': data[2], 'role_id':data[3],'user_id':data[4],'user_name':data[5],'user_email':data[6]}
            else:
                return {'success': False, 'description': 'stored procedure not return true/false','app_status':True}
        else:
            return {'success': False, 'description': 'stored procedure not return true/false','app_status':False}
    
    def otp_send_db(otp, mobile_no, app_name, flag):
        conn = pyodbc.connect(conn_str)
        curs = conn.cursor()
        quer = "call [masters].[sp_mobile_otp_verification]('{}','{}',{},'{}')".format(mobile_no, otp, flag, app_name)
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

    def get_candidate_list_updated(user_id,cand_stage,app_version):
        conn = pyodbc.connect(conn_str)
        curs = conn.cursor()
        quer = "SELECT TOP (1) id FROM [masters].[tbl_mclg_app_version_history] order by id desc"
        curs.execute(quer)
        data=curs.fetchall()
        data = '' if data==[] else data[0][0]
        if app_version < str(data):
            curs.close()
            conn.close()
            out = {'success': False, 'description': "Lower App Version", 'app_status':False}
            return out
        if cand_stage==1:
            sql = 'exec [candidate_details].[sp_get_candidate_list_stage_M]  ?, ?'
            filenmae = 'candidate_list_'+str(user_id) +'_'+ str(datetime.now().strftime('%Y%m%d_%H%M%S'))+'_M.xml'
        elif cand_stage==2:
            sql = 'exec [candidate_details].[sp_get_candidate_list_stage_R]  ?, ?'
            filenmae = 'candidate_list_'+str(user_id) +'_'+ str(datetime.now().strftime('%Y%m%d_%H%M%S'))+'_R.xml'
        elif cand_stage==3:
            sql = 'exec [candidate_details].[sp_get_candidate_list_stage_E]  ?, ?'
            filenmae = 'candidate_list_'+str(user_id) +'_'+ str(datetime.now().strftime('%Y%m%d_%H%M%S'))+'_E.xml'
        else:
            out = {'success': False, 'description': "incorrect stage", 'app_status':True}
            return out
        
        values = (user_id,cand_stage)
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
        out = {'success': True, 'description': "XML Created", 'app_status':True, 'filename':filenmae}
        return out

    def get_submit_candidate_mobi(user_id, xml, latitude, longitude, timestamp, app_version,device_model,imei_num,android_version):
        conn = pyodbc.connect(conn_str)
        curs = conn.cursor()
        quer = "SELECT TOP (1) id FROM [masters].[tbl_mclg_app_version_history] order by id desc"
        curs.execute(quer)
        data=curs.fetchall()
        data = '' if data==[] else data[0][0]
        if app_version < str(data):
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
            (isFresher, salutation, first_name, middle_name, last_name, date_of_birth, isDob, age,primary_contact_no, secondary_contact_no, email_id, gender,marital_status, caste, disability_status, religion, source_of_information, present_pincode,present_district, permanent_district,permanent_pincode,candidate_stage_id, candidate_status_id, created_on, created_by, is_active, insert_from,permanent_state,permanent_country,present_state, present_country)
            OUTPUT inserted.candidate_id
            values
            '''
            quer2='''
            insert into candidate_details.tbl_candidate_reg_enroll_details
            (candidate_id,mother_tongue,current_occupation,average_annual_income,interested_course,product,candidate_photo,present_address_line1,permanaet_address_line1,created_on,created_by,is_active)
            values
            '''
            quer3='''
            insert into candidate_details.tbl_candidate_reg_enroll_non_mandatory_details
            (candidate_id,present_address_line2,present_village,present_panchayat,present_taluk_block,permanent_address_line2,permanent_village,permanent_panchayat,permanent_taluk_block,created_on,created_by,is_active)
            values
            '''
            url = candidate_xml_weburl + xml
            r = requests.get(url)
            data = r.text
            root = ET.fromstring(data)
            out = []
            for child in root:
                data = child.attrib
                out.append(data)
                #quer1_a + = 
                quer = "({},'{}','{}','{}','{}','{}',{},{},'{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}',1,2,GETDATE(),{},1,'m','{}','{}','{}','{}'),".format(1 if data['isFresher']=='true' else 0,data['candSaltn'],data['firstname'],data['midName'],data['lastName'],
                            data['candDob'],1 if data['dobEntered']=='true' else 0,data['candAge'],data['primaryMob'],data['secMob'],data['candEmail'],data['candGender'],data['maritalStatus'],data['candCaste'], data['disableStatus'], data['candReligion'],
                            data['candSource'], data['presPincode'],data['presDistrict'],data['permDistrict'],data['permPincode'],user_id,data['permState'],data['permCountry'] ,data['presState'],data['presCountry'])
                quer1 += '\n'+quer
            quer1 = quer1[:-1]+';'
            curs.execute(quer1)
            d = list(map(lambda x:x[0],curs.fetchall()))
            curs.commit()

            for i in range(len(d)):
                quer2 += '\n' + "({},'{}','{}','{}','{}','{}','{}','{}','{}',GETDATE(),{},1),".format(d[i],out[i]['motherTongue'],out[i]['candOccuptn'],out[i]['annualIncome'],out[i]['interestCourse'],out[i]['candProduct'],out[i]['candPic'],out[i]['presAddrOne'],out[i]['permAddrOne'],user_id)
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
    def get_submit_candidate_reg(user_id, xml, latitude, longitude, timestamp, app_version,device_model,imei_num,android_version):
        conn = pyodbc.connect(conn_str)
        curs = conn.cursor()
        quer = "SELECT TOP (1) id FROM [masters].[tbl_mclg_app_version_history] order by id desc"
        curs.execute(quer)
        data=curs.fetchall()
        data = '' if data==[] else data[0][0]
        if app_version < str(data):
            curs.close()
            conn.close()
            out = {'success': False, 'description': "Lower App Version", 'app_status':False}
            return out
        
        try:
            quer1 = '''
            update candidate_details.tbl_candidates set isFresher={},isDob={},years_of_experience='{}',salutation='{}',first_name='{}',middle_name='{}',last_name='{}',date_of_birth='{}',age='{}',primary_contact_no='{}',secondary_contact_no='{}',email_id='{}',gender='{}',marital_status='{}',caste='{}',disability_status='{}',religion='{}',source_of_information='{}',candidate_stage_id=2,candidate_status_id=2,created_on=GETDATE(),created_by='{}',is_active=1 where candidate_id='{}';
            '''
            quer2='''
            update candidate_details.tbl_candidate_reg_enroll_details set candidate_photo='{}',mother_tongue='{}',current_occupation='{}',average_annual_income='{}',interested_course='{}',product='{}',aadhar_no='{}',identifier_type={},identity_number='{}',document_copy_image_name='{}',employment_type='{}',preferred_job_role='{}',relevant_years_of_experience='{}',current_last_ctc='{}',preferred_location='{}',willing_to_travel='{}',willing_to_work_in_shifts='{}',bocw_registration_id='{}',expected_ctc='{}',created_by='{}',aadhar_image_name='{}',created_on=GETDATE(),is_active=1 where candidate_id='{}';
            '''

            url = candidate_xml_weburl + xml
            r = requests.get(url)
            data = r.text
            root = ET.fromstring(data)
            query = ""
            for child in root:
                data = child.attrib
                aadhar_image_name=''
                if 'aadhar_image_name' in data:
                    aadhar_image_name=data['aadhar_image_name']
                query += '\n' + quer1.format(1 if data['isFresher']=='true' else 0 ,1 if data['dobEntered']=='true' else 0,data['yrsExp'],data['candSaltn'],data['firstname'],data['midName'],data['lastName'],data['candDob'],data['candAge'],data['primaryMob'],data['secMob'],data['candEmail'],data['candGender'],data['maritalStatus'],data['candCaste'],data['disableStatus'],data['candReligion'],data['candSource'],user_id,data['cand_id'])
                query += '\n' + quer2.format(data['candPic'],data['motherTongue'],data['candOccuptn'],data['annualIncome'],data['interestCourse'],data['candProduct'],data['aadhaarNo'],data['idType'],data['idNum'],data['idCopy'],data['empType'],data['prefJob'],data['relExp'],data['lastCtc'],data['prefLocation'],data['willTravel'],data['workShift'],data['bocwId'],data['expectCtc'],user_id,aadhar_image_name,data['cand_id'])
            
            curs.execute(query)
            curs.commit()

            out = {'success': True, 'description': "Submitted Successfully", 'app_status':True}
        except Exception as e:
            out = {'success': False, 'description': "error: "+str(e), 'app_status':True}
        finally:
            curs.close()
            conn.close()
            return out
            
    def get_submit_candidate_enr(user_id, xml, latitude, longitude, timestamp, app_version,device_model,imei_num,android_version):
        conn = pyodbc.connect(conn_str)
        curs = conn.cursor()
        quer = "SELECT TOP (1) id FROM [masters].[tbl_mclg_app_version_history] order by id desc"
        curs.execute(quer)
        data=curs.fetchall()
        data = '' if data==[] else data[0][0]
        if app_version < str(data):
            curs.close()
            conn.close()
            out = {'success': False, 'description': "Lower App Version", 'app_status':False}
            return out
        
        try:
            quer1 = '''
            update candidate_details.tbl_candidates set isFresher={},isDob={},salutation='{}',first_name='{}',middle_name='{}',last_name='{}',date_of_birth='{}',age='{}',primary_contact_no='{}',secondary_contact_no='{}',email_id='{}',gender='{}',marital_status='{}',caste='{}',disability_status='{}',religion='{}',source_of_information='{}',present_district='{}',present_state='{}',present_pincode='{}',present_country='{}',permanent_district='{}',permanent_state='{}',permanent_pincode='{}',permanent_country='{}',candidate_stage_id=3,candidate_status_id=2,created_on=GETDATE(),created_by='{}',is_active=1 where candidate_id='{}';
            '''
            quer2='''
            update candidate_details.tbl_candidate_reg_enroll_details set candidate_photo='{}',mother_tongue='{}',current_occupation='{}',average_annual_income='{}',interested_course='{}',product='{}',present_address_line1='{}',permanaet_address_line1='{}',highest_qualification='{}',stream_specialization='{}',computer_knowledge='{}',technical_knowledge='{}',average_household_income='{}',bank_name='{}',account_number='{}',created_by='{}',created_on=GETDATE(),is_active=1 where candidate_id='{}';
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
            url = candidate_xml_weburl + xml
            r = requests.get(url)
            data = r.text
            root = ET.fromstring(data)
            query = ""
            fam_query=""
            out=[]
            for child in root:
                data = child.attrib
                out.append(data['assign_batch'])
                query += '\n' + quer1.format(1 if data['isFresher']=='true' else 0 ,1 if data['dobEntered']=='true' else 0,data['candSaltn'],data['firstname'],data['midName'],data['lastName'],data['candDob'],data['candAge'],data['primaryMob'],data['secMob'],data['candEmail'],data['candGender'],data['maritalStatus'],data['candCaste'],data['disableStatus'],data['candReligion'],data['candSource'],data['presDistrict'],data['presState'],data['presPincode'],data['presCountry'],data['permDistrict'],data['permState'],data['permPincode'],data['permCountry'],user_id,data['cand_id'])
                query += '\n' + quer2.format(data['candPic'],data['motherTongue'],data['candOccuptn'],data['annualIncome'],data['interestCourse'],data['candProduct'],data['presAddrOne'],data['permAddrOne'],data['highQuali'],data['candStream'],data['compKnow'],data['techKnow'],data['houseIncome'],data['bankName'],data['accNum'],user_id,data['cand_id'])
                query += '\n' + quer3.format(data['presAddrTwo'],data['presVillage'],data['presPanchayat'],data['presTaluk'],data['permAddrTwo'],data['permVillage'],data['permPanchayat'],data['permTaluk'],data['instiName'],data['university'],data['yrPass'],data['percentage'],data['branchName'],data['ifscCode'],data['accType'],data['bankCopy'],user_id,data['cand_id'])

                quer = "({},'SAE',GETDATE(),{},1),".format(data['cand_id'],user_id)
                quer4 += '\n'+quer
                
                for fam in child.findall('family_details'):
                    dt=fam.attrib
                    fam_query+="({},'{}','{}','{}','{}','{}','{}','{}','{}','{}','{}',{},GETDATE(),1),".format(data['cand_id'],dt['memberSal'],dt['memberName'],dt['memberDob'],dt['memberAge'],dt['memberContact'],dt['memberEmail'],dt['memberGender'],dt['memberRelation'],dt['memberQuali'],dt['memberOccuptn'],user_id)
            curs.execute(query)
            curs.commit()

            quer4 = quer4[:-1]+';'
            curs.execute(quer4)
            d = list(map(lambda x:x[0],curs.fetchall()))
            curs.commit()
            for i in range(len(d)):
                quer5 += '\n' + "({},(select course_id from batches.tbl_batches where batch_id={}),{},concat('ENR',(NEXT VALUE FOR candidate_details.sq_candidate_enrollment_no)),GETDATE(),{},1),".format(d[i],out[i],out[i],user_id)
            quer5 = quer5[:-1]+';'
            curs.execute(quer5)
            curs.commit()
            
            if fam_query!="":
                quer6 += fam_query[:-1]+';'
                curs.execute(quer6)
                curs.commit()

            out = {'success': True, 'description': "Submitted Successfully", 'app_status':True}
        except Exception as e:
            out = {'success': False, 'description': "error: "+str(e), 'app_status':True}
        finally:
            curs.close()
            conn.close()
            return out
          
    def get_batch_list_updated(user_id):
        conn = pyodbc.connect(conn_str)
        curs = conn.cursor()
        quer = """
        SELECT	distinct b.batch_id, b.batch_name, batch_code FROM [masters].[tbl_map_sub_project_user] as mspb inner join	batches.tbl_batches as b on b.sub_project_id=mspb.sub_project_id where mspb.user_id={} and CONVERT(DATE, GETDATE(), 102) <= b.actual_end_date
        UNION
        SELECT	distinct b.batch_id, b.batch_name, batch_code FROM [masters].[tbl_map_sub_project_user] as mspb inner join	batches.tbl_batches as b on b.co_funding_project_id=mspb.sub_project_id where mspb.user_id={} and CONVERT(DATE, GETDATE(), 102) <= b.actual_end_date
        """.format(user_id,user_id)
        
        curs.execute(quer)
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
    def mobilization_web_inser(df,user_id):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        try:
            quer1 = '''
            insert into candidate_details.tbl_candidates
            (isFresher, salutation, first_name, middle_name, last_name, date_of_birth, isDob, age,primary_contact_no, secondary_contact_no, email_id, gender,marital_status, caste, disability_status, religion, source_of_information, present_pincode,present_district, permanent_district,permanent_pincode,candidate_stage_id, candidate_status_id, created_on, created_by, is_active, insert_from,permanent_state,permanent_country,present_state, present_country)
            OUTPUT inserted.candidate_id
            values
            '''
            quer2='''
            insert into candidate_details.tbl_candidate_reg_enroll_details
            (candidate_id,candidate_photo,present_address_line1,permanaet_address_line1,created_on,created_by,is_active)
            values
            '''
            quer3='''
            insert into candidate_details.tbl_candidate_reg_enroll_non_mandatory_details
            (candidate_id,present_address_line2,present_village,present_panchayat,present_taluk_block,permanent_address_line2,permanent_village,permanent_panchayat,permanent_taluk_block,created_on,created_by,is_active)
            values
            '''
            df['Date of Birth*'] = df['Date of Birth*'].astype(str)
            out = df.values.tolist()
            for row in out:
                quer = "({},'{}','{}','{}','{}','{}',{},'{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}',1,2,GETDATE(),{},1,'w',{},'{}',{},'{}'),".format(1 if row[0]=='Fresher' else 0,row[2],row[3],row[4],row[5],row[6],
                        1 if row[7]=='' else 0,row[7] if row[7]!='' else 0,row[8],row[9],row[10],row[11],row[12],row[13],row[14],row[15],row[16],row[24],row[22],row[31],row[33],user_id,"(select state_id from masters.tbl_states where state_name like trim('{}'))".format(row[23]),
                        '1',"(select state_id from masters.tbl_states where state_name like trim('{}'))".format(row[32]),'1')
                quer1 += '\n'+quer
            quer1 = quer1[:-1]+';'
            cur.execute(quer1)
            d = list(map(lambda x:x[0],cur.fetchall()))
            cur.commit()
            for i in range(len(d)):
                quer2 += '\n' + "({},'{}','{}','{}',GETDATE(),{},1),".format(d[i],out[i][1],out[i][17],out[i][26],user_id)
                quer3 += '\n' + "({},'{}','{}','{}','{}','{}','{}','{}','{}',GETDATE(),{},1),".format(d[i],out[i][18],out[i][19],out[i][20],out[i][21],out[i][27],out[i][28],out[i][29],out[i][30],user_id)
            quer2 = quer2[:-1]+';'
            quer3 = quer3[:-1]+';'
            cur.execute(quer2 + '\n' + quer3)
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

    def download_selected_registration_candidate(candidate_ids,filename):
        response=[]
        h={}
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec	[candidate_details].[sp_get_candidate_download_new_R] ?'
        values = (candidate_ids,)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        data = list(map(lambda x:list(x),cur.fetchall()))

        cur.close()
        con.close()
        return data

    def registration_web_inser(df,user_id):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        try:
            df['Date of Birth*'] = df['Date of Birth*'].astype(str)
            out = df.values.tolist()
                                                                                                                                                                                                                                                                                                                                                                                                    
            quer1 = '''
            update candidate_details.tbl_candidates set isFresher={},isDob={},years_of_experience='{}',salutation='{}',first_name='{}',middle_name='{}',last_name='{}',date_of_birth='{}',age='{}',primary_contact_no='{}',secondary_contact_no='{}',email_id='{}',gender='{}',marital_status='{}',caste='{}',disability_status='{}',religion='{}',source_of_information='{}', present_district='{}', present_state=(select state_id from masters.tbl_states where state_name like trim('{}')),present_pincode='{}',present_country=(select country_id from masters.tbl_countries where country_name like trim('{}')),permanent_district='{}',permanent_state=(select state_id from masters.tbl_states where state_name like trim('{}')),permanent_pincode='{}',permanent_country=(select country_id from masters.tbl_countries where country_name like trim('{}')), candidate_stage_id=2,candidate_status_id=2,created_on=GETDATE(),created_by='{}',is_active=1 where candidate_id='{}';
            '''
            quer2='''
            update candidate_details.tbl_candidate_reg_enroll_details set candidate_photo='{}',mother_tongue='{}',current_occupation='{}',average_annual_income='{}',interested_course='{}',product='{}',aadhar_no='{}',identifier_type=(select identification_id from masters.tbl_identification_type where UPPER(identification_name)=UPPER('{}')),identity_number='{}',document_copy_image_name='{}',employment_type='{}',preferred_job_role='{}',relevant_years_of_experience='{}',current_last_ctc='{}',preferred_location='{}',willing_to_travel='{}',willing_to_work_in_shifts='{}',bocw_registration_id='{}',expected_ctc='{}',present_address_line1='{}',permanaet_address_line1='{}',created_by='{}',created_on=GETDATE(),is_active=1 where candidate_id='{}';
            '''
            quer3='''
            update candidate_details.tbl_candidate_reg_enroll_non_mandatory_details set present_address_line2='{}',present_village='{}',present_panchayat='{}',present_taluk_block='{}',permanent_address_line2='{}',permanent_village='{}',permanent_panchayat='{}',permanent_taluk_block='{}',created_by='{}',created_on=GETDATE(),is_active=1 where candidate_id='{}';
            '''
            query = ""
            for row in out:
                #row[42]=1
                query += '\n' + quer1.format(1 if str(row[1]).lower()=='true' else 0, 1 if row[8]=='' else 0,row[47],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],row[14],row[15],row[16],row[20],row[28],row[29],row[30],row[31],row[37],row[38],row[39],row[40],user_id,row[0])
                query += '\n' + quer2.format(row[2],row[17],row[18],row[19],row[21],row[22],row[41],row[42],row[43],row[44],row[45],row[46],row[48],row[49],row[50],row[51],row[52],row[53],row[54],row[23],row[32],user_id,row[0])
                query += '\n' + quer3.format(row[24],row[25],row[26],row[27],row[33],row[34],row[35],row[36],user_id,row[0])
            
            cur.execute(query)
            cur.commit()
            out = {'Status': True, 'message': "Submitted Successfully"}
        except Exception as e:
            print(e)
            out = {'Status': False, 'message': "error: "+str(e)}
        finally:
            cur.close()
            con.close()
            return out
    
    def enrollment_web_inser(df,user_id):
        try:
            conn = pyodbc.connect(conn_str)
            curs = conn.cursor()

            df['Date of Birth*'] = df['Date of Birth*'].astype(str)
            out = df.values.tolist()
            quer1 = '''
            update candidate_details.tbl_candidates set isFresher={},isDob={},years_of_experience='{}',salutation='{}',first_name='{}',middle_name='{}',last_name='{}',date_of_birth='{}',age='{}',primary_contact_no='{}',secondary_contact_no='{}',email_id='{}',gender='{}',marital_status='{}',caste='{}',disability_status='{}',religion='{}',source_of_information='{}', present_district='{}', present_state=(select state_id from masters.tbl_states where state_name like trim('{}')),present_pincode='{}',present_country=(select country_id from masters.tbl_countries where country_name like trim('{}')),permanent_district='{}',permanent_state=(select state_id from masters.tbl_states where state_name like trim('{}')),permanent_pincode='{}',permanent_country=(select country_id from masters.tbl_countries where country_name like trim('{}')), candidate_stage_id=3,candidate_status_id=2,created_on=GETDATE(),created_by='{}',is_active=1 where candidate_id='{}';
            '''
            quer2='''
            update candidate_details.tbl_candidate_reg_enroll_details set candidate_photo='{}',mother_tongue='{}',current_occupation='{}',average_annual_income='{}',interested_course='{}',product='{}',present_address_line1='{}',permanaet_address_line1='{}',aadhar_no='{}',identifier_type=(select identification_id from masters.tbl_identification_type where UPPER(identification_name)=UPPER('{}')),identity_number='{}',document_copy_image_name='{}',employment_type='{}',preferred_job_role='{}',relevant_years_of_experience='{}',current_last_ctc='{}',preferred_location='{}',willing_to_travel='{}',willing_to_work_in_shifts='{}',bocw_registration_id='{}',expected_ctc='{}',highest_qualification='{}',stream_specialization='{}',computer_knowledge='{}',technical_knowledge='{}',family_salutation='{}',member_name='{}',gender='{}',education_qualification='{}',relationship='{}',occupation='{}',average_household_income='{}',bank_name='{}',account_number='{}',created_by='{}',created_on=GETDATE(),is_active=1 where candidate_id='{}';
            '''
            quer3='''
            update candidate_details.tbl_candidate_reg_enroll_non_mandatory_details set present_address_line2='{}',present_village='{}',present_panchayat='{}',present_taluk_block='{}',permanent_address_line2='{}',permanent_village='{}',permanent_panchayat='{}',permanent_taluk_block='{}',name_of_institute='{}',university='{}',year_of_pass='{}',percentage='{}',family_date_of_birth='{}',family_age='{}',family_primary_contact='{}',family_email_address='{}',branch_name='{}',branch_code='{}',account_type='{}',attachment_image_name='{}',created_by='{}',created_on=GETDATE(),is_active=1 where candidate_id='{}';
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
            query = ""
            b=[]
            temp=""
            for row in out:
                #que = '''select candidate_intervention_id from candidate_details.tbl_candidate_interventions where candidate_id='{}' '''.format(row[0])
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
                    query += quer6.format(row[80],intervention_id[0][0])
                else:
                    b.append(row[80])
                    temp += '\n' + "({},'SAE',GETDATE(),{},1),".format(row[0],user_id)
                
                query += '\n' + quer1.format(1 if str(row[1]).lower()=='Fresher' else 0, 1 if row[8]=='' else 0,row[47],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],row[14],row[15],row[16],row[20],row[28],row[29],row[30],row[31],row[37],row[38],row[39],row[40],user_id,row[0])
                query += '\n' + quer2.format(row[2],row[17],row[18],row[19],row[21],row[22],row[23],row[32],row[41],row[42],row[43],row[44],row[45],row[46],row[48],row[49],row[50],row[51],row[52],row[53],row[54],row[55],row[56],row[61],row[62],row[63],row[64],row[69],row[70],row[71],row[72],row[73],row[74],row[78],user_id,row[0])
                query += '\n' + quer3.format(row[24],row[25],row[26],row[27],row[33],row[34],row[35],row[36],row[57],row[58],row[59],row[60],row[65],row[66],row[67],row[68],row[75],row[76],row[77],row[79],user_id,row[0])
            
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
                curs.commit()

            out = {'Status': True, 'message': "Submitted Successfully"}
        except Exception as e:
            out = {'Status': False, 'message': "error: "+str(e)}
        finally:
            curs.close()
            conn.close()
            return out

    def SaveCandidateActivityStatus(json_string,user_id,latitude,longitude,timestamp,app_version,device_model,imei_num,android_version):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec	[candidate_details].[sp_store_sub_candidate_activity_status]  ?, ?,?,?,?,?,?,?,?'
        values = (json_string,user_id,latitude,longitude,timestamp,app_version,device_model,imei_num,android_version)
        cur.execute(sql,(values))
        for row in cur:
            success=row[0]
            description=row[1]
        cur.commit()
        cur.close()
        con.close()
        return {"success":success,"description":description}


    def download_selected_enrolled_candidate(candidate_ids,filename):
        response=[]
        h={}
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec	[candidate_details].[sp_get_candidate_download_new_E] ?'
        values = (candidate_ids,)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        data = list(map(lambda x:list(x),cur.fetchall()))
        cur.close()
        con.close()
        return data

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
    def partner_list(partner_type_ids,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        response = {}
        d = []
        h={}
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [masters].[sp_get_partner_list] ?, ?, ?, ?, ?, ?'
        values = (partner_type_ids,start_index,page_length,search_value,order_by_column_position,order_by_column_direction)
        print(values)
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
    def add_partner_details(partner_name,user_id,is_active,partner_type_id,address,partner_id):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec	[masters].[sp_add_edit_partner] ?, ?, ?, ?, ?, ?'
        values = (partner_name,user_id,is_active,partner_type_id,address,partner_id)
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
    def GetPartners():
        response=[]
        h={}
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [masters].[sp_get_partners]'
        #values = (BatchId,)
        cur.execute(sql)
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            for i in range(len(columns)):
                h[columns[i]]=row[i]
            response.append(h.copy())
        out = response
        cur.commit()
        cur.close()
        con.close()       
        return out
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
            print(str(df.to_json(orient='records')))
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
            else:
                msg="Error"
                Status=False
            return {"Status":Status,'message':msg}
        except Exception as e:
            print(str(e))
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

