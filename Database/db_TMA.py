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

'''
cur.execute(sql,(values))
        columns = [column[0].title() for column in cur.description]
        #cur.execute("SELECT u.user_id,u.user_name,u.user_role_id FROM users.tbl_users AS u LEFT JOIN users.tbl_user_details AS ud ON ud.user_id=u.user_id where ud.email='"+email+"' AND u.password='"+passw+"';")
        for row in cur:
            for i in range(len(columns)):
                h[columns[i]]=row[i]
            #h = {""+columns[0]+"":row[0],""+columns[1]+"":row[1],""+columns[2]+"":row[2],""+columns[3]+"":row[3]}
            tr.append(h)
        cur.commit()
'''

class TMADatabase:
    def AppVersionCheck(curs, app_version):
        quer = "SELECT TOP (1) version_code FROM [masters].[tbl_mclg_app_version_history] order by id desc"
        curs.execute(quer)
        data=curs.fetchall()
        data = 0 if data==[] else data[0][0]
        return (int(app_version) >= int(data))

    def GetBatchCandidateList_db(batch_id,session_id):
        con = pyodbc.connect(conn_str)
        curs = con.cursor()
        quer = "call [masters].[sp_tma_get_batch_candidates]({},{})".format(batch_id, session_id)
        quer = "{"+ quer + "}"
        curs.execute(quer)
        data = curs.fetchall()
        CandidateList=[]
        if len(data)>0:
            for candidate in data:
                CandidateList.append({'candidate_name':candidate[0],'enrollment_id': candidate[1],'guardian_name': candidate[2],'phone': candidate[3],'gender': candidate[4],'date_of_birth': candidate[5],'attendance_date': candidate[6],'attendance': candidate[7],'image_file_name': candidate[8]})
        return CandidateList
    
    def GetSessionPlanModuleDetailsForCourse(course_id,qp_id):
        con = pyodbc.connect(conn_str)
        curs = con.cursor()
        quer="call [masters].[sp_get_tma_session_plan_module]({},{})".format(course_id,qp_id)
        quer="{"+quer+"}"
        curs.execute(quer)
        data=curs.fetchall()
        out=[]
        if(data!=None):
            set_id = set(list(map(lambda x:x[1], data)))                    
            for  i in set_id:
                temp={}
                temp_module_id = list(filter(lambda x: x[1]==i, data))
                temp['course_id'] = 0 if temp_module_id[0][0]==None else temp_module_id[0][0]
                temp['session_plan_id']=0 if temp_module_id[0][1]==None else temp_module_id[0][1]
                temp['session_plan_name'] = temp_module_id[0][2]
                temp['modules'] = [{'module_id':0 if module[3]==None else module[3], 'module_name':module[4]} for module in temp_module_id]
                out.append(temp)
        return out

    def GetBatchSessionCurrentStageDetails(batch_id,session_id,user_id):
        con = pyodbc.connect(conn_str)
        curs = con.cursor()
        quer = "call [masters].[sp_tma_get_batch_session_current_stage_detail]({},{},{})".format(user_id, batch_id, session_id)
        quer = "{"+ quer + "}"
        curs.execute(quer)
        data = curs.fetchall()
        #print(data)
        StageId=0
        if data!=[]:
            StageId=data[0][0]
        curs.close()
        con.close()
        return StageId

    def GetBatchListForTMA(BatchStatusId,UserId,CenterId,role_id,app_version):
        con = pyodbc.connect(conn_str)
        curs = con.cursor()
        if TMADatabase.AppVersionCheck(curs, app_version):
            quer="call [batches].[sp_tma_get_batch_list]({},{},{},{})".format(BatchStatusId, UserId,CenterId,role_id)
            quer = "{"+ quer + "}"
            curs.execute(quer)
            data=curs.fetchall()
            BatchList=[]
            if ((data!=None)and(data!=[])):
                for batch in data:
                    BatchList.append({'batch_id':batch[0],'batch_code': batch[1],'batch_start_date': batch[2],'batch_end_date': batch[3],'batch_status': batch[4],'batch_active_status': batch[5],'batch_stage_id': batch[6],'batch_stage_name': batch[7],'business_unit': batch[8],'center_name': batch[9],'center_type': batch[10],'course_id': batch[11],'course_code': batch[12],'course_name': batch[13],'qp_id': batch[14],'qp_code': batch[15],'qp_name': batch[16],'image_required': batch[17],'center_id': batch[18]})
            res={'status':1,'message':'Success','batch_list':BatchList,'app_status':True}
        else:
            res={'status':1,'message':'Failed lower app version','app_status':False}
        curs.close()
        con.close()
        return res

    def GetBatchSessionListForTMA(BatchId,UserId,SessionPlanId,ModuleId,StatusId,SessionName,app_version):
        con = pyodbc.connect(conn_str)
        curs = con.cursor()
        if TMADatabase.AppVersionCheck(curs, app_version):
            quer="call [batches].[sp_tma_get_batch_sessions]({},{},{},{},{},'{}')".format(BatchId, UserId,SessionPlanId,ModuleId,StatusId,SessionName)
            quer = "{"+ quer + "}"
            curs.execute(quer)
            data=curs.fetchall()
            SessionList=[]
            #return data
            if ((data!=None)and(data!=[])):
                for i in range(len(data)):
                    is_active=False
                    if data[i][11]<4:
                        if i==0:
                            is_active=True
                            stg_id=data[i][11]  #11 - session stage id
                        elif stg_id==4:
                            is_active=True
                            stg_id=data[i][11]
                        elif (stg_id<4)and(stg_id==data[i][11]):
                            is_active=True
                            #stg_id=data[i][11]
                        else:
                            is_active=False
                            #stg_id=data[i][11]
                        SessionList.append({'session_id':data[i][0],'session_name': data[i][1],'course_id': data[i][2],'course_code': data[i][3],'course_name': data[i][4],'qp_id': data[i][5],'qp_code': data[i][6],'qp_name': data[i][7],'status_id': data[i][8],'status_name': data[i][9],'session_duration': data[i][10],'session_stage_id':data[i][11],'session_stage_name':data[i][12],'session_order':data[i][13],'is_active':is_active})
                    elif data[i][11]==4:
                        stg_id=data[i][11]
                        SessionList.append({'session_id':data[i][0],'session_name': data[i][1],'course_id': data[i][2],'course_code': data[i][3],'course_name': data[i][4],'qp_id': data[i][5],'qp_code': data[i][6],'qp_name': data[i][7],'status_id': data[i][8],'status_name': data[i][9],'session_duration': data[i][10],'session_stage_id':data[i][11],'session_stage_name':data[i][12],'session_order':data[i][13],'is_active':is_active})
                #for session in data:
                #    SessionList.append({'session_id':session[0],'session_name': session[1],'course_id': session[2],'course_code': session[3],'course_name': session[4],'qp_id': session[5],'qp_code': session[6],'qp_name': session[7],'status_id': session[8],'status_name': session[9],'session_duration': session[10],'session_stage_id':session[11],'session_stage_name':session[12],'session_order':session[13]})
                res={'status':1,'message':'Success','session_list':SessionList,'app_status':True}
            else:
                res={'status':1,'message':'No session(s) found','session_list':SessionList,'app_status':True}
        else:
            res={'status':1,'message':'Failed lower app version','app_status':False}
        curs.close()
        con.close()
        return res
        
    def LogTrainerStageDetails(session_id,user_id,batch_id,stage_id,latitude,longitude,image_file_name,mark_candidate_attendance,attendance_data,group_attendance_image_data,app_version):
        con = pyodbc.connect(conn_str)
        curs = con.cursor()
        if TMADatabase.AppVersionCheck(curs, app_version):
            quer = "call [masters].[sp_tma_log_trainer_stage_details]({},'{}',{},{},'{}','{}','{}',{},'{}','{}')".format(batch_id,session_id,user_id,stage_id,latitude,longitude,image_file_name,mark_candidate_attendance,attendance_data,group_attendance_image_data)
            quer = "{"+ quer + "}"
            curs.execute(quer)
            data = curs.fetchall()[0]
            if len(data)==0:
                res = {'status':0, 'message':'Not able to log','app_status':True}
            else:
                res = {'status':1,'message':'Success','app_status':True}
        else:
            res={'status':1,'message':'Failed lower app version','app_status':False}
        curs.commit()
        curs.close()
        con.close()
        return res
        
    def GetSubProjectsForCustomer(customer_ids):
        response = []
        h={}
        con = pyodbc.connect(conn_str)
        cur2 = con.cursor()
        sql = 'exec [masters].[sp_get_sub_projects_for_customer]  ?'
        values = (customer_ids,)
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