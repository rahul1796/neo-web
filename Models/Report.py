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
            df.to_excel(writer, index=None, header=None ,startrow=3 ,sheet_name='Region-Contract Nos & Revenue')

            df = pd.DataFrame(data['sheet2'], columns=data['sheet2_columns'])
            df.to_excel(writer, index=None, header=None ,startrow=3 ,sheet_name='Region Wise Batch Count') 

            df = pd.DataFrame(data['sheet3'], columns=data['sheet3_columns'])
            df.to_excel(writer, index=None, header=None ,startrow=3 ,sheet_name='Customer Wise Candidate Count') 

            default_column = ['Region','BU']
            first_row = ['Enrolment', 'Certification','Placement']
            second_row = ['Target', 'Actual','Target', 'Actual','Target', 'Actual']
            third_row = ['W-1', 'W-2','W-3','W-4','Total','W-1', 'W-2','W-3','W-4','Total','Conversion %',
                         'W-1', 'W-2','W-3','W-4','Total','W-1', 'W-2','W-3','W-4','Total','Conversion %',
                         'W-1', 'W-2','W-3','W-4','Total','W-1', 'W-2','W-3','W-4','Total','Conversion %']
            
            default_column1 = ['Region','BU','Contract']
            first_row1 = ['Enrolment', 'Certification','Placement','Revenue (In Rs)']
            second_row1 = ['Target', 'Actual','Target', 'Actual','Target', 'Actual','Target', 'Actual']
            third_row1 = ['W-1', 'W-2','W-3','W-4','Total','W-1', 'W-2','W-3','W-4','Total','Conversion %',
                         'W-1', 'W-2','W-3','W-4','Total','W-1', 'W-2','W-3','W-4','Total','Conversion %',
                         'W-1', 'W-2','W-3','W-4','Total','W-1', 'W-2','W-3','W-4','Total','Conversion %',
                         'W-1', 'W-2','W-3','W-4','Total','W-1', 'W-2','W-3','W-4','Total','Conversion %']
            
            worksheet = writer.sheets['Region-Contract Nos & Revenue']
            for col_num, value in enumerate(default_column1):
                worksheet.merge_range(0, col_num, 2, col_num, value, header_format)
            col=3
            for col_num, value in enumerate(first_row1):
                if col_num==-1:
                    worksheet.merge_range(0, col, 0, 4+col, value, header_format)
                    col=col+5                    
                else:
                    worksheet.merge_range(0, col, 0, 10+col, value, header_format)
                    col=col+11
            col=3
            for col_num, value in enumerate(second_row1):
                if col_num==-1:
                    worksheet.merge_range(1, col, 1, 4+col, value, header_format)
                    col=col+5
                elif value=='Target':
                    worksheet.merge_range(1, col, 1, 4+col, value, header_format)
                    col=col+5
                elif value=='Actual':
                    worksheet.merge_range(1, col, 1, 5+col, value, header_format)
                    col=col+6                
            
            for col_num, value in enumerate(third_row1):
                worksheet.write(2, 3+col_num, value, header_format)

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
            df.to_excel(writer, index=None, header=None ,startrow=2 ,sheet_name='Region-BU Wise Summary') 

            df = pd.DataFrame(data['sheet2'], columns=data['sheet2_columns'])
            df.to_excel(writer, index=None, header=None ,startrow=2 ,sheet_name='Customer-BU Wise Nos') 

            df = pd.DataFrame(data['sheet3'], columns=data['sheet3_columns'])
            df.to_excel(writer, index=None, header=None ,startrow=2 ,sheet_name='Batch Plan Summary') 

            worksheet = writer.sheets['Region-BU Wise Summary']
            default_column = ['Region','BU']
            first_row = ['Enrolment', 'Certification','Placement','  New Batch Start(Planned Vs Actual)', '  Batch Certification(Planned Vs Actual)']
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

            worksheet = writer.sheets['Customer-BU Wise Nos']            
            default_column = ['Region','BU','Customer ','PMT']
            for col_num, value in enumerate(default_column):
                worksheet.merge_range(0, col_num, 1, col_num, value, header_format)
            col=4
            for col_num, value in enumerate(first_row):
                worksheet.merge_range(0, col, 0, 2+col, value, header_format)
                col=col+3
            
            for col_num, value in enumerate(second_row):
                worksheet.write(1, 4+col_num, value, header_format)

            worksheet = writer.sheets['Batch Plan Summary']            
            default_column = ['Region','BU','Customer ']
            first_row = ['  New Batch Start(Planned Vs Actual)  ', '  Batch Certification(Planned Vs Actual)  ']
            second_row = ['MTD Batch Plan', 'Actual Batch','Cancelled Planned Batch','Yet To Start',
                          'MTD Batch Plan', 'Actual Batch','Cancelled Planned Batch','Yet To Start'
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
    
    def DownloadCandidateData(candidate_id, user_id, user_role_id, project_types, customer, project, sub_project, batch, region, center, created_by, Contracts, candidate_stage, from_date, to_date):
        try:
            print("hi")
            data=Database.DownloadCandidateData(candidate_id, user_id, user_role_id, project_types, customer, project, sub_project, batch, region, center, created_by, Contracts, candidate_stage, from_date, to_date)
            DownloadPath=config.neo_report_file_path+'report file/'
            report_name = config.CandidateDataFileName+datetime.now().strftime('%Y_%m_%d_%H_%M_%S')+".xlsx"  
            r=re.compile(config.CandidateDataFileName + ".*")
            lst=os.listdir(DownloadPath)
            newlist = list(filter(r.match, lst))
            for i in newlist:
                os.remove( DownloadPath + i)
            path = '{}{}'.format(DownloadPath,report_name)
            res={}
            res=Report.CreateExcelForCandidateData(data,path,project_types,candidate_stage)
            if res['success']:
                return {"success":True,"msg":"File Created.",'FileName':report_name,'FilePath':config.neo_report_file_path_web}
            else:
                return {"success":False,"msg":res['msg']}
        except Exception as e:
            return {"success":False,"msg":str(e)}

    def CreateExcelForCandidateData(data,path,project_types,candidate_stage):
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
            
            
            df_mob=df[['Candidate_Id', 'Salutation', 'First_Name', 'Middle_Name', 'Last_Name', 'Date_Of_Birth', 'Age', 'Primary_Contact_No', 'Secondary_Contact_No', 'Email_Id', 'Gender', 'Marital_Status', 'Caste', 'Disability_Status', 'Religion', 'Mother_Tongue', 'Occupation', 'Average_Annual_Income', 'Interested_Course', 'Product','Source_Of_Information','Mobilized_On','Mobilized_By']]
            df_mob.drop_duplicates(keep='first',inplace=True) 
            df_mob.to_excel(writer, index=None, header=None ,startrow=1 ,sheet_name='Mobilization') 
            worksheet1 = writer.sheets['Mobilization']
            default_column = ['Candidate_Id', 'Salutation', 'First_Name', 'Middle_Name', 'Last_Name', 'Date_Of_Birth', 'Age', 'Primary_Contact_No', 'Secondary_Contact_No', 'Email_Id', 'Gender', 'Marital_Status', 'Caste', 'Disability_Status', 'Religion', 'Mother_Tongue', 'Occupation', 'Average_Annual_Income', 'Interested_Course', 'Product','Source_Of_Information','Mobilized_On','Mobilized_By']
            for i in range(len(default_column)):
                worksheet1.write(0,i ,default_column[i], header_format)

            df_she=df[['Candidate_Id',  'First_Name', 'Middle_Name', 'Last_Name','Primary_Contact_No','Email_Id','Result','Age18To40','Eight_Pass','Past_Experience','Full_Time','Travel','Bank_Acount',
                       #'Date of birth (age between 18 to 40)' , 'Are you 8th Pass?','Do you have any work experience in the past?','Will you able to work full time or at least 6 hours a day?','Are you willing to travel from one place to another within panchayat?','Do you have a bank account?',
                       
                       'Are You Able To Read And Write Local Language?', 'Do You Have A Smart Phone?', 'Are You Willing To Buy A Smartphone?', 'Do You Own Two Wheeler?', 'Do You Know How To Operate A Smartphone?', 'Are You/ Have You Been An Entrepreneur Before?', 'Do You Have Permission From Your Family To Work Outside?', 'Are You A Member Of Shg?', 
                       'Are You Willing To Serve The Community At This Time Of Covid-19 Pandemic As Sanitization & Hygiene Entrepreneurs (She)?', 'Are You Willing To Undergo Online Trainings And Mentorship Program For 6 Month?', 'Are You Willing To Share Details Of Customer, Revenue, Expenses Frequently With Ln?', 
                       'Are You Willing To Work And Sign The Work Contract With Ln?', 'Are You Willing To Buy Tools And Consumables Required To Run Your Business?', 'Are You Willing To Adopt Digital Transactions In Your Business?', 'Are You Willing To Register Your Business In Social Platforms Like Whatsapp, Face Book, Geo Listing, Just Dial Etc.?', 
                       'Have You Availed Any Loan In The Past?', 'Do You Have Any Active Loan?', 'Are You Willing To Take Up A Loan To Purchase Tools And Consumables?', 'Are You Covered Under Any Health Insurance?', 'Are You Allergic To Any Chemicals And Dust?', 'Will You Able To Wear Mandatory Ppes During The Work?', 
                       'Are You Willing To Follow  Environment, Health And Safety Norms In Your Business?', 'Have You Ever Been Subjected To Any Legal Enquiry For Non Ethical Work/Business?', 'Address As Per Aadhar Card (Incl Pin Code)', 'Number Of Members Earning In The Family', 'Rented Or Own House?', 'Size Of The House', 'Ration Card (Apl Or Bpl)', 'Tv', 'Refrigerator', 'Washing Machine', 'Ac /Cooler', 'Car', 'Kids Education', 'Medical Insurance', 'Life Insurance', 'Others', 'Educational Qualification', 'Age Proof', 'Signed Mou', 'Mou Signed Date', 'Kit Given Date', 'Head Of The Household', 'Farm Land', 'If Yes, Acres Of Land']]
            df_she.drop_duplicates(keep='first',inplace=True) 
            df_she.to_excel(writer, index=None, header=None ,startrow=1 ,sheet_name='SHE') 
            worksheet3 = writer.sheets['SHE']
            default_column_she = ['Candidate_Id',  'First_Name', 'Middle_Name', 'Last_Name','Primary_Contact_No','Email_Id','MCL Result',
                       'Date of birth (age between 18 to 40)' , 'Are you 8th Pass?','Do you have any work experience in the past?','Will you able to work full time or at least 6 hours a day?','Are you willing to travel from one place to another within panchayat?','Do you have a bank account?',
                       'Are You Able To Read And Write Local Language?', 'Do You Have A Smart Phone?', 'Are You Willing To Buy A Smartphone?', 'Do You Own Two Wheeler?', 'Do You Know How To Operate A Smartphone?', 'Are You/ Have You Been An Entrepreneur Before?', 'Do You Have Permission From Your Family To Work Outside?', 'Are You A Member Of Shg?', 
                       'Are You Willing To Serve The Community At This Time Of Covid-19 Pandemic As Sanitization & Hygiene Entrepreneurs (She)?', 'Are You Willing To Undergo Online Trainings And Mentorship Program For 6 Month?', 'Are You Willing To Share Details Of Customer, Revenue, Expenses Frequently With Ln?', 
                       'Are You Willing To Work And Sign The Work Contract With Ln?', 'Are You Willing To Buy Tools And Consumables Required To Run Your Business?', 'Are You Willing To Adopt Digital Transactions In Your Business?', 'Are You Willing To Register Your Business In Social Platforms Like Whatsapp, Face Book, Geo Listing, Just Dial Etc.?', 
                       'Have You Availed Any Loan In The Past?', 'Do You Have Any Active Loan?', 'Are You Willing To Take Up A Loan To Purchase Tools And Consumables?', 'Are You Covered Under Any Health Insurance?', 'Are You Allergic To Any Chemicals And Dust?', 'Will You Able To Wear Mandatory Ppes During The Work?', 
                       'Are You Willing To Follow  Environment, Health And Safety Norms In Your Business?', 'Have You Ever Been Subjected To Any Legal Enquiry For Non Ethical Work/Business?', 'Address As Per Aadhar Card (Incl Pin Code)', 'Number Of Members Earning In The Family', 'Rented Or Own House?', 'Size Of The House', 'Ration Card (Apl Or Bpl)', 'Tv', 'Refrigerator', 'Washing Machine', 'Ac /Cooler', 'Car', 'Kids Education', 'Medical Insurance', 'Life Insurance', 'Others', 'Educational Qualification', 'Age Proof', 'Signed Mou', 'Mou Signed Date', 'Kit Given Date', 'Head Of The Household', 'Farm Land', 'If Yes, Acres Of Land']
            for i in range(len(default_column_she)):
                worksheet3.write(0,i ,default_column_she[i], header_format)

            df_reg=df[['Candidate_Id',  'First_Name', 'Middle_Name', 'Last_Name','Primary_Contact_No','Email_Id','Present_Address_Line1','Present_Address_Line2', 'Present_Village', 'Present_Panchayat', 'Present_Taluk_Block','Present_District', 'Present_State', 'Present_Pincode', 'Present_Country', 'Permanaet_Address_Line1','Permanent_Address_Line2', 'Permanent_Village', 'Permanent_Panchayat', 'Permanent_Taluk_Block','Permanent_District', 'Permanent_State', 'Permanent_Pincode', 'Permanent_Country','Aadhar_No', 'Identifier_Type', 'Identity_Number','Employment_Type', 'Preferred_Job_Role', 'Relevant_Years_Of_Experience', 'Current_Last_Ctc', 'Preferred_Location', 'Willing_To_Travel', 'Willing_To_Work_In_Shifts', 'Bocw_Registration_Id', 'Expected_Ctc','Project_Type','Registered_On','Registered_By']]
            df_reg.drop_duplicates(keep='first',inplace=True) 
            df_reg.to_excel(writer, index=None, header=None ,startrow=1 ,sheet_name='Registration') 
            worksheet2 = writer.sheets['Registration']
            default_column_reg = ['Candidate_Id',  'First_Name', 'Middle_Name', 'Last_Name','Primary_Contact_No','Email_Id','Present_Address_Line1','Present_Address_Line2', 'Present_Village', 'Present_Panchayat', 'Present_Taluk_Block','Present_District', 'Present_State', 'Present_Pincode', 'Present_Country', 'Permanent_Address_Line1','Permanent_Address_Line2', 'Permanent_Village', 'Permanent_Panchayat', 'Permanent_Taluk_Block','Permanent_District', 'Permanent_State', 'Permanent_Pincode', 'Permanent_Country','Aadhar_No', 'Identifier_Type', 'Identity_Number','Employment_Type', 'Preferred_Job_Role', 'Relevant_Years_Of_Experience', 'Current_Last_Ctc', 'Preferred_Location', 'Willing_To_Travel', 'Willing_To_Work_In_Shifts', 'Bocw_Registration_Id', 'Expected_Ctc','Project_Type','Registered_On','Registered_By']
            for i in range(len(default_column_reg)):
                worksheet2.write(0,i ,default_column_reg[i], header_format)
            
            

            df_enr=df[['Candidate_Id','Batch_Code','Intervention_Value',  'First_Name', 'Middle_Name', 'Last_Name','Primary_Contact_No','Email_Id','Highest_Qualification', 'Stream_Specialization', 'Computer_Knowledge', 'Technical_Knowledge','Name_Of_Institute', 'University', 'Year_Of_Pass', 'Percentage','Family Salutation', 'Name', 'Family_Date_Of_Birth', 'Family_Age', 'Family_Primary_Contact', 'Family_Email_Address', 'Family Gender', 'Relationship', 'Education_Qualification', 'Members_Occupation','Bank_Name', 'Account_Number','Branch_Name', 'Branch_Code', 'Account_Type','Project_Type','Enrolled_On','Enrolled_By']]
            #df_enr.drop_duplicates(keep='first',inplace=True) 
            df_enr.to_excel(writer, index=None, header=None ,startrow=1 ,sheet_name='Enrolment') 
            worksheet4 = writer.sheets['Enrolment']
            default_column_enr = ['Candidate_Id','Batch_Code','Enrollment Id', 'First_Name', 'Middle_Name', 'Last_Name','Primary_Contact_No','Email_Id','Highest_Qualification', 'Stream_Specialization', 'Computer_Knowledge', 'Technical_Knowledge','Name_Of_Institute', 'University', 'Year_Of_Pass', 'Percentage','Family Salutation', 'Name', 'Family_Date_Of_Birth', 'Family_Age', 'Family_Primary_Contact', 'Family_Email_Address', 'Family Gender', 'Relationship', 'Education_Qualification', 'Members_Occupation','Bank_Name', 'Account_Number','Branch_Name', 'Branch_Code', 'Account_Type','Project_Type','Enrolled_On','Enrolled_By']
            for i in range(len(default_column_enr)):
                worksheet4.write(0,i ,default_column_enr[i], header_format)
                      
            if candidate_stage == '2':
                worksheet4.hide()
                
            if candidate_stage == '1':
                worksheet2.hide()
                worksheet3.hide()
                worksheet4.hide()
             
            if project_types == '1':
                worksheet3.hide()
            
            writer.save()

            return({'msg':'created excel', 'success':True, 'filename':path})
        except Exception as e:
            return({'msg':'Error creating excel -'+str(e), 'success':False, 'Error':str(e)})
    
    def project_list_report(user_id,user_role_id,user_region_id,entity,customer,p_group,block,practice,bu,product,status,report_name):
        try:
            name_withpath = config.neo_report_file_path + 'report file/'+ report_name
            
            writer = pd.ExcelWriter(name_withpath, engine='xlsxwriter')
            workbook  = writer.book

            header_format = workbook.add_format({
                'bold': True,
                'text_wrap': True,
                'valign': 'center',
                'fg_color': '#D7E4BC',
                'border': 1})

            resp = Database.project_list(user_id,user_role_id,user_region_id,0,10000,'','','asc','',entity,customer,p_group,block,practice,bu,product,status)['data']
            df = pd.DataFrame(resp)
            columns = ['Entity_Name', 'Customer_Name', 'Contract_Name','Project_Code', 'Project_Name','Center_Count', 'Course_Count', 'Project_Group_Name', 'Project_Type_Name', 'Block_Name', 'Practice_Name', 'Bu_Name', 'Product_Name', 'Project_Manager', 'Course_Name','Start_Date', 'End_Date', 'Status']
            df=df[columns]

            header = ['Entity Name', 'Customer Name', 'Contract Name', 'Project Code', 'Project Name','Center Count', 'Course Count', 'Group', 'Type', 'Block', 'Practice', 'Bu', 'Product', 'Project Manager', 'Course Name', 'Start Date', 'End Date', 'Status']
            df.to_excel(writer, index=None, header=None, startrow=1 ,sheet_name='Project_list')
            worksheet = writer.sheets['Project_list']
            for col_num, value in enumerate(header):
                worksheet.write(0, col_num, value, header_format)
                
            writer.save()
            return({'Description':'created excel', 'Status':True, 'filename':report_name})
            
        except Exception as e:
            return({'Description':'Error creating excel', 'Status':False, 'Error':str(e)})
        
    def sub_project_list_report(user_id,user_role_id,user_region_id,entity,customer,p_group,block,practice,bu,product,status,project,report_name):
        try:
            name_withpath = config.neo_report_file_path + 'report file/'+ report_name
            
            writer = pd.ExcelWriter(name_withpath, engine='xlsxwriter')
            workbook  = writer.book
            header_format = workbook.add_format({
                'bold': True,
                'text_wrap': True,
                'valign': 'center',
                'fg_color': '#D7E4BC',
                'border': 1})

            resp = Database.sub_project_list(user_id,user_role_id,user_region_id,0,10000,'','','asc','',entity,customer,p_group,block,practice,bu,product,status,project)['data']
            df = pd.DataFrame(resp)

            columns = ['Entity_Name', 'Customer_Name', 'Project_Code', 'Project_Name', 'Sub_Project_Code', 'Sub_Project_Name', 'Region_Name', 'State_Name', 'Center_Count', 'Center_Name', 'Course_Count', 'Course_Name', 'Users_Count', 'Planned_Batches', 'Project_Group_Name', 'Project_Type_Name', 'Block_Name', 'Practice_Name', 'Bu_Name', 'Product_Name', 'Project_Manager', 'Start_Date', 'End_Date', 'Status']
            df=df[columns]

            header = ['Entity Name', 'Customer Name', 'Project Code', 'Project Name', 'Sub Project Code', 'Sub Project Name', 'Region Name', 'State Name', 'Center Count', 'Center Name', 'Course Count', 'Course Name', 'Users Count', 'Planned Batches', 'Group', 'Type', 'Block', 'Practice', 'Bu', 'Product', 'Project Manager', 'Start Date', 'End Date', 'Status']
            df.to_excel(writer, index=None, header=None, startrow=1 ,sheet_name='Sub_Project_list')
            worksheet = writer.sheets['Sub_Project_list']
            for col_num, value in enumerate(header):
                worksheet.write(0, col_num, value, header_format)
                
            writer.save()
            return({'Description':'created excel', 'Status':True, 'filename':report_name})
            
        except Exception as e:
            return({'Description':'Error creating excel', 'Status':False, 'Error':str(e)})
        