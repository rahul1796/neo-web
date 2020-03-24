import pypyodbc as pyodbc
#import pyodbc
from .config import *
import pandas as pd

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
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [masters].[sp_get_project_list] ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?'
        values = (user_id,user_role_id,user_region_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,entity,customer,p_group,block,practice,bu,product,status)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        record="0"
        fil="0"
        for row in cur:
            record=row[16]
            fil=row[15]
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[3]+"":row[3],""+columns[4]+"":row[4],""+columns[5]+"":row[5],""+columns[6]+"":row[6],""+columns[7]+"":row[7],""+columns[8]+"":row[8],""+columns[9]+"":row[9],""+columns[10]+"":row[10],""+columns[11]+"":row[11],""+columns[12]+"":row[12],""+columns[13]+"":row[13],""+columns[14]+"":row[14]}
            d.append(h)
        content = {"draw":draw,"recordsTotal":record,"recordsFiltered":fil,"data":d}
        cur.close()
        con.close()
        return content
    def GetALLClient():
        client = []
        h={}
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()
        cur2.execute("SELECT customer_id,customer_name FROM [masters].[tbl_customer] where is_active=1 and is_deleted=0")
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
    def add_project_details(ProjectName, ProjectCode, ClientName, ContractName, Practice, BU, projectgroup, ProjectType, Block, Product, StartDate, EndDate, isactive, project_id, user_id):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec	[masters].[sp_add_edit_project] ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?'
        values = (ProjectName, ProjectCode, ClientName, ContractName, Practice, BU, projectgroup, ProjectType, Block, Product, StartDate, EndDate, isactive, project_id, user_id)
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
        sql = 'SELECT * FROM [masters].[tbl_projects] where project_id=?'
        values = (glob_project_id,)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[3]+"":row[3],""+columns[5]+"":row[5],""+columns[6]+"":row[6]}
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
    def add_center_details(center_name,user_id,is_active,center_id,center_type_id,center_category_id,bu_id,region_id,cluster_id,country_id,satet_id,district_id,location_name):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec	[masters].[sp_add_edit_centers] ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?'
        values = (center_name,user_id,is_active,center_id,center_type_id,center_category_id,bu_id,region_id,cluster_id,country_id,satet_id,district_id,location_name)
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
        sql = 'SELECT * FROM [masters].[tbl_bu] where is_active=1;'
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

    def course_list(course_id,sectors,qps,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw, status):
        content = {}
        d = []
        h={}
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [content].[sp_get_course_list] ?, ?, ?, ?, ?, ?, ?, ?, ?'
        values = (course_id,sectors,qps,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,status)
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
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[3]+"":row[3]}
        cur.close()
        con.close()
        return h

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
    def trainer_list(user_id,user_region_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw,user_role_id,centers, status, Region_id, Cluster_id, Dept,entity_ids,project_ids,sector_ids):
        content = {}
        d = []
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [users].[sp_get_trainer_list] ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?,?,?'
        values = (user_id,user_region_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,user_role_id,centers, status, Region_id, Cluster_id, Dept,entity_ids,project_ids,sector_ids)
        cur.execute(sql,(values))
        print(values)
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
        
    def batch_list_updated(batch_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw,user_id,user_role_id, status, customer, project, sub_project, region, center, center_type):
        #print(status, customer, project, course, region, center)
        content = {}
        d = []
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [batches].[sp_get_batch_list_updatd] ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?'
        values = (batch_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,user_id,user_role_id, status, customer, project, sub_project, region, center, center_type)
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

    def add_batch_details(BatchName, BatchCode, Product, Center, Course, SubProject, Cofunding, Trainer, isactive, StartDate, EndDate, StartTime, EndTime, BatchId, user_id):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec	batches.sp_add_edit_batches ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?'
        values = (BatchName, BatchCode, Product, Center, Course, SubProject, Cofunding, Trainer, isactive, StartDate, EndDate, StartTime, EndTime, BatchId, user_id)
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
        sql = 'SELECT * FROM [batches].[tbl_batches] where batch_id=?'
        values = (batch_id,)
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[3]+"":row[3],""+columns[4]+"":row[4],""+columns[5]+"":row[5],""+columns[6]+"":row[6],""+columns[7]+"":row[7],""+columns[8]+"":row[8],""+columns[9]+"":row[9],""+columns[10]+"":row[10],""+columns[12]+"":row[12],""+columns[13]+"":row[13],""+columns[14]+"":row[14],""+columns[15]+"":row[15],""+columns[16]+"":row[16],""+columns[17]+"":row[17],""+columns[18]+"":row[18]}
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

    def drop_edit_map_candidate_batch(candidate_ids,batch_id,course_id,user_id,drop_remark):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec	[candidate_details].[drop_edit_map_candidate_batch] ?, ?, ?, ?, ?'
        values = (candidate_ids,batch_id,course_id,user_id,drop_remark)
        cur.execute(sql,(values))
        for row in cur:
            pop=row[1]
        cur.commit()
        cur.close()
        con.close()
        if pop ==1:
            msg={"message":"Candidate Dropout"}
        else:
            msg={"message":"Error fetching batch data for Droping"}
        return msg

    def qp_list(qp_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw, sectors):
        content = {}
        d = []
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [masters].[sp_get_qp_list] ?, ?, ?, ?, ?, ?, ?'
        values = (qp_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction, sectors)
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

    def candidate_list(candidate_id,customer,project,sub_project,region,center,center_type,status,user_id,user_role_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        content = {}
        d = []
        h={}
        
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [candidate_details].[sp_get_candidate_web_list_new] ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?,?'
        values = (candidate_id,customer,project,sub_project,region,center,center_type,status,user_id,user_role_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction)
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
    def get_cand_center_basedon_course_multiple(course_id, RegionId):
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

    def client_list(client_id,Is_Active,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw, funding_sources,customer_groups,category_type_ids):
        content = {}
        d = []
        h={}
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [masters].[sp_get_client_list] ?, ?, ?, ?, ?, ?, ?, ?, ?, ?'
        values = (client_id,Is_Active, funding_sources,customer_groups,category_type_ids,start_index,page_length,search_value,order_by_column_position,order_by_column_direction)
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

    def add_contract_details(ContractName, ContractCode, ClientName, EntityName, SalesCatergory, StartDate, EndDate, isactive, user_id, contract_id):
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec	[masters].[sp_add_edit_contract] ?, ?, ?, ?, ?, ?, ?, ?, ?, ?'
        values = (ContractName, ContractCode, ClientName, EntityName, SalesCatergory, StartDate, EndDate, isactive, user_id, contract_id)
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

    def contract_list(contract_id,customer_ids,stage_ids,from_date,to_date,entity_ids,sales_category_ids,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        content = {}
        d = []
        h={}
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [masters].[sp_get_contract_list] ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?'
        values = (contract_id,customer_ids,stage_ids,from_date,to_date,entity_ids,sales_category_ids,start_index,page_length,search_value,order_by_column_position,order_by_column_direction)
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
    def get_project_basedon_client_multiple(client_id):
        project = []
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()
        #print(client_id)
        sql = """SELECT project_id, project_name FROM masters.tbl_projects WHERE is_active=1 and is_deleted=0 and ('{}'='-1' or customer_id in (select value from string_split('{}',',') where trim(value)!=''))""".format(client_id, client_id)  #'{}'='' or 
        cur2.execute(sql)
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
    def GetSubProjectsForCenter_course(center_id, course_id, sub_project_id):
        response = []
        h={}
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()
        sql = 'exec [masters].[sp_get_sub_projects_for_center_course]  ?, ?, ?'
        values = (center_id, course_id, sub_project_id)
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

    def Get_all_Center_db():
        response=[]
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [masters].[get_all_Center]'
        cur.execute(sql)
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
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[3]+"":row[3],""+columns[4]+"":row[4]}
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
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2], ""+columns[3]+"":row[3],""+columns[4]+"":row[4],""+columns[5]+"":row[5]}
            response.append(h)

        out = {'sub_project':response,'project_name':row[6],'project_code':row[7]}
        cur.commit()
        cur.close()
        con.close()       
        return out

    def get_subproject_basedon_proj_multiple(project_id):
        courses = []
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()

        sql = """SELECT distinct sub_project_id, sub_project_name FROM masters.tbl_sub_projects WHERE is_active=1 and is_deleted=0 and ('{}'='-1' or project_id in (select value from string_split('{}',',') where trim(value)!=''))""".format(project_id, project_id)  #'{}'='' or 
        cur2.execute(sql)
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
    def AllCourse_center_db(cls, center_id):
        response=[]
        con = pyodbc.connect(conn_str)
        cur = con.cursor()
        sql = 'exec [masters].[sp_course_basedon_center] ?'
        values = (center_id, )
        cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        for row in cur:
            h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1]}
            response.append(h)
        cur.commit()
        cur.close()
        con.close()       
        return response