from flask_restful import Resource
from flask import request
from Models import Content

###########################################################3
class course_list(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            user_id=request.form['user_id']
            user_role_id=request.form['user_role_id']
            course_id = request.form['course_id'] 
            sectors = request.form['sectors']
            qps = request.form['qps']
            
            start_index = request.form['start']
            page_length = request.form['length']
            search_value = request.form['search[value]']
            order_by_column_position = request.form['order[0][column]']
            order_by_column_direction = request.form['order[0][dir]']
            draw=request.form['draw']

            status = request.form['status']
            return Content.course_list(user_id,user_role_id,course_id,sectors,qps,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw, status)

class AllCenterList(Resource,):
    @staticmethod
    def get():
        if request.method == 'GET':
            cluster_id = request.args['cluster_id']
            return Content.AllCenter(cluster_id)
        
class AllClusterList(Resource):
    @staticmethod
    def get():
        if request.method == 'GET':
            return Content.AllCluster()
class AllRegionList(Resource):
    @staticmethod
    def get():
        if request.method == 'GET':
            return Content.AllRegion()
            
class AllProjectList(Resource):
    @staticmethod
    def get():
        if request.method == 'GET':
            return Content.AllProject()

class AllPracticeList(Resource):
    @staticmethod
    def get():
        if request.method == 'GET':
            return Content.AllPractice()


class AllProjectsBasedOnPractice(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            practice_id = request.form['practice_id']
            project_id = request.form['project_id']
            return Content.AllProjectOnPractice(project_id,practice_id) 


