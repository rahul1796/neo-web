from Database import Database
from Database import config
from flask_restful import Resource
from flask import request
from datetime import datetime
import xlsxwriter,re,os,zipfile,zlib 

class DownloadDump(Resource):
    DownloadPath=config.DownloadPathLocal
    report_name = config.DumpFileName+datetime.now().strftime('%Y_%m_%d_%H_%M_%S')+".zip"    

    @staticmethod
    def get():
        if request.method=='GET':
            try:
                r=re.compile(config.DumpFileName + ".*")
                lst=os.listdir(DownloadDump.DownloadPath)
                newlist = list(filter(r.match, lst))
                for i in newlist:
                    os.remove( DownloadDump.DownloadPath + i)
                path = '{}{}.xlsx'.format(DownloadDump.DownloadPath,DownloadDump.report_name)
                res=DownloadDump.GetAllFiles()
                ImagePath=config.DownloadPathWeb
                return {'FileName':DownloadDump.report_name,'FilePath':ImagePath}
            except Exception as e:
                print(str(e))
                return {"exception":str(e),"File":"HI"}
    
    def GetAllFiles():
        try:
            DumpFiles=config.DumpFilesList
            file_names=[]
            dump_file_path=DownloadDump.DownloadPath+DownloadDump.report_name
            
            for key in DumpFiles.keys():  
                r=re.compile(key + ".*")
                lst=os.listdir(DownloadDump.DownloadPath)
                newlist = list(filter(r.match, lst))
                for i in newlist:
                    os.remove( DownloadDump.DownloadPath + i)              
                file_path='{}{}.xlsx'.format(DownloadDump.DownloadPath,key+datetime.now().strftime('_%Y_%m_%d_%H_%M_%S'))
                #file_names.append(os.path.join(file_path))
                file_names.append(key+datetime.now().strftime('_%Y_%m_%d_%H_%M_%S')+'.xlsx')
                Response=Database.GetDataForExcel(DumpFiles[key])
                flag=DownloadDump.CreateExcelForDump(Response,file_path,key)

            rootdir = os.path.basename(DownloadDump.DownloadPath)
            with zipfile.ZipFile(dump_file_path, 'w',zipfile.ZIP_DEFLATED) as zipObj:
                for folderName, subfolders, filenames in os.walk(DownloadDump.DownloadPath):
                    for filename in filenames:
                        if filename in file_names:
                            filepath   = os.path.join(folderName, filename)
                            parentpath = os.path.relpath(filepath, DownloadDump.DownloadPath)
                            arcname    = os.path.join(rootdir, parentpath)
                            zipObj.write(filepath,arcname)
                
        except Exception as e:
            return {"exception":str(e),"File":'NA'}
    
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
                        worksheet.write(j+1,k ,'NA',write_format)
                    else:
                        worksheet.write(j+1,k ,Response['data'].iloc[j,k],write_format)
                                                    
            workbook.close()
            return True
        except Exception as e:
            print(str(e))
            return False
