from flask_restful import Resource
from flask import request
from Models import Master           
from Database import Database
import xlsxwriter
###########################################################3
class center_list(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            center_id = request.form['center_id']
            center_type_ids = request.form['center_type_ids']
            bu_ids = request.form['bu_ids']
            status = request.form['status'] 
            start_index = request.form['start']
            page_length = request.form['length']
            search_value = request.form['search[value]']
            order_by_column_position = request.form['order[0][column]']
            order_by_column_direction = request.form['order[0][dir]']
            draw=request.form['draw']
            regions=request.form['regions']
            clusters=request.form['clusters']
            courses=request.form['courses']
            
            Center_lt = Master.center_list(center_id,center_type_ids,bu_ids,status,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw,regions,clusters,courses)
            return Center_lt


class all_districts_based_on_state(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            state_id=request.form['state_id']
            return Master.AllDistrictsOnState(state_id)


class all_states_based_on_country(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            country_id=request.form['country_id']
            return Master.AllStatesOnCountry(country_id)



class all_countries(Resource):
    @staticmethod
    def get():
        if request.method == 'GET':
            return Master.AllCountry()


class all_center_categories(Resource):
    @staticmethod
    def get():
        if request.method == 'GET':
            return Master.AllCenterCategory()


class all_center_type(Resource):
    @staticmethod
    def get():
        if request.method == 'GET':
            return Master.AllCenterTypes()

class DownloadCenterList:
    def download_centers_list(center_type_ids,bu_ids,status,path):
        response= Database.download_centers_list(center_type_ids,bu_ids,status)
        FileName=DownloadCenterList.CreateExcelDownloadCenterList(response,path)

    def CreateExcelDownloadCenterList(data,path):
        filename=''
        col=['Center_Name', 'Center_Type_Name','Bu_Name','Is_Active', 'Region_Name','Cluster_Name','Country_Name','State_Name','District_Name','Location']        
        
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
            worksheet = workbook.add_worksheet('Centers')
            for i in range(len(col)):
                worksheet.write(0,i ,col[i], header_format)   
            for j in range(len(data)) : 
                for k in range(len(col)):
                    worksheet.write(j+1,k ,data.iloc[j,k],write_format)
                            
            workbook.close()
        except Exception as e:
            print(str(e))
            
        return path

