from Database import Database
from Database import config
from datetime import datetime
import pandas as pd
import xlsxwriter,re,os

class Report:
    def AllRegionsBasedOnUser(UserId,UserRoleId,UserRegionId):
        return Database.AllRegionsBasedOnUser(UserId,UserRoleId,UserRegionId)
    def GetAllCentersBasedOnRegion_User(UserId,UserRoleId,RegionId):
        return Database.GetAllCentersBasedOnRegion_User(UserId,UserRoleId,RegionId)
    def GetAllCoursesBasedOnCenter_User(UserId,UserRoleId,CenterId):
        return Database.GetAllCoursesBasedOnCenter_User(UserId,UserRoleId,CenterId)
    def GetAllTrainersBasedOnCenter_User(UserId,UserRoleId,CenterId):
        return Database.GetAllTrainersBasedOnCenter_User(UserId,UserRoleId,CenterId)
    def GetAllMobilizersBasedOnCenter_User(UserId,UserRoleId,CenterId):
        return Database.GetAllMobilizersBasedOnCenter_User(UserId,UserRoleId,CenterId)
    def TrainerDeploymentBatches(region_id,center_id,course_ids,trainer_ids,from_date,to_date,batch_stage_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        return Database.TrainerDeploymentBatches(region_id,center_id,course_ids,trainer_ids,from_date,to_date,batch_stage_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)
    def ReportAttendanceBatches(region_id,center_id,course_ids,trainer_ids,from_date,to_date,batch_stage_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw):
        return Database.ReportAttendanceBatches(region_id,center_id,course_ids,trainer_ids,from_date,to_date,batch_stage_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)
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
                columns=[ 'Practice','Customer','Contract Code','Contract Name','Project Code','Project Name','Sub Project Code','Sub Project Name','Center','Product','BU','Region','Batch Code','Course Code','Course Name','Status','Actual Start Date','Actual End Date','Unit Rate','E Ratio','C Ratio','P Ratio','Enrolled','Dropped','Certified','Certificates Distribution','Placed','Placement Count(RR)','Placement Is Percent Of','Ojt Completed','Enrolled(Selected Duration)','Dropped(Selected Duration)','Certified(Selected Duration)','Certificates Distribution(Selected Duration)','Placed(Selected Duration)','Placement Count RR(Selected Duration)','Ojt Completed(Selected Duration)','Excess No','Excess Revenue','Overall Revenue','Revenue(Selected Duration)']
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