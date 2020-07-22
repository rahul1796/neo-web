from Database import Database
from Database import config
from datetime import datetime
import pandas as pd
import xlsxwriter,re,os

class Report:
    def AllRegionsBasedOnUser(UserId,UserRoleId,UserRegionId):
        return Database.AllRegionsBasedOnUser(UserId,UserRoleId,UserRegionId)
    def AllAssessmentStages(UserId,UserRoleId):
        return Database.AllAssessmentStages(UserId,UserRoleId)
    def GetAllCentersBasedOnRegion_User(UserId,UserRoleId,RegionId):
        return Database.GetAllCentersBasedOnRegion_User(UserId,UserRoleId,RegionId)
    def GetAllCoursesBasedOnCenter_User(UserId,UserRoleId,CenterId):
        return Database.GetAllCoursesBasedOnCenter_User(UserId,UserRoleId,CenterId)
    def GetAllTrainersBasedOnCenter_User(UserId,UserRoleId,CenterId):
        return Database.GetAllTrainersBasedOnCenter_User(UserId,UserRoleId,CenterId)
    def GetAllMobilizersBasedOnCenter_User(UserId,UserRoleId,CenterId):
        return Database.GetAllMobilizersBasedOnCenter_User(UserId,UserRoleId,CenterId)
    def TrainerDeploymentBatches(region_id,sub_project_ids,course_ids,trainer_ids,from_date,to_date,batch_stage_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        return Database.TrainerDeploymentBatches(region_id,sub_project_ids,course_ids,trainer_ids,from_date,to_date,batch_stage_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)
    def ReportAttendanceBatches(region_id,sub_project_ids,course_ids,trainer_ids,from_date,to_date,batch_stage_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw, user_id, user_role_id):
        return Database.ReportAttendanceBatches(region_id,sub_project_ids,course_ids,trainer_ids,from_date,to_date,batch_stage_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw, user_id, user_role_id)
    def ReportBatchSession(batch_id,course_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        return Database.ReportBatchSession(batch_id,course_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)
    def GetBatchDetailsForAttReport(batch_id):
        return Database.GetBatchDetailsForAttReport(batch_id)
    def GetSessionTrainerActivity(batch_id,session_id):
        return Database.GetSessionTrainerActivity(batch_id,session_id)
    def GetCandidateSessionAttendance(batch_id,session_id):
        return Database.GetCandidateSessionAttendance(batch_id,session_id)
    def GetCandidateGrpAttendance(batch_id,session_id):
        return Database.GetCandidateGrpAttendance(batch_id,session_id)
    def GetMobilizationReportData(region_id,center_id,course_ids,mobilizer_ids,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        return Database.GetMobilizationReportData(region_id,center_id,course_ids,mobilizer_ids,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw) 
    def GetRegisteredCandidatesList(center_id,course_id,mobilizer_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        return Database.GetRegisteredCandidatesList(center_id,course_id,mobilizer_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)
    def GetCandidateBasicDetails(candidate_id):
        return Database.GetCandidateBasicDetails(candidate_id)   
    def GetAllClustersBasedOnMultipleRegion_User(UserId,UserRoleId,RegionIds):
        return Database.GetAllClustersBasedOnMultipleRegion_User(UserId,UserRoleId,RegionIds)
    def GetAllCentersBasedOnMultipleClusters_User(UserId,UserRoleId,ClusterIds):
        return Database.GetAllCentersBasedOnMultipleClusters_User(UserId,UserRoleId,ClusterIds)
    def GetAllCoursesBasedOnMultipleCenters_User(UserId,UserRoleId,CenterIds):
        return Database.GetAllCoursesBasedOnMultipleCenters_User(UserId,UserRoleId,CenterIds)
    def GetAllCooBasedOnMultipleRegions_User(UserId,UserRoleId,RegionIds):
        return Database.GetAllCooBasedOnMultipleRegions_User(UserId,UserRoleId,RegionIds)
    def GetAllTmBasedOnMultipleClusters_User(UserId,UserRoleId,ClusterIds):
        return Database.GetAllTmBasedOnMultipleClusters_User(UserId,UserRoleId,ClusterIds)
    def tma_registration_compliance_report(region_id,cluster_id,center_id,center_type_id,course_id,tm,coo,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        return Database.tma_registration_compliance_report(region_id,cluster_id,center_id,center_type_id,course_id,tm,coo,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)
    def download_tma_registration_compliance_report(region_id,cluster_id,center_id,center_type_id,course_id,tm,coo,path):
        response= Database.download_tma_registration_compliance_report(region_id,cluster_id,center_id,center_type_id,course_id,tm,coo)
        FileName=Report.CreateExcelTmaRegistrationCompliance(response,path)
    def CreateExcelTmaRegistrationCompliance(data,path):
        filename=''
        col=['Region_Name', 'Cluster_Name', 'Center_Type_Name', 'Center_Name', 'Course_Name', 'Batch_Count', 'Trainer_Count', 'Tma_Used_Trainer','Coo','Tm']
        
        try:
            workbook = xlsxwriter.Workbook(path)

            header_format = workbook.add_format({
                'bold': True,
                #'text_wrap': True,
                'align': 'top',
                'valign': 'center',
                'fg_color': '#D7E4BC',
                'border': 1})

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
            worksheet = workbook.add_worksheet('TMA Registration Compliance')
            for i in range(len(col)):
                worksheet.write(0,i ,col[i], header_format)   
            for j in range(len(data)) : 
                for k in range(len(col)):
                    worksheet.write(j+1,k ,data.iloc[j,k],write_format)
                            
            workbook.close()
        except Exception as e:
            print(str(e))
            
        return path
    def trainerwise_tma_registration_compliance_report(region_id,cluster_id,center_id,center_type_id,course_id,tm,coo,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        return Database.trainerwise_tma_registration_compliance_report(region_id,cluster_id,center_id,center_type_id,course_id,tm,coo,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)
    def download_trainerwise_tma_registration_compliance_report(region_id,cluster_id,center_id,center_type_id,course_id,tm,coo,path):
        response= Database.download_trainerwise_tma_registration_compliance_report(region_id,cluster_id,center_id,center_type_id,course_id,tm,coo)
        FileName=Report.CreateExcelTrainerTmaRegistrationCompliance(response,path)
    def CreateExcelTrainerTmaRegistrationCompliance(data,path):
        filename=''
        col=['Trainer_Name','Region_Name', 'Cluster_Name', 'Center_Type_Name', 'Center_Name', 'Course_Name', 'Batch_Count','Coo','Tm']
        print(path)
        try:
            workbook = xlsxwriter.Workbook(path)

            header_format = workbook.add_format({
                'bold': True,
                #'text_wrap': True,
                'align': 'top',
                'valign': 'center',
                'fg_color': '#D7E4BC',
                'border': 1})

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
            worksheet = workbook.add_worksheet('Trainerwise TMA Registration')
            print(worksheet.name)
            for i in range(len(col)):
                worksheet.write(0,i ,col[i], header_format)   
            for j in range(len(data)) : 
                for k in range(len(col)):
                    worksheet.write(j+1,k ,data.iloc[j,k],write_format)
                            
            workbook.close()
        except Exception as e:
            print(str(e))
            
        return path
    
    def GetECPReportData(user_id,user_role_id,customer_ids,contract_ids,region_ids,from_date,to_date):
        return Database.GetECPReportData(user_id,user_role_id,customer_ids,contract_ids,region_ids,from_date,to_date)
    def GetMobilizerReportData(user_id,user_role_id,Role, Date):
        return Database.GetMobilizerReportData(user_id,user_role_id,Role, Date)

    def GetQpWiseReportData(user_id,user_role_id,customer_ids,contract_ids,from_date,to_date):
        return {"Data":Database.GetQpWiseReportData(user_id,user_role_id,customer_ids,contract_ids,from_date,to_date)}
    def GetQpWiseRegionLevelData(user_id,user_role_id,customer_ids,contract_ids,from_date,to_date,qp_id):
        return {"Data":Database.GetQpWiseRegionLevelData(user_id,user_role_id,customer_ids,contract_ids,from_date,to_date,qp_id)}
    def GetQpWiseRegionWiseBatchLevelData(user_id,user_role_id,customer_ids,contract_ids,from_date,to_date,qp_id,region_id):
        res=Database.GetQpWiseRegionWiseBatchLevelData(user_id,user_role_id,customer_ids,contract_ids,from_date,to_date,qp_id,region_id)
        return {"Data":res['response']}
    
    def DownloadBatchReport(user_id,user_role_id,customer_ids,contract_ids):
        try:
            DownloadPath=config.neo_report_file_path+'report file/'
            report_name = config.BatchReportFileName+datetime.now().strftime('%Y_%m_%d_%H_%M_%S')+".xlsx"  
            r=re.compile(config.BatchReportFileName + ".*")
            lst=os.listdir(DownloadPath)
            newlist = list(filter(r.match, lst))
            for i in newlist:
                os.remove( DownloadPath + i)
            path = '{}{}'.format(DownloadPath,report_name)
            response=Database.GetQpWiseDownloadData(user_id,user_role_id,customer_ids,contract_ids)
            
            df=pd.DataFrame(response)
            
            df=df[[ 'Customer_Name','Contract_Name','Qp_Code','Qp_Name','Batch_Count','Target_Enrolment','Target_Certification','Target_Placement','Enrolled','Dropped','Certified','In_Training','Placement']]
            columns=['Customer Name','Contract Name', 'Qp Code','Qp Name','Batch Count','Target Enrolment','Target Certification','Target Placement','Enrolled','Dropped','Certified','In Training','Placement']
            temp_qp={"data":df,"columns":columns} 
                     
            response=Database.GetRegionWiseDownloadData(user_id,user_role_id,customer_ids,contract_ids)
            
            df=pd.DataFrame(response)
            df=df[['Region_Name', 'Customer_Name','Contract_Name','Qp_Code','Qp_Name','Target_Enrolment','Target_Certification','Target_Placement','Enrolled','Dropped','Certified','In_Training','Placement']]
            columns=['Region Name','Customer Name','Contract Name','Qp Code', 'Qp Name','Target Enrolment','Target Certification','Target Placement','Enrolled','Dropped','Certified','In Training','Placement']
            temp_region={"data":df,"columns":columns}

            response=Database.GetQpWiseRegionWiseBatchLevelData(user_id,user_role_id,customer_ids,contract_ids,'','',0,0)
            df1=pd.DataFrame(response['response'])
            df1=df1[['Region_Name', 'Qp_Name','Center_Name','Batch_Code','Actual_Start_Date','Actual_End_Date','Enrolled','Dropped','Certified','In_Training','Placement']]
            columns=['Region Name', 'Qp Name','Center Name','Batch Code','Actual Start Date','Actual End Date','Enrolled','Dropped','Certified','In Training','Placement']
            temp_batch={"data":df1,"columns":columns}
            
            res=Report.CreateExcel(temp_qp,temp_region,temp_batch,path)
            print(res)
            if res['success']:
                return {"success":True,"msg":"Report Created.",'FileName':report_name,'FilePath':config.neo_report_file_path_web}
            else:
                return {"success":False,"msg":res['msg']}
        except Exception as e:
            return {"success":False,"msg":str(e)}

    def CreateExcel(Response_qp,Response_region,Response_batch,file_path):
        try:
            
            workbook = xlsxwriter.Workbook(file_path)
            
            header_format = workbook.add_format({
                'bold': True,
                #'text_wrap': True,
                'align': 'top',
                'valign': 'center',
                'fg_color': '#D7E4BC',
                'border': 1})

            write_format = workbook.add_format({
                'border': 1,
                'align': 'top',
                'valign': 'top'})
            worksheet = workbook.add_worksheet('QP_Wise')          
            
            #print(worksheet.name)
            for i in range(len(Response_qp['columns'])):
                worksheet.write(0,i ,Response_qp['columns'][i], header_format)   
            for j in range(len(Response_qp['data'])) : 
                for k in range(len(Response_qp['columns'])):
                    if Response_qp['data'].iloc[j,k] is None:
                        worksheet.write(j+1,k ,'',write_format)
                    else:
                        worksheet.write(j+1,k ,Response_qp['data'].iloc[j,k],write_format)

            worksheet = workbook.add_worksheet('Region_Wise')
            for i in range(len(Response_region['columns'])):
                worksheet.write(0,i ,Response_region['columns'][i], header_format)   
            for j in range(len(Response_region['data'])) : 
                for k in range(len(Response_region['columns'])):
                    if Response_region['data'].iloc[j,k] is None:
                        worksheet.write(j+1,k ,'',write_format)
                    else:
                        worksheet.write(j+1,k ,Response_region['data'].iloc[j,k],write_format)

            worksheet = workbook.add_worksheet('Batch_Wise')
            for i in range(len(Response_batch['columns'])):
                worksheet.write(0,i ,Response_batch['columns'][i], header_format)   
            for j in range(len(Response_batch['data'])) : 
                for k in range(len(Response_batch['columns'])):
                    if Response_batch['data'].iloc[j,k] is None:
                        worksheet.write(j+1,k ,'',write_format)
                    else:
                        worksheet.write(j+1,k ,Response_batch['data'].iloc[j,k],write_format)
                                                    
            workbook.close()
            return {"success":True}
        except Exception as e:
            print(str(e))
            return {"success":False,"msg":str(e)}

    def user_sub_project_list(customer,project,sub_project,region,user_id,user_role_id,employee_status,sub_project_status,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        return Database.user_sub_project_list(customer,project,sub_project,region,user_id,user_role_id,employee_status,sub_project_status,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)
    
    def DownloadBatchStatusReport(user_id,user_role_id,customer_ids,contract_ids,contract_status,batch_status,from_date,to_date):
        try:
            DownloadPath=config.neo_report_file_path+'report file/'
            report_name = config.BatchStatusReportFileName+datetime.now().strftime('%Y_%m_%d_%H_%M_%S')+".xlsx"  
            r=re.compile(config.BatchStatusReportFileName + ".*")
            lst=os.listdir(DownloadPath)
            newlist = list(filter(r.match, lst))
            for i in newlist:
                os.remove( DownloadPath + i)
            path = '{}{}'.format(DownloadPath,report_name)
            response=Database.DownloadBatchStatusReport(user_id,user_role_id,customer_ids,contract_ids,contract_status,batch_status,from_date,to_date)
            
            df=pd.DataFrame(response)
            if len(df.index)>0:
                df=df[[ 'Practice_Name','Customer_Name','Contract_Code','Contract_Name','Project_Code','Project_Name','Sub_Project_Code','Sub_Project_Name','Center_Name','Product_Name','Bu_Name','Region_Name','Batch_Code','Course_Code','Course_Name','Status','Actual_Start_Date','Actual_End_Date','Unit_Rate','E_Ratio','C_Ratio','P_Ratio','Batch_Enrolled','Batch_Dropped','Batch_Certified','Certification_Distribution','Batch_Placement','Placement_Count_Rr','Placement_Is_Per_Of','Ojt_Completed','Filtered_Enrolled','Filtered_Dropped','Filtered_Certified','Filtered_Certification_Distribution','Filtered_Placed','Filtered_Placement_Count_Rr','Filtered_Ojt_Completed','Excess_No','Excess_Revenue','Overall_Revenue','Mon_Revenue']]
                columns=[ 'Practice','Customer','Contract Code','Contract Name','Project Code','Project Name','Sub Project Code','Sub Project Name','Center','Product','BU','Region','Batch Code','Course Code','Course Name','Status','Actual Start Date','Actual End Date','Unit Rate','E Ratio','C Ratio','P Ratio','Enrolled','Dropped','Certified','Certificates Distribution','Placed','Placement Count(RR)','Placement Is Percent Of','Ojt Completed','Enrolled(Selected Duration)','Dropped(Selected Duration)','Certified(Selected Duration)','Certificates Distribution(Selected Duration)','Placed(Selected Duration)','Placement Count RR(Selected Duration)','Ojt Completed(Selected Duration)','Excess No','Excess Revenue','Revenue(Without Excess)','Revenue(Selected Duration)']
                temp={"data":df,"columns":columns} 
                
                res=Report.CreateExcelFun(temp,path,'Batch Status')
                print(res)
                if res:
                    return {"success":True,"msg":"Report Created.",'FileName':report_name,'FilePath':config.neo_report_file_path_web}
                else:
                    return {"success":False,"msg":res['msg']}
            else:
                return {"success":False,"msg":'No records found'} 
        except Exception as e:
            return {"success":False,"msg":str(e)}
    
    #Please do not edit/remove the below function and try to reuse the same to create an excel with single sheet by passing data and sheet name as paramenters. 
    #Response param is tuple as shown {"data":df,"columns":column_names}.
    def CreateExcelFun(Response,file_path,sheet_name):
        try:
            #print(Response)
            workbook = xlsxwriter.Workbook(file_path)
            
            header_format = workbook.add_format({
                'bold': True,
                #'text_wrap': True,
                'align': 'top',
                'valign': 'center',
                'fg_color': '#D7E4BC',
                'border': 1})

            write_format = workbook.add_format({
                'border': 1,
                'align': 'top',
                'valign': 'top'})

            worksheet = workbook.add_worksheet(sheet_name)
            #print(worksheet.name)
            for i in range(len(Response['columns'])):
                worksheet.write(0,i ,Response['columns'][i], header_format)   
            for j in range(len(Response['data'])) : 
                for k in range(len(Response['columns'])):
                    if Response['data'].iloc[j,k] is None:
                        worksheet.write(j+1,k ,'',write_format)
                    else:
                        worksheet.write(j+1,k ,Response['data'].iloc[j,k],write_format)
                                                    
            workbook.close()
            return True
        except Exception as e:
            print(str(e))
            return False
    def GetBatchStatusReportDataList(user_id,user_role_id,customer_ids,contract_ids,contract_status,batch_status,from_date,to_date,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        return Database.GetBatchStatusReportDataList(user_id,user_role_id,customer_ids,contract_ids,contract_status,batch_status,from_date,to_date,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw) 
    def DownloadOpsProductivityReport(customer_ids,contract_ids,month,role_id):
        try:
            data=Database.DownloadOpsProductivityReport(customer_ids,contract_ids,month,role_id)
            DownloadPath=config.neo_report_file_path+'report file/'
            report_name = config.OpsProductivityFileName+datetime.now().strftime('%Y_%m_%d_%H_%M_%S')+".xlsx"  
            r=re.compile(config.OpsProductivityFileName + ".*")
            lst=os.listdir(DownloadPath)
            newlist = list(filter(r.match, lst))
            for i in newlist:
                os.remove( DownloadPath + i)
            path = '{}{}'.format(DownloadPath,report_name)
            res={}
            if int(role_id)==11:
                res=Report.CreateExcelForOpsProductivityCOO(data,role_id,path)
            if int(role_id)==14:
                res=Report.CreateExcelForOpsProductivityTM(data,role_id,path)
            if int(role_id)==5:
                res=Report.CreateExcelForOpsProductivityCM(data,role_id,path)
            if res['success']:
                return {"success":True,"msg":"Report Created.",'FileName':report_name,'FilePath':config.neo_report_file_path_web}
            else:
                return {"success":False,"msg":res['msg']}
        except Exception as e:
            return {"success":False,"msg":str(e)}
    def CreateExcelForOpsProductivityCOO(data,role_id,path):
        try:
            writer = pd.ExcelWriter(path, engine='xlsxwriter')
            workbook  = writer.book

            header_format = workbook.add_format({
                'bold': True,
                #'text_wrap': True,
                'valign': 'center',
                'fg_color': '#D7E4BC',
                'border': 1})
            df = pd.DataFrame(data['sheet1'], columns=data['sheet1_columns'])
            df.to_excel(writer, index=None, header=None ,startrow=3 ,sheet_name='Userwise') 

            df = pd.DataFrame(data['sheet2'], columns=data['sheet2_columns'])
            df.to_excel(writer, index=None, header=None ,startrow=3 ,sheet_name='User-Sub Project') 

            df = pd.DataFrame(data['sheet3'], columns=data['sheet3_columns'])
            df.to_excel(writer, index=None, header=None ,startrow=3 ,sheet_name='User-Course') 

            worksheet = writer.sheets['Userwise']
            default_column = ['COO']
            first_row = ['Enrolment', 'New Batch Start','Training Nos', 'Certification','Placement']
            second_row = ['Target', 'Actual','Target', 'Actual','Actual','Target', 'Actual','Target', 'Actual']
            third_row = ['W-1', 'W-2','W-3','W-4','Total','W-1', 'W-2','W-3','W-4','Total','%', 'W-1', 'W-2','W-3','W-4','Total','W-1', 'W-2','W-3','W-4','Total','%',
                         'W-1', 'W-2','W-3','W-4','Total',
                         'W-1', 'W-2','W-3','W-4','Total','W-1', 'W-2','W-3','W-4','Total','%','W-1', 'W-2','W-3','W-4','Total','W-1', 'W-2','W-3','W-4','Total','%',]
            
            for col_num, value in enumerate(default_column):
                worksheet.merge_range(0, col_num, 2, col_num, value, header_format)
            col=1
            for col_num, value in enumerate(first_row):
                if col_num==2:
                    worksheet.merge_range(0, col, 0, 4+col, value, header_format)
                    col=col+5                    
                else:
                    worksheet.merge_range(0, col, 0, 10+col, value, header_format)
                    col=col+11
            col=1
            for col_num, value in enumerate(second_row):
                if col_num==4:
                    worksheet.merge_range(1, col, 1, 4+col, value, header_format)
                    col=col+5
                elif value=='Target':
                    worksheet.merge_range(1, col, 1, 4+col, value, header_format)
                    col=col+5
                elif value=='Actual':
                    worksheet.merge_range(1, col, 1, 5+col, value, header_format)
                    col=col+6
                
            for col_num, value in enumerate(third_row):
                worksheet.write(2, 1+col_num, value, header_format)

            worksheet = writer.sheets['User-Sub Project']
            default_column = ['COO','Sub Project']
            for col_num, value in enumerate(default_column):
                worksheet.merge_range(0, col_num, 2, col_num, value, header_format)
            col=2
            for col_num, value in enumerate(first_row):
                if col_num==2:
                    worksheet.merge_range(0, col, 0, 4+col, value, header_format)
                    col=col+5                    
                else:
                    worksheet.merge_range(0, col, 0, 10+col, value, header_format)
                    col=col+11
            col=2
            for col_num, value in enumerate(second_row):
                if col_num==4:
                    worksheet.merge_range(1, col, 1, 4+col, value, header_format)
                    col=col+5
                elif value=='Target':
                    worksheet.merge_range(1, col, 1, 4+col, value, header_format)
                    col=col+5
                elif value=='Actual':
                    worksheet.merge_range(1, col, 1, 5+col, value, header_format)
                    col=col+6                
            for col_num, value in enumerate(third_row):
                worksheet.write(2, 2+col_num, value, header_format)

            worksheet = writer.sheets['User-Course']            
            default_column = ['COO','Course']
            for col_num, value in enumerate(default_column):
                worksheet.merge_range(0, col_num, 2, col_num, value, header_format)
            col=2
            for col_num, value in enumerate(first_row):
                if col_num==2:
                    worksheet.merge_range(0, col, 0, 4+col, value, header_format)
                    col=col+5                    
                else:
                    worksheet.merge_range(0, col, 0, 10+col, value, header_format)
                    col=col+11
            col=2
            for col_num, value in enumerate(second_row):
                if col_num==4:
                    worksheet.merge_range(1, col, 1, 4+col, value, header_format)
                    col=col+5
                elif value=='Target':
                    worksheet.merge_range(1, col, 1, 4+col, value, header_format)
                    col=col+5
                elif value=='Actual':
                    worksheet.merge_range(1, col, 1, 5+col, value, header_format)
                    col=col+6
            for col_num, value in enumerate(third_row):
                worksheet.write(2, 2+col_num, value, header_format)
            writer.save()
            return({'msg':'created excel', 'success':True, 'filename':path})
        except Exception as e:
            return({'msg':'Error creating excel -'+str(e), 'success':False, 'Error':str(e)})
    def CreateExcelForOpsProductivityTM(data,role_id,path):
        try:
            writer = pd.ExcelWriter(path, engine='xlsxwriter')
            workbook  = writer.book

            header_format = workbook.add_format({
                'bold': True,
                #'text_wrap': True,
                'valign': 'center',
                'fg_color': '#D7E4BC',
                'border': 1})
            df = pd.DataFrame(data['sheet1'], columns=data['sheet1_columns'])
            df.to_excel(writer, index=None, header=None ,startrow=3 ,sheet_name='Userwise') 

            df = pd.DataFrame(data['sheet2'], columns=data['sheet2_columns'])
            df.to_excel(writer, index=None, header=None ,startrow=3 ,sheet_name='User-Sub Project') 

            df = pd.DataFrame(data['sheet3'], columns=data['sheet3_columns'])
            df.to_excel(writer, index=None, header=None ,startrow=3 ,sheet_name='User-Course') 

            worksheet = writer.sheets['Userwise']
            default_column = ['COO','TM']
            first_row = ['Enrolment', 'New Batch Start','Training Nos', 'Certification','Placement']
            second_row = ['Target', 'Actual','Target', 'Actual','Actual','Target', 'Actual','Target', 'Actual']
            third_row = ['W-1', 'W-2','W-3','W-4','Total','W-1', 'W-2','W-3','W-4','Total','%', 'W-1', 'W-2','W-3','W-4','Total','W-1', 'W-2','W-3','W-4','Total','%',
                         'W-1', 'W-2','W-3','W-4','Total',
                         'W-1', 'W-2','W-3','W-4','Total','W-1', 'W-2','W-3','W-4','Total','%','W-1', 'W-2','W-3','W-4','Total','W-1', 'W-2','W-3','W-4','Total','%',]
            
            for col_num, value in enumerate(default_column):
                worksheet.merge_range(0, col_num, 2, col_num, value, header_format)
            col=2
            for col_num, value in enumerate(first_row):
                if col_num==2:
                    worksheet.merge_range(0, col, 0, 4+col, value, header_format)
                    col=col+5                    
                else:
                    worksheet.merge_range(0, col, 0, 10+col, value, header_format)
                    col=col+11
            col=2
            for col_num, value in enumerate(second_row):
                if col_num==4:
                    worksheet.merge_range(1, col, 1, 4+col, value, header_format)
                    col=col+5
                elif value=='Target':
                    worksheet.merge_range(1, col, 1, 4+col, value, header_format)
                    col=col+5
                elif value=='Actual':
                    worksheet.merge_range(1, col, 1, 5+col, value, header_format)
                    col=col+6
                
            for col_num, value in enumerate(third_row):
                worksheet.write(2, 2+col_num, value, header_format)

            worksheet = writer.sheets['User-Sub Project']
            default_column = ['COO','TM','Sub Project']
            for col_num, value in enumerate(default_column):
                worksheet.merge_range(0, col_num, 2, col_num, value, header_format)
            col=3
            for col_num, value in enumerate(first_row):
                if col_num==2:
                    worksheet.merge_range(0, col, 0, 4+col, value, header_format)
                    col=col+5                    
                else:
                    worksheet.merge_range(0, col, 0, 10+col, value, header_format)
                    col=col+11
            col=3
            for col_num, value in enumerate(second_row):
                if col_num==4:
                    worksheet.merge_range(1, col, 1, 4+col, value, header_format)
                    col=col+5
                elif value=='Target':
                    worksheet.merge_range(1, col, 1, 4+col, value, header_format)
                    col=col+5
                elif value=='Actual':
                    worksheet.merge_range(1, col, 1, 5+col, value, header_format)
                    col=col+6                
            for col_num, value in enumerate(third_row):
                worksheet.write(2, 3+col_num, value, header_format)

            worksheet = writer.sheets['User-Course']            
            default_column = ['COO','TM','Course']
            for col_num, value in enumerate(default_column):
                worksheet.merge_range(0, col_num, 2, col_num, value, header_format)
            col=3
            for col_num, value in enumerate(first_row):
                if col_num==2:
                    worksheet.merge_range(0, col, 0, 4+col, value, header_format)
                    col=col+5                    
                else:
                    worksheet.merge_range(0, col, 0, 10+col, value, header_format)
                    col=col+11
            col=3
            for col_num, value in enumerate(second_row):
                if col_num==4:
                    worksheet.merge_range(1, col, 1, 4+col, value, header_format)
                    col=col+5
                elif value=='Target':
                    worksheet.merge_range(1, col, 1, 4+col, value, header_format)
                    col=col+5
                elif value=='Actual':
                    worksheet.merge_range(1, col, 1, 5+col, value, header_format)
                    col=col+6
            for col_num, value in enumerate(third_row):
                worksheet.write(2, 3+col_num, value, header_format)
            writer.save()
            return({'msg':'created excel', 'success':True, 'filename':path})
        except Exception as e:
            return({'msg':'Error creating excel -'+str(e), 'success':False, 'Error':str(e)})
    def CreateExcelForOpsProductivityCM(data,role_id,path):
        try:
            writer = pd.ExcelWriter(path, engine='xlsxwriter')
            workbook  = writer.book

            header_format = workbook.add_format({
                'bold': True,
                #'text_wrap': True,
                'valign': 'center',
                'fg_color': '#D7E4BC',
                'border': 1})
            df = pd.DataFrame(data['sheet1'], columns=data['sheet1_columns'])
            df.to_excel(writer, index=None, header=None ,startrow=3 ,sheet_name='Userwise') 

            df = pd.DataFrame(data['sheet2'], columns=data['sheet2_columns'])
            df.to_excel(writer, index=None, header=None ,startrow=3 ,sheet_name='User-Sub Project') 

            df = pd.DataFrame(data['sheet3'], columns=data['sheet3_columns'])
            df.to_excel(writer, index=None, header=None ,startrow=3 ,sheet_name='User-Course') 

            worksheet = writer.sheets['Userwise']
            default_column = ['COO','TM','CM']
            first_row = ['Enrolment', 'New Batch Start','Training Nos', 'Certification','Placement']
            second_row = ['Target', 'Actual','Target', 'Actual','Actual','Target', 'Actual','Target', 'Actual']
            third_row = ['W-1', 'W-2','W-3','W-4','Total','W-1', 'W-2','W-3','W-4','Total','%', 'W-1', 'W-2','W-3','W-4','Total','W-1', 'W-2','W-3','W-4','Total','%',
                         'W-1', 'W-2','W-3','W-4','Total',
                         'W-1', 'W-2','W-3','W-4','Total','W-1', 'W-2','W-3','W-4','Total','%','W-1', 'W-2','W-3','W-4','Total','W-1', 'W-2','W-3','W-4','Total','%',]
            
            for col_num, value in enumerate(default_column):
                worksheet.merge_range(0, col_num, 2, col_num, value, header_format)
            col=3
            for col_num, value in enumerate(first_row):
                if col_num==2:
                    worksheet.merge_range(0, col, 0, 4+col, value, header_format)
                    col=col+5                    
                else:
                    worksheet.merge_range(0, col, 0, 10+col, value, header_format)
                    col=col+11
            col=3
            for col_num, value in enumerate(second_row):
                if col_num==4:
                    worksheet.merge_range(1, col, 1, 4+col, value, header_format)
                    col=col+5
                elif value=='Target':
                    worksheet.merge_range(1, col, 1, 4+col, value, header_format)
                    col=col+5
                elif value=='Actual':
                    worksheet.merge_range(1, col, 1, 5+col, value, header_format)
                    col=col+6
                
            for col_num, value in enumerate(third_row):
                worksheet.write(2, 3+col_num, value, header_format)

            worksheet = writer.sheets['User-Sub Project']
            default_column = ['COO','TM','CM','Sub Project']
            for col_num, value in enumerate(default_column):
                worksheet.merge_range(0, col_num, 2, col_num, value, header_format)
            col=4
            for col_num, value in enumerate(first_row):
                if col_num==2:
                    worksheet.merge_range(0, col, 0, 4+col, value, header_format)
                    col=col+5                    
                else:
                    worksheet.merge_range(0, col, 0, 10+col, value, header_format)
                    col=col+11
            col=4
            for col_num, value in enumerate(second_row):
                if col_num==4:
                    worksheet.merge_range(1, col, 1, 4+col, value, header_format)
                    col=col+5
                elif value=='Target':
                    worksheet.merge_range(1, col, 1, 4+col, value, header_format)
                    col=col+5
                elif value=='Actual':
                    worksheet.merge_range(1, col, 1, 5+col, value, header_format)
                    col=col+6                
            for col_num, value in enumerate(third_row):
                worksheet.write(2, 4+col_num, value, header_format)

            worksheet = writer.sheets['User-Course']            
            default_column = ['COO','TM','CM','Course']
            for col_num, value in enumerate(default_column):
                worksheet.merge_range(0, col_num, 2, col_num, value, header_format)
            col=4
            for col_num, value in enumerate(first_row):
                if col_num==2:
                    worksheet.merge_range(0, col, 0, 4+col, value, header_format)
                    col=col+5                    
                else:
                    worksheet.merge_range(0, col, 0, 10+col, value, header_format)
                    col=col+11
            col=4
            for col_num, value in enumerate(second_row):
                if col_num==4:
                    worksheet.merge_range(1, col, 1, 4+col, value, header_format)
                    col=col+5
                elif value=='Target':
                    worksheet.merge_range(1, col, 1, 4+col, value, header_format)
                    col=col+5
                elif value=='Actual':
                    worksheet.merge_range(1, col, 1, 5+col, value, header_format)
                    col=col+6
            for col_num, value in enumerate(third_row):
                worksheet.write(2, 4+col_num, value, header_format)
            writer.save()
            return({'msg':'created excel', 'success':True, 'filename':path})
        except Exception as e:
            return({'msg':'Error creating excel -'+str(e), 'success':False, 'Error':str(e)})
    def DownloadRegionProductivityReport(customer_ids,contract_ids,month,region_ids):
        try:
            data=Database.DownloadRegionProductivityReport(customer_ids,contract_ids,month,region_ids)
            DownloadPath=config.neo_report_file_path+'report file/'
            report_name = config.RegionProductivityFileName+datetime.now().strftime('%Y_%m_%d_%H_%M_%S')+".xlsx"  
            r=re.compile(config.RegionProductivityFileName + ".*")
            lst=os.listdir(DownloadPath)
            newlist = list(filter(r.match, lst))
            for i in newlist:
                os.remove( DownloadPath + i)
            path = '{}{}'.format(DownloadPath,report_name)
            res={}
            res=Report.CreateExcelForRegionProductivity(data,path)
            if res['success']:
                return {"success":True,"msg":"Report Created.",'FileName':report_name,'FilePath':config.neo_report_file_path_web}
            else:
                return {"success":False,"msg":res['msg']}
        except Exception as e:
            return {"success":False,"msg":str(e)}

    def CreateExcelForRegionProductivity(data,path):
        try:
            writer = pd.ExcelWriter(path, engine='xlsxwriter')
            workbook  = writer.book

            header_format = workbook.add_format({
                'bold': True,
                #'text_wrap': True,
                'valign': 'center',
                'fg_color': '#D7E4BC',
                'border': 1})
            df = pd.DataFrame(data['sheet1'], columns=data['sheet1_columns'])
            df.to_excel(writer, index=None, header=None ,startrow=3 ,sheet_name='Region Wise Candidate Count') 

            df = pd.DataFrame(data['sheet2'], columns=data['sheet2_columns'])
            df.to_excel(writer, index=None, header=None ,startrow=3 ,sheet_name='Region Wise Batch Count') 

            df = pd.DataFrame(data['sheet3'], columns=data['sheet3_columns'])
            df.to_excel(writer, index=None, header=None ,startrow=3 ,sheet_name='Customer Wise Candidate Count') 

            worksheet = writer.sheets['Region Wise Candidate Count']
            default_column = ['Region','BU']
            first_row = ['Enrolment', 'Certification','Placement']
            second_row = ['Target', 'Actual','Target', 'Actual','Target', 'Actual']
            third_row = ['W-1', 'W-2','W-3','W-4','Total','W-1', 'W-2','W-3','W-4','Total','Conversion %',
                         'W-1', 'W-2','W-3','W-4','Total','W-1', 'W-2','W-3','W-4','Total','Conversion %','W-1', 'W-2','W-3','W-4','Total','W-1', 'W-2','W-3','W-4','Total','Conversion %',]
            
            for col_num, value in enumerate(default_column):
                worksheet.merge_range(0, col_num, 2, col_num, value, header_format)
            col=2
            for col_num, value in enumerate(first_row):
                if col_num==-1:
                    worksheet.merge_range(0, col, 0, 4+col, value, header_format)
                    col=col+5                    
                else:
                    worksheet.merge_range(0, col, 0, 10+col, value, header_format)
                    col=col+11
            col=2
            for col_num, value in enumerate(second_row):
                if col_num==-1:
                    worksheet.merge_range(1, col, 1, 4+col, value, header_format)
                    col=col+5
                elif value=='Target':
                    worksheet.merge_range(1, col, 1, 4+col, value, header_format)
                    col=col+5
                elif value=='Actual':
                    worksheet.merge_range(1, col, 1, 5+col, value, header_format)
                    col=col+6                
            for col_num, value in enumerate(third_row):
                worksheet.write(2, 2+col_num, value, header_format)

            worksheet = writer.sheets['Region Wise Batch Count']
            #default_column = ['COO','Sub Project']
            for col_num, value in enumerate(default_column):
                worksheet.merge_range(0, col_num, 2, col_num, value, header_format)
            col=2
            for col_num, value in enumerate(first_row):
                if col_num==-1:
                    worksheet.merge_range(0, col, 0, 4+col, value, header_format)
                    col=col+5                    
                else:
                    worksheet.merge_range(0, col, 0, 10+col, value, header_format)
                    col=col+11
            col=2
            for col_num, value in enumerate(second_row):
                if col_num==-1:
                    worksheet.merge_range(1, col, 1, 4+col, value, header_format)
                    col=col+5
                elif value=='Target':
                    worksheet.merge_range(1, col, 1, 4+col, value, header_format)
                    col=col+5
                elif value=='Actual':
                    worksheet.merge_range(1, col, 1, 5+col, value, header_format)
                    col=col+6                
            for col_num, value in enumerate(third_row):
                worksheet.write(2, 2+col_num, value, header_format)

            worksheet = writer.sheets['Customer Wise Candidate Count']            
            default_column = ['Region','BU','Customer']
            for col_num, value in enumerate(default_column):
                worksheet.merge_range(0, col_num, 2, col_num, value, header_format)
            col=3
            for col_num, value in enumerate(first_row):
                if col_num==-1:
                    worksheet.merge_range(0, col, 0, 4+col, value, header_format)
                    col=col+5                    
                else:
                    worksheet.merge_range(0, col, 0, 10+col, value, header_format)
                    col=col+11
            col=3
            for col_num, value in enumerate(second_row):
                if col_num==-1:
                    worksheet.merge_range(1, col, 1, 4+col, value, header_format)
                    col=col+5
                elif value=='Target':
                    worksheet.merge_range(1, col, 1, 4+col, value, header_format)
                    col=col+5
                elif value=='Actual':
                    worksheet.merge_range(1, col, 1, 5+col, value, header_format)
                    col=col+6
            for col_num, value in enumerate(third_row):
                worksheet.write(2, 3+col_num, value, header_format)
            writer.save()
            return({'msg':'created excel', 'success':True, 'filename':path})
        except Exception as e:
            return({'msg':'Error creating excel -'+str(e), 'success':False, 'Error':str(e)})
    
    def DownloadCustomerTargetReport(customer_ids,contract_ids,month,region_ids):
        try:
            data=Database.DownloadCustomerTargetReport(customer_ids,contract_ids,month,region_ids)
            DownloadPath=config.neo_report_file_path+'report file/'
            report_name = config.CustomerTargetFileName+datetime.now().strftime('%Y_%m_%d_%H_%M_%S')+".xlsx"  
            r=re.compile(config.CustomerTargetFileName + ".*")
            lst=os.listdir(DownloadPath)
            newlist = list(filter(r.match, lst))
            for i in newlist:
                os.remove( DownloadPath + i)
            path = '{}{}'.format(DownloadPath,report_name)
            res={}
            res=Report.CreateExcelForCustomerTarget(data,path)
            if res['success']:
                return {"success":True,"msg":"Report Created.",'FileName':report_name,'FilePath':config.neo_report_file_path_web}
            else:
                return {"success":False,"msg":res['msg']}
        except Exception as e:
            return {"success":False,"msg":str(e)}

    def CreateExcelForCustomerTarget(data,path):
        try:
            writer = pd.ExcelWriter(path, engine='xlsxwriter')
            workbook  = writer.book

            header_format = workbook.add_format({
                'bold': True,
                #'text_wrap': True,
                'valign': 'center',
                'fg_color': '#D7E4BC',
                'border': 1})
            df = pd.DataFrame(data['sheet1'], columns=data['sheet1_columns'])
            df.to_excel(writer, index=None, header=None ,startrow=2 ,sheet_name='Summary') 

            df = pd.DataFrame(data['sheet2'], columns=data['sheet2_columns'])
            df.to_excel(writer, index=None, header=None ,startrow=2 ,sheet_name='LE NEO vs Actual') 

            df = pd.DataFrame(data['sheet3'], columns=data['sheet3_columns'])
            df.to_excel(writer, index=None, header=None ,startrow=2 ,sheet_name='Enrolment and Assessment Batch') 

            worksheet = writer.sheets['Summary']
            default_column = ['Region','BU']
            first_row = ['Enrolment', 'Certification','Placement','New Batch Start(Planned Vs Actual)', 'Batch Certification(Planned Vs Actual)']
            second_row = ['Target', 'Actual','% Achieved',
                          'Target', 'Actual','% Achieved',
                          'Target', 'Actual','% Achieved',
                          'Target', 'Actual','% Achieved',
                          'Target', 'Actual','% Achieved',
                          ]
            
            for col_num, value in enumerate(default_column):
                worksheet.merge_range(0, col_num, 1, col_num, value, header_format)
            col=2
            for col_num, value in enumerate(first_row):
                worksheet.merge_range(0, col, 0, 2+col, value, header_format)
                col=col+3
            for col_num, value in enumerate(second_row):
                worksheet.write(1, 2+col_num, value, header_format)

            worksheet = writer.sheets['LE NEO vs Actual']            
            default_column = ['Region','BU','Customer','PMT']
            for col_num, value in enumerate(default_column):
                worksheet.merge_range(0, col_num, 1, col_num, value, header_format)
            col=4
            for col_num, value in enumerate(first_row):
                worksheet.merge_range(0, col, 0, 2+col, value, header_format)
                col=col+3
            
            for col_num, value in enumerate(second_row):
                worksheet.write(1, 4+col_num, value, header_format)

            worksheet = writer.sheets['Enrolment and Assessment Batch']            
            default_column = ['Region','BU','Customer']
            first_row = ['New Batch Start(Planned Vs Actual)', 'Batch Certification(Planned Vs Actual)']
            second_row = ['MTD Batch Plan', 'Yes','No','Not Started',
                          'MTD Batch Plan', 'Yes','No','Not Started'
                          ]
            header_format = workbook.add_format({
                'bold': True,
                'text_wrap': True,
                'valign': 'center',
                'fg_color': '#D7E4BC',
                'border': 1})
            for col_num, value in enumerate(default_column):
                worksheet.merge_range(0, col_num, 1, col_num, value, header_format)
            col=3

            for col_num, value in enumerate(first_row):
                worksheet.merge_range(0, col, 0, 3+col, value, header_format)
                col=col+4
            
            for col_num, value in enumerate(second_row):
                worksheet.write(1, 3+col_num, value, header_format)

            writer.save()
            return({'msg':'created excel', 'success':True, 'filename':path})
        except Exception as e:
            return({'msg':'Error creating excel -'+str(e), 'success':False, 'Error':str(e)})
    
    