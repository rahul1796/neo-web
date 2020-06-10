from Database import Database,config
from flask_restful import Resource
from flask import request
from datetime import datetime
import xlsxwriter,re,os,zipfile,zlib 


class Assessments:
    def GetBatchAssessments(BatchId,Stage):
        return Database.GetBatchAssessments(BatchId,Stage)
    def GetBatchAssessmentsHistory(AssessmentId):
        return Database.GetBatchAssessmentsHistory(AssessmentId)
    def GetAssessmentTypes():
        return Database.GetAssessmentTypes()
    def GetAssessmentAgency():
        return Database.GetAssessmentAgency()
    def ScheduleAssessment(batch_id,user_id,requested_date,scheduled_date,assessment_date,assessment_type_id,assessment_agency_id,assessment_id,partner_id,current_stage_id,present_candidate,absent_candidate,assessor_name,assessor_email,assessor_mobile,reassessment_flag):
        return Database.ScheduleAssessment(batch_id,user_id,requested_date,scheduled_date,assessment_date,assessment_type_id,assessment_agency_id,assessment_id,partner_id,current_stage_id,present_candidate,absent_candidate,assessor_name,assessor_email,assessor_mobile,reassessment_flag)

class DownloadAssessmentResultUploadTemplate(Resource):
    DownloadPath=config.DownloadcandidateResultPathLocal
    
    @staticmethod
    def get():
        if request.method=='GET':
            try:
                
                AssessmentId=request.args.get('AssessmentId',0,type=int)
                BatchId=request.args.get('BatchId',0,type=int)
                Batch_Code=request.args.get('Batch_Code','',type=str)
                print(Batch_Code)
                report_name = config.AssessmentCandidateResultUploadTemplate+'_'+Batch_Code+'_'+datetime.now().strftime('%Y_%m_%d_%H_%M_%S')+".xlsx"   
                r=re.compile(config.DumpFileName + ".*")
                lst=os.listdir(DownloadAssessmentResultUploadTemplate.DownloadPath)
                newlist = list(filter(r.match, lst))
                for i in newlist:
                    os.remove( DownloadAssessmentResultUploadTemplate.DownloadPath + i)
                path = '{}{}'.format(DownloadAssessmentResultUploadTemplate.DownloadPath,report_name)
                response=Database.GetAssessmentCandidateResultUploadTemplate(AssessmentId,BatchId)
                res=DownloadAssessmentResult.CreateExcelForDump(response,path,'Template')
                ImagePath=config.DownloadcandidateResultPathWeb
                return {'FileName':report_name,'FilePath':ImagePath}
            except Exception as e:
                print(str(e))
                return {"exception":str(e),"File":"HI"}

class DownloadAssessmentResult(Resource):
    DownloadPath=config.DownloadcandidateResultPathLocal
    #print(DownloadPath)
    
    @staticmethod
    def get():
        if request.method=='GET':
            try:
                AssessmentId=request.args.get('AssessmentId',0,type=int)
                Batch_Code=request.args.get('Batch_Code','',type=str)
                report_name = config.AssessmentCandidateResult+'_'+Batch_Code+'_'+datetime.now().strftime('%Y_%m_%d_%H_%M_%S')+".xlsx"   

                #print(AssessmentId)
                r=re.compile(config.AssessmentCandidateResult + ".*")
                lst=os.listdir(DownloadAssessmentResult.DownloadPath)
                #print(DownloadAssessmentResult.DownloadPath)
                newlist = list(filter(r.match, lst))
                for i in newlist:
                    os.remove( DownloadAssessmentResult.DownloadPath + i)
                path = '{}{}'.format(DownloadAssessmentResult.DownloadPath,report_name)
                response=Database.GetAssessmentCandidateResults(AssessmentId)
                res=DownloadAssessmentResult.CreateExcelForDump(response,path,'Result')
                ImagePath=config.DownloadcandidateResultPathWeb
                return {'FileName':report_name,'FilePath':ImagePath}
            except Exception as e:
                print(str(e))
                return {"exception":str(e),"File":"HI"}

    def CreateExcelForDump(Response,file_path,sheet_name):
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