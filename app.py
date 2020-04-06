from flask import Flask,render_template,request,redirect,url_for,session,g,jsonify,send_file
from flask_restful import Resource
from flask_restful import Api
#from flask_session import Session
from Models import Content,Assessments,DownloadAssessmentResult
from Models import Master
from Models import UsersM
from Models import Batch
from Models import Candidate
from Models import Report
from Database import config
from Database import Database
import sent_mail
import course_api
import center_category_api
import center_api
import final_report
import MCL_updated_report
import os
from flask import jsonify
import json
from datetime import datetime, timedelta
import pandas as pd
import re
import filter_tma_report
import filter_tma_report_new
import candidate_report
from Models import DownloadDump
from lib.ms_sql import MsSql
from lib.postgre_sql import PostgreSql

#from lib.log import Log
#from lib.log import log

app = Flask(__name__)

api = Api(app)
app.config["SESSION_PERMANENT"] = True
app.secret_key = config.secret_key

#sessions
@app.route('/log_out',methods=['GET', 'POST'])
def report_log_out():
    if g.user:
        session.pop('user_name', None)
        session.pop('user_id', None)
        return redirect('/')
        #return render_template("login.html",error=config.displaymsg)
    else:
        return render_template("login.html",error="Already logged out")
    
@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=config.SessionTimeOut)

    g.user = None
    g.course_id = None
    g.center_category_id = None
    g.center_type_id = None
    g.center_id = None
    g.user_id = None
    g.user_role_id = None
    g.web_user_id = None
    g.batch_id = None
    g.qp_id = None
    g.client_id = None
    g.question_type_id = None
    g.section_type_id = None
    g.section_id = None
    g.state_id = None
    g.parent_center_id = None
    g.session_course_id = None
    g.User_detail_with_ids = []
    g.session_data = None
    g.project_id= None
    g.user_role = None
    g.Batch_Sessions=None
    g.sector_id=None
    g.contract_id=None
    g.RegisteredCandidatesList=None
    g.subproject_id=None
    g.project_code=None
    
    if 'user_name' in session.keys():
        g.user = session['user_name']
        g.user_id = session['user_id']
        g.user_role = session['user_role_id']
        g.user_region_id=session['user_region_id']
        g.base_url = session['base_url']
        # print(g.user,g.user_id,g.user_role)
        g.User_detail_with_ids.append(g.user)
        g.User_detail_with_ids.append(g.user_id)
        g.User_detail_with_ids.append(g.user_role)
        g.User_detail_with_ids.append(g.base_url)
        g.User_detail_with_ids.append(g.user_region_id)
    if 'course_id' in session.keys():
        g.course_id = session['course_id']
    if 'center_category_id' in session.keys():
        g.center_category_id = session['center_category_id']
    if 'center_type_id' in session.keys():
        g.center_type_id = session['center_type_id']
    if 'center_id' in session.keys():
        g.center_id = session['center_id']
    if 'web_user_role_id' in session.keys():
        g.user_role_id = session['web_user_role_id']
    if 'web_user_id' in session.keys():
        g.web_user_id = session['web_user_id']
    if 'batch_id' in session.keys():
        g.batch_id = session['batch_id']
    if 'qp_id' in session.keys():
        g.qp_id = session['qp_id']
    if 'client_id' in session.keys():
        g.client_id = session['client_id']
    if 'region_id' in session.keys():
        g.region_id = session['region_id']
    if 'cluster_id' in session.keys():
        g.cluster_id = session['cluster_id']
    if 'question_type_id' in session.keys():
        g.question_type_id = session['question_type_id']
    if 'section_type_id' in session.keys():
        g.section_type_id = session['section_type_id']
    if 'section_id' in session.keys():
        g.section_id=session['section_id']
    if 'state_id' in session.keys():
        g.state_id=session['state_id']
    if 'sub_center_id' in session.keys():
        g.sub_center_id = session['sub_center_id']
    if 'parent_center_id' in session.keys():
        g.parent_center_id = session['parent_center_id']
    if 'session_course_id' in session.keys():
        g.session_course_id = session['session_course_id']
    if 'session_data' in session.keys():
        
        #g.session_data.expend(session['session_data'])
        g.session_data = session['session_data']
        #return str(g.session_data) + str(session['session_data'])
    if 'project_id' in session.keys():
        g.project_id=session['project_id']
    if 'Batch_Sessions' in session.keys():
        g.Batch_Sessions=session['Batch_Sessions']
    if 'RegisteredCandidatesList' in session.keys():
        g.RegisteredCandidatesList=session['RegisteredCandidatesList']
    if 'sector_id' in session.keys():
        g.sector_id = session['sector_id']
    if 'contract_id' in session.keys():
        g.contract_id = session['contract_id']
    if 'project_code' in session.keys():
        g.project_code=session['project_code']
    if 'subproject_id' in session.keys():
        g.subproject_id=session['subproject_id']
    
    

#home_API's
#home_batch -> for batchlist in home page
@app.route("/")
def index():
    if g.user:        
        return render_template("home.html",values=g.User_detail_with_ids,html="dashboard")
    else:
        return render_template("login.html",error=config.displaymsg)

@app.route("/dashboard")
def dashboard():
    if g.user:
        return render_template("Dashboard/dashboard.html")
    else:
        return redirect("/")
        
@app.route("/EraseDisplayMsg")
def EraseDisplayMsg():
    config.displaymsg=""
    return redirect(url_for('index'))
    
@app.route("/home")
def home():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="dashboard")
    else:        
        return redirect(url_for('index'))


@app.route("/login", methods=['POST'])
def login():
    if request.method == 'POST':
        tr = []
        email = request.form['inemailaddress']
        passw = request.form['inpassword']
        tr = Database.Login(email,passw)
        if tr != []:
            if tr[0]['Is_Active'] == 1:
                session['user_name'] = tr[0]['User_Name']            
                session['user_id'] = tr[0]['User_Id']
                session['user_role_id'] = tr[0]['User_Role_Id']
                session['user_region_id'] = tr[0]['Region_Id']  
                session['base_url'] = config.Base_URL         
                config.displaymsg=""
                return redirect(url_for('home'))
                #assign_sessions()
            elif tr[0]['Is_Active'] == 0:
                config.displaymsg="Please contact admin because this user is inactive."
                return redirect(url_for('index'))
            else:
                config.displaymsg="Unknown error"
                return redirect(url_for('index'))
            
        else:
            config.displaymsg="wrong"
            return redirect(url_for('index'))
        
####################################################################################################

        

#Center_API's
@app.route("/center_list_page")
def center_list_page():
    if g.user:
        status=request.args.get('status',-1,type=int)
        return render_template("Master/center-list.html", status=status)
    else:
        return redirect("/")

@app.route("/center")
def center():
    if g.user:
        status=request.args.get('status',-1,type=int) 
        html_str="center_list_page?status=" + str(status)
        return render_template("home.html",values=g.User_detail_with_ids,html=html_str)
    else:
        return render_template("login.html",error="Session Time Out!!")
    

@app.route("/center_add_edit")
def center_add_edit():
    if g.user:
        return render_template("Master/center-add-edit.html",center_id=g.center_id)
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/assign_center_add_edit_to_home", methods=['GET','POST'])
def assign_center_add_edit_to_home():
    #global glob_center_id
    #print(request.form['hdn_center_id'])
    #glob_center_id=request.form['hdn_center_id']
    session['center_id'] = request.form['hdn_center_id']
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="center_add_edit")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/after_popup_center")
def after_popup_center():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="center")
    else:
        return render_template("login.html",error="Session Time Out!!")


class add_center_details(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            center_name=request.form['CenterName']
            user_id=g.user_id
            is_active=request.form['isactive']
            center_id=request.form['CenterId']
            center_type_id=request.form['CenterType']
            center_category_id=request.form['CenterCategory']
            bu_id=request.form['BUId']
            region_id=request.form['RegionId']
            cluster_id=request.form['ClusterId']
            country_id=request.form['CenterCountry']
            satet_id=request.form['CenterState']
            district_id=request.form['CenterDistrict']
            location_name=request.form['LocationName']
            return Master.add_center(center_name,user_id,is_active,center_id,center_type_id,center_category_id,bu_id,region_id,cluster_id,country_id,satet_id,district_id,location_name)

class get_center_details(Resource):
    @staticmethod
    def get():
        if request.method == 'GET':
            return jsonify(Master.AllCenters(g.center_id))

class get_all_BU(Resource):
    @staticmethod
    def get():
        if request.method == 'GET':
            return Master.get_all_BU()
class get_all_Cluster_Based_On_Region(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            region_id=request.form['region_id']
            return  Master.get_all_Cluster_Based_On_Region(region_id)

class download_centers_list(Resource):
    DownloadPath=config.DownloadPathLocal
    report_name = "Center_List_"+datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    @staticmethod
    def post():
        if request.method=='POST':
            try:
                center_type_ids = request.form['center_type_ids']
                bu_ids = request.form['bu_ids']
                status = request.form['status']
                r=re.compile("Center_List_.*")
                lst=os.listdir(download_centers_list.DownloadPath)
                newlist = list(filter(r.match, lst))
                for i in newlist:
                    os.remove( download_centers_list.DownloadPath + i)
                path = '{}{}.xlsx'.format(download_centers_list.DownloadPath,download_centers_list.report_name)
                res=center_api.DownloadCenterList.download_centers_list(center_type_ids,bu_ids,status,path)
                print(download_centers_list.report_name)
                print(path)
                ImagePath=config.DownloadPathWeb
                return {'FileName':download_centers_list.report_name,'FilePath':ImagePath}
            except Exception as e:
                print(str(e))
                return {"exceptione":str(e)}

api.add_resource(download_centers_list,'/download_centers_list')

api.add_resource(get_all_BU,'/Get_all_BU')
api.add_resource(get_all_Cluster_Based_On_Region,'/Get_all_Cluster_Based_On_Region')
api.add_resource(center_api.center_list, '/center_list')
api.add_resource(center_api.all_center_type, '/AllCenterTypes')
api.add_resource(center_api.all_center_categories, '/AllCenterCategories')
api.add_resource(center_api.all_countries, '/AllCountries')
api.add_resource(center_api.all_states_based_on_country, '/AllStatesBasedOnCountry')
api.add_resource(center_api.all_districts_based_on_state, '/AllDistrictsBasedOnState')

api.add_resource(get_center_details, '/GetCenterDetails')
api.add_resource(add_center_details, '/add_center_details')
####################################################################################################
#Center_Type_API's
@app.route("/center_type_list_page")
def center_type_list_page():
    if g.user:
        return render_template("Master/center-type-list.html")
    else:
        return render_template("login.html",error="Session Time Out!!")


@app.route("/center_type")
def center_type():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="center_type_list_page")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/center_type_add_edit")
def center_type_add_edit():
    if g.user:
        return render_template("Master/center-type-add-edit.html",center_type_id=g.center_type_id)
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/assign_center_type_add_edit_to_home", methods=['GET','POST'])
def assign_center_type_add_edit_to_home():
    #global glob_center_type_id
    #print(request.form['hdn_center_type_id'])
    #glob_center_type_id=request.form['hdn_center_type_id']
    #return request.form['hdn_center_type_id']
    session['center_type_id'] = request.form['hdn_center_type_id']
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="center_type_add_edit")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/after_popup_center_type")
def after_popup_center_type():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="center_type")
    else:
        return render_template("login.html",error="Session Time Out!!")

class add_center_type_details(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            center_type_name=request.form['CenterTypeName']
            user_id=g.user_id
            is_active=request.form['isactive']
            center_type_id=request.form['CenterTypeId']
            return Master.add_center_type(center_type_name,user_id,is_active,center_type_id)



class get_center_type_details(Resource):
    @staticmethod
    def get():
        if request.method == 'GET':
            try: 
                return jsonify(Master.get_center_type(g.center_type_id))
            except Exception as e:
                return {'message':str(e)}
                
class center_type_list(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            center_type_id = request.form['center_type_id'] 
            start_index = request.form['start']
            page_length = request.form['length']
            search_value = request.form['search[value]']
            order_by_column_position = request.form['order[0][column]']
            order_by_column_direction = request.form['order[0][dir]']
            draw=request.form['draw']
            CenterT = Master.center_type_list(center_type_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)
            return CenterT



api.add_resource(center_type_list, '/center_type_list')
api.add_resource(add_center_type_details, '/add_center_type_details')
api.add_resource(get_center_type_details, '/GetCenterTypeDetails')
 
####################################################################################################
#Center_Category_API's
@app.route("/center_category_list_page")
def center_category_list_page():
    if g.user:
        return render_template("Master/center-category-list.html")
    else:
        return render_template("login.html",error="Session Time Out!!")
   
@app.route("/center_category")
def center_category():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="center_category_list_page")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/center_category_add_edit")
def center_category_add_edit():
    if g.user:
        return render_template("Master/center-category-add-edit.html",center_category_id=g.center_category_id)
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/assign_center_category_add_edit_to_home", methods=['GET','POST'])
def assign_center_category_add_edit_to_home():
    #global glob_center_category_id
    #print(request.form['hdn_center_category_id'])
    #glob_center_category_id=request.form['hdn_center_category_id']
    session['center_category_id'] = request.form['hdn_center_category_id']
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="center_category_add_edit")
    else:
        return render_template("login.html",error="Session Time Out!!")

    
@app.route("/after_popup_center_category")
def after_popup_center_category():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="center_category")
    else:
        return render_template("login.html",error="Session Time Out!!")

class add_center_category_details(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            center_category_name=request.form['CenterCategoryName']
            user_id=g.user_id
            is_active=request.form['isactive']
            center_category_id=request.form['CenterCategoryId']
            return Master.add_center_category(center_category_name,user_id,is_active,center_category_id)


class get_center_category_details(Resource):
    @staticmethod
    def get():
        if request.method == 'GET':
            #global glob_center_category_id
            #g.center_category_id
            return jsonify(Master.get_center_category(g.center_category_id))


api.add_resource(center_category_api.center_category_list, '/center_category_list')
api.add_resource(add_center_category_details, '/add_center_category_details')
api.add_resource(get_center_category_details, '/GetCenterCategoryDetails')
 
####################################################################################################
#Course_API's
@app.route("/course_list_page")
def course_list_page():
    if g.user:
        status=request.args.get('status',-1,type=int)
        return render_template("Content/course-list.html",status=status)
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/course")
def course():
    if g.user:
        status=request.args.get('status',-1,type=int) 
        html_str="course_list_page?status=" + str(status)
        return render_template("home.html",values=g.User_detail_with_ids,html=html_str)
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/course_add_edit")
def course_add_edit():
    if g.user:
        return render_template("Content/course-add-edit.html",course_id=g.course_id)
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/assign_course_add_edit_to_home", methods=['GET','POST'])
def assign_course_type_add_edit_to_home():
    
    #global glob_course_id
    #return(request.form['hdn_course_id'])
    #glob_course_id= request.form['hdn_course_id']
    session['course_id'] = request.form['hdn_course_id']
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="course_add_edit")
    else:
        return render_template("login.html",error="Session Time Out!!")


@app.route("/after_popup_course")
def after_popup_course():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="course")
    else:
        return render_template("login.html",error="Session Time Out!!")

######### API with g data
class add_course_details(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            course_name=request.form['CourseName']
            #project_id=13    ### WHY project id is fixed
            project_id=request.form['ProjectId']
            user_id=g.user_id
            qp_id=request.form['QpId']
            is_active=request.form['isactive']
            center_ids=request.form['CenterId']
            items=request.form['SessionJSON']
            course_id=request.form['CourseId']
            course_code=request.form['CourseCode']
            return Content.add_course(course_name,project_id,user_id,is_active,center_ids,qp_id,course_id,items,course_code)
            
class GetCourseDetails(Resource):
    @staticmethod
    def get():
        if request.method == 'GET':
            course_id=int(request.args['course_id'])
            return Content.get_course(course_id)

class get_qp_for_course(Resource):
    @staticmethod
    def get():
        if request.method == 'GET':
            return Content.get_qp_for_course()

api.add_resource(course_api.course_list, '/course_list')
api.add_resource(course_api.AllCenterList, '/AllCenterList')
api.add_resource(course_api.AllPracticeList, '/AllPracticeList')
api.add_resource(course_api.AllProjectsBasedOnPractice, '/AllProjectsBasedOnPractice')

api.add_resource(add_course_details, '/add_course_details')
api.add_resource(GetCourseDetails, '/GetCourseDetails')
api.add_resource(get_qp_for_course,'/get_qp_for_course')

####################################################################################################

#User_role_API's
@app.route("/user_role_list_page")
def user_role_list_page():
    if g.user:
        return render_template("User_Management/user-role-list.html")
    else:
        return render_template("login.html",error="Session Time Out!!")


@app.route("/user_role")
def user_role():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="user_role_list_page")
    else:
        return render_template("login.html",error="Session Time Out!!")


@app.route("/user_role_add_edit")
def user_role_add_edit():
    if g.user:
        return render_template("User_Management/user-role-add-edit.html",user_role_id=g.user_role_id)
    else:
        return render_template("login.html",error="Session Time Out!!")


@app.route("/assign_user_role_add_edit_to_home", methods=['GET','POST'])
def assign_user_role_add_edit_to_home():
    session['web_user_role_id'] = request.form['hdn_user_role_id']
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="user_role_add_edit")
    else:
        return render_template("login.html",error="Session Time Out!!")


@app.route("/after_popup_user_role")
def after_popup_user_role():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="user_role")
    else:
        return render_template("login.html",error="Session Time Out!!")

##############################  API   #########################
class user_role_list(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            user_role_id = request.form['user_role_id'] 
            start_index = request.form['start']
            page_length = request.form['length']
            search_value = request.form['search[value]']
            order_by_column_position = request.form['order[0][column]']
            order_by_column_direction = request.form['order[0][dir]']
            draw=request.form['draw']
            return UsersM.user_role_list(user_role_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)

class add_user_role_details(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            user_role_name=request.form['UserRoleName']
            user_id=g.user_id
            is_active=request.form['isactive']
            user_role_id=g.user_role_id
            return UsersM.add_user_role(user_role_name,user_id,is_active,user_role_id)
                    
class get_user_role_details(Resource):
    @staticmethod
    def get():
        if request.method == 'GET':
            return UsersM.get_user_role(g.user_role_id)



api.add_resource(get_user_role_details, '/GetUserRoleDetails')
api.add_resource(add_user_role_details, '/add_user_role_details')
api.add_resource(user_role_list, '/user_role_list')

####################################################################################################
#Users_API's
@app.route("/user_list_page")
def user_list_page():
    if g.user:
        role_id=request.args.get('role_id',-1,type=int)
        return render_template("User_Management/user-list.html",role=role_id)
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/user",methods=['GET','POST'])
def user():
    if g.user:
        role_id=request.args.get('role_id',-1,type=int) 
        html_str="user_list_page?role_id=" + str(role_id)       
        return render_template("home.html",values=g.User_detail_with_ids,html=html_str)
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/user_add_edit")
def user_add_edit():
    if g.user:
        return render_template("User_Management/user-add-edit.html",user_id=g.web_user_id)
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/assign_user_add_edit_to_home", methods=['GET','POST'])
def assign_user_type_add_edit_to_home():
    session['web_user_id']=request.form['hdn_user_id']
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="user_add_edit")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/after_popup_user")
def after_popup_user():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="user")
    else:
        return render_template("login.html",error="Session Time Out!!")

####################  API  #######################
class user_list(Resource):
    @staticmethod
    def post():
        
        if request.method == 'POST':
            user_id = request.form['user_id']
            start_index = request.form['start']
            page_length = request.form['length']
            search_value = request.form['search[value]']
            order_by_column_position = request.form['order[0][column]']
            order_by_column_direction = request.form['order[0][dir]']
            draw=request.form['draw']
            dept_ids=request.form['dept_ids']
            role_ids=request.form['role_ids']
            entity_ids=request.form['entity_ids']
            region_ids=request.form['region_ids']
            RM_Role_ids=request.form['RM_Role_ids']
            R_mangager_ids=request.form['R_mangager_ids']
            filter_role_id=request.form['filter_role_id']
            user_region_id=request.form['user_region_id']
            user_role_id=request.form['user_role_id']
            status_ids=request.form['status_ids']
            project_ids=request.form['project_ids']
            #print(user_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw,dept_ids,role_ids,entity_ids,region_ids,RM_Role_ids,R_mangager_ids,filter_role_id,user_region_id,user_role_id,status_ids,project_ids)
            return UsersM.user_list(user_id,filter_role_id,user_region_id,user_role_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw, dept_ids, role_ids, entity_ids, region_ids, RM_Role_ids, R_mangager_ids,status_ids,project_ids)
            

class add_user_details(Resource):
    @staticmethod
    def post():
        try:
            if request.method == 'POST':
                center_ids=""
                user_role_id=request.form['UserRole']
                first_name=request.form['FirstName']
                last_name=request.form['LastName']
                email=request.form['Email']
                mobile=request.form['MobileNumber']
                created_id=g.user_id
                is_active=request.form['isactive']
                user_id=g.web_user_id
                Id=request.form['Id']
                is_reporting_manager=request.form['IsReportingManager']
                return UsersM.add_user(user_role_id,first_name,last_name,email,mobile,created_id,is_active,user_id,Id,is_reporting_manager)
        except Exception as e:
            msg={"message":str(e), "UserId": 0}
            return {"PopupMessage": msg}
                    
class all_user_role(Resource):
    @staticmethod
    def get():
        if request.method == 'GET':
            return UsersM.AllUserRole()


class get_user_details(Resource):
    @staticmethod
    def get():
        if request.method == 'GET':
            #return g.web_user_id
            return UsersM.get_user(g.web_user_id)


api.add_resource(user_list, '/user_list')
api.add_resource(add_user_details, '/add_user_details')
api.add_resource(all_user_role, '/AllUserRole')
api.add_resource(get_user_details, '/GetUserDetails')

####################################################################################################
#Batch_API's

@app.route("/batch_list_page")
def batch_list_page():
    if g.user:
        status=request.args.get('status',-1,type=int)
        if int(g.user_role) in [11,12,13,14,18]:
            return render_template("Batch/home-batch-list.html")
        else:
            return render_template("Batch/batch-list.html", status=status)
    else:
        return render_template("login.html",error="Session Time Out!!")


@app.route("/batch")
def batch():
    if g.user:
        status=request.args.get('status',-1,type=int) 
        html_str="batch_list_page?status=" + str(status)
        return render_template("home.html",values=g.User_detail_with_ids,html=html_str)
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/batch_add_edit")
def batch_add_edit():
    if g.user:
        return render_template("Batch/batch-add-edit.html",batch_id=g.batch_id)
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/assign_batch_add_edit_to_home", methods=['GET','POST'])
def assign_batch_add_edit_to_home():
    
    session['batch_id']=request.form['hdn_batch_id']
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="batch_add_edit")
    else:
        return render_template("login.html",error="Session Time Out!!")


@app.route("/after_popup_batch")
def after_popup_batch():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="batch")
    else:
        return render_template("login.html",error="Session Time Out!!")
    
#################################  API  ###################

class batch_list(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            batch_id = request.form['batch_id'] 
            start_index = request.form['start']
            page_length = request.form['length']
            search_value = request.form['search[value]']
            order_by_column_position = request.form['order[0][column]']
            order_by_column_direction = request.form['order[0][dir]']
            draw=request.form['draw']
            user_role_id  = request.form['user_role_id']
            user_id = request.form['user_id']
            
            return Batch.batch_list(batch_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw,user_id,user_role_id)

class batch_list_updated(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            
            batch_id = request.form['batch_id'] 
            
            user_role_id  = request.form['user_role_id']
            user_id = request.form['user_id']
            customer = request.form['customer']
            project = request.form['project']
            sub_project = request.form['sub_project']
            region = request.form['region']
            center = request.form['center']
            center_type = request.form['center_type']
            status = request.form['status']
            #print('before hi')
            BU=''
            if 'BU' in request.form:
                BU = request.form['BU']            
            course_ids=''
            if 'course_ids' in request.form:
                course_ids=request.form['course_ids']

            start_index = request.form['start']
            page_length = request.form['length']
            search_value = request.form['search[value]']
            order_by_column_position = request.form['order[0][column]']
            order_by_column_direction = request.form['order[0][dir]']
            draw=request.form['draw']
            
            return Batch.batch_list_updated(batch_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw,user_id,user_role_id, status, customer, project, sub_project, region, center, center_type,course_ids, BU)

class add_batch_details(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            BatchId=request.form['BatchId']
            BatchName=request.form['BatchName']
            #BatchCode=request.form['BatchCode']
            Center=request.form['Center']
            Trainer=request.form['Trainer']
            PlannedStartDate=request.form['PlannedStartDate']
            PlannedEndDate=request.form['PlannedEndDate']
            ActualStartDate=request.form['ActualStartDate']
            ActualEndDate=request.form['ActualEndDate']
            StartTime=request.form['StartTime']
            EndTime=request.form['EndTime']
            user_id=g.user_id
            isactive=request.form['isactive']
            Product=request.form['Product']
            Course=request.form['Course']
            SubProject=request.form['SubProject']
            Cofunding=request.form['Cofunding']
        
            return Batch.add_batch(BatchName, Product, Center, Course, SubProject, Cofunding, Trainer, isactive, PlannedStartDate, PlannedEndDate, ActualStartDate, ActualEndDate, StartTime, EndTime, BatchId, user_id)


class get_batch_details(Resource):
    @staticmethod
    def get():
        if request.method == 'GET':
            return Batch.get_batch(g.batch_id)

class all_course_list(Resource):
    @staticmethod
    def get():
        if request.method == 'GET':
            return Batch.AllCourse()

class centers_based_on_course(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            course_id=request.form['course_id']
            return Batch.AllCenterOnCourse(course_id)

class trainers_based_on_center(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            center_id=request.form['center_id']
            return Batch.AllTrainersOnCenter(center_id)

class center_manager_based_on_center(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            center_id=request.form['center_id']
            return Batch.AllCenterManagerOnCenter(center_id)

class sub_center_based_on_center(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            center_id=request.form['center_id']
            
            return Batch.AllSubCenterOnCenter(center_id)

class candidates_based_on_course(Resource):
    @staticmethod
    def post():
         if request.method == 'POST':
            candidate_id = request.form['candidate_id']
            course_ids = request.form['course_id']
            center_id = request.form['center_id']
            batch_id=request.form['batch_id']
            start_index = request.form['start']
            page_length = request.form['length']
            search_value = request.form['search[value]']
            order_by_column_position = request.form['order[0][column]']
            order_by_column_direction = request.form['order[0][dir]']
            draw=request.form['draw']
            return Batch.candidate_based_on_course(candidate_id,course_ids,batch_id,center_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)

class candidates_maped_in_batch(Resource):
    @staticmethod
    def post():
         if request.method == 'POST':
            candidate_id = request.form['candidate_id']
            course_ids = request.form['course_id']
            center_id = request.form['center_id']
            batch_id=request.form['batch_id']
            start_index = request.form['start']
            page_length = request.form['length']
            search_value = request.form['search[value]']
            order_by_column_position = request.form['order[0][column]']
            order_by_column_direction = request.form['order[0][dir]']
            draw=request.form['draw']
            return Batch.candidate_maped_in_batch(candidate_id,course_ids,batch_id,center_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)

class add_edit_map_candidate_batch(Resource):
    @staticmethod
    def post():
        candidate_ids=request.form['candidate_ids']
        batch_id=request.form['batch_id']
        course_id=request.form['course_id']
        user_id= g.user_id
        return Batch.add_edit_candidate_batch(str(candidate_ids),batch_id,course_id,user_id)


class drop_edit_map_candidate_batch(Resource):
    @staticmethod
    def post():
        candidate_ids=request.form['candidate_ids']
        batch_id=request.form['batch_id']
        course_id=request.form['course_id']
        user_id= g.user_id
        drop_remark = request.form['drop_remark']
        return Batch.drop_edit_candidate_batch(str(candidate_ids),batch_id,course_id,user_id,drop_remark)


api.add_resource(batch_list, '/batch_list')
api.add_resource(batch_list_updated, '/batch_list_updated')
api.add_resource(add_batch_details, '/add_batch_details')
api.add_resource(get_batch_details, '/GetBatchDetails')
api.add_resource(all_course_list, '/AllCourseList')
api.add_resource(centers_based_on_course, '/CentersBasedOnCourse')
api.add_resource(trainers_based_on_center, '/TrainersBasedOnCenter')
api.add_resource(center_manager_based_on_center, '/CenterManagerBasedOnCenter')
api.add_resource(candidates_based_on_course,'/ALLCandidatesBasedOnCourse')
api.add_resource(candidates_maped_in_batch,'/ALLCandidatesMapedInBatch')
api.add_resource(add_edit_map_candidate_batch,'/add_edit_map_candidate_batch')
api.add_resource(drop_edit_map_candidate_batch,'/drop_edit_candidate_batch')
api.add_resource(sub_center_based_on_center, '/SubCenterBasedOnCenter')
####################################################################################################

#QP_API's
@app.route("/qp_list_page")
def qp_list_page():
    if g.user:
        return render_template("Content/qp-list.html")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/qp")
def qp():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="qp_list_page")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/qp_add_edit")
def qp_add_edit():
    if g.user:
        return render_template("Content/qp-add-edit.html",qp_id=g.qp_id)
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/assign_qp_add_edit_to_home", methods=['GET','POST'])
def assign_qp_add_edit_to_home():
    session['qp_id']=request.form['hdn_qp_id']
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="qp_add_edit")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/after_popup_qp")
def after_popup_qp():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="qp")
    else:
        return render_template("login.html",error="Session Time Out!!")

class qp_list(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            user_id=request.form['user_id']
            user_role_id=request.form['user_role_id']
            qp_id = request.form['qp_id']
            start_index = request.form['start']
            page_length = request.form['length']
            search_value = request.form['search[value]']
            order_by_column_position = request.form['order[0][column]']
            order_by_column_direction = request.form['order[0][dir]']
            draw=request.form['draw']

            sectors = request.form['sectors']
            
            return Content.qp_list(user_id,user_role_id,qp_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw, sectors)

class add_qp_details(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            qp_name=request.form['QpName']
            qp_code=request.form['QpCode']
            user_id=g.user_id
            is_active=request.form['isactive']
            qp_id=g.qp_id
            return Content.add_qp(qp_name,qp_code,user_id,is_active,qp_id)

class get_qp_details(Resource):
    @staticmethod
    def get():
        return Content.get_qp(g.qp_id)

api.add_resource(qp_list, '/qp_list')
api.add_resource(add_qp_details, '/add_qp_details')
api.add_resource(get_qp_details, '/GetQpDetails')

  

#######################################################################################################


#Candidate_API's

@app.route("/candidate_list_page")
def candidate_list_page():
    if g.user:
        return render_template("Candidate/candidate-list.html")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/candidate")
def candidate():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="candidate_list_page")
    else:
        return render_template("login.html",error="Session Time Out!!")

class get_project_basedon_client_multiple(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            client_id=request.form['ClientId']
            user_id=0
            if 'user_id' in request.form:
                user_id=request.form['user_id']
            user_role_id=0
            if 'user_role_id' in request.form:
                user_role_id=request.form['user_role_id']
            return Candidate.get_project_basedon_client_multiple(user_id,user_role_id,client_id)

class get_project_basedon_client(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            client_id=request.form['ClientId']
            return Candidate.get_project_basedon_client(client_id)


class get_cand_course_basedon_proj(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            project_id=request.form['ProjectId']
            return Candidate.get_cand_course_basedon_proj(project_id)

class get_cand_course_basedon_proj_multiple(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            project_id=request.form['ProjectId']
            return Candidate.get_cand_course_basedon_proj_multiple(project_id)

class get_cand_center_basedon_course(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            course_id = request.form['CourseId']
            return Candidate.get_cand_center_basedon_course(course_id)

class get_cand_center_basedon_course_multiple(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            user_id=0
            if 'user_id' in request.form:
                user_id=request.form['user_id']
            user_role_id=0
            if 'user_role_id' in request.form:
                user_role_id=request.form['user_role_id']
            course_id = request.form['CourseId']
            RegionId = request.form['RegionId']
            return Candidate.get_cand_center_basedon_course_multiple(user_id,user_role_id,course_id, RegionId)

class get_section_for_cand(Resource):
    @staticmethod
    def get():
        if request.method == 'GET':
            return Candidate.get_section_for_cand()

class candidate_list(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            candidate_id = request.form['candidate_id']
            sub_project = request.form['sub_project']
            project = request.form['project']
            region = request.form['region']
            customer = request.form['customer']
            status = request.form['status']
            center_type = request.form['center_type']
            center = request.form['center']
            user_id=request.form['user_id']
            user_role_id=request.form['user_role_id']
            
            start_index = request.form['start']
            page_length = request.form['length']
            search_value = request.form['search[value]']
            order_by_column_position = request.form['order[0][column]']
            order_by_column_direction = request.form['order[0][dir]']
            draw=request.form['draw']
            
            #print(candidate_id,customer,project,sub_project,region,center,center_type,status,user_id,user_role_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)
            return Candidate.candidate_list(candidate_id,customer,project,sub_project,region,center,center_type,status,user_id,user_role_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)


api.add_resource(candidate_list, '/candidate_list')
api.add_resource(get_project_basedon_client_multiple,'/GetALLProject_multiple')
api.add_resource(get_project_basedon_client,'/GetALLProject')
api.add_resource(get_cand_course_basedon_proj, '/get_cand_course_basedon_proj')
api.add_resource(get_cand_course_basedon_proj_multiple, '/get_cand_course_basedon_proj_multiple')
api.add_resource(get_cand_center_basedon_course, '/get_cand_center_basedon_course')
api.add_resource(get_cand_center_basedon_course_multiple, '/get_cand_center_basedon_course_multiple')
api.add_resource(get_section_for_cand,'/GetSectionCand')

####################################################################################################


#Client_API's
@app.route("/client_list_page",methods=['GET','POST'])
def client_list_page():
    if g.user:
        print(request.args.get('client',100,type=int))
        return render_template("Master/client-list.html",active=1)
    else:
        return render_template("login.html",error="Session Time Out!!")


@app.route("/client",methods=['GET','POST'])
def client():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="client_list_page")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/client_add_edit")
def client_add_edit():
    if g.user:
        return render_template("Master/client-add-edit.html",client_id=g.client_id)
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/assign_client_add_edit_to_home", methods=['GET','POST'])
def assign_client_add_edit_to_home():
    session['client_id']=request.form['hdn_client_id']
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="client_add_edit")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/after_popup_client")
def after_popup_client():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="client")
    else:
        return render_template("login.html",error="Session Time Out!!")

class client_list(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            user_id = request.form['user_id'] 
            user_role_id = request.form['user_role_id'] 
            client_id = request.form['client_id'] 
            if 'is_active' in request.form:
                Is_Active=request.form['is_active']
            else:
                Is_Active=-1
            start_index = request.form['start']
            page_length = request.form['length']
            search_value = request.form['search[value]']
            order_by_column_position = request.form['order[0][column]']
            order_by_column_direction = request.form['order[0][dir]']
            draw=request.form['draw']
            funding_sources = request.form['funding_sources']
            customer_groups = request.form['customer_groups']
            category_type_ids = request.form['category_type_ids']
            #print(order_by_column_position,order_by_column_direction)
            return Master.client_list(user_id,user_role_id,client_id,Is_Active,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw, funding_sources,customer_groups,category_type_ids)

class add_client_details(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            client_name=request.form['ClientName']
            client_code=request.form['ClientCode']
            FundingSource=request.form['FundingSource']
            CustomerGroup=request.form['CustomerGroup']
            IndustryType=request.form['IndustryType']
            CategoryType=request.form['CategoryType']

            user_id=g.user_id
            is_active=request.form['isactive']
            client_id=g.client_id
            return Master.add_client(client_name,client_code,user_id,is_active,client_id,FundingSource, CustomerGroup, IndustryType, CategoryType)

class get_client_details(Resource):
    @staticmethod
    def get():
        if request.method == 'GET':
            return Master.get_client(g.client_id)

api.add_resource(client_list,'/client_list')
api.add_resource(add_client_details,'/add_client_details')
api.add_resource(get_client_details,'/GetClientDetails')


####################################################################################################

#Region_API's
@app.route("/region_list_page")
def region_list_page():
    if g.user:
        return render_template("Master/region-list.html")
    else:
        return render_template("login.html",error="Session Time Out!!")


@app.route("/region")
def region():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="region_list_page")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/region_add_edit")
def region_add_edit():
    if g.user:
        return render_template("Master/region-add-edit.html",region_id=g.region_id)
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/assign_region_add_edit_to_home", methods=['GET','POST'])
def assign_region_add_edit_to_home():
    session['region_id']=request.form['hdn_region_id']
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="region_add_edit")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/after_popup_region")
def after_popup_region():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="region")
    else:
        return render_template("login.html",error="Session Time Out!!")

class region_list(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            region_id = request.form['region_id']
            user_id = request.form['user_id']
            user_role_id = request.form['user_role_id'] 
            user_region_id = request.form['user_region_id'] 
            start_index = request.form['start']
            page_length = request.form['length']
            search_value = request.form['search[value]']
            order_by_column_position = request.form['order[0][column]']
            order_by_column_direction = request.form['order[0][dir]']
            draw=request.form['draw']
            return Master.region_list(region_id,user_id,user_role_id,user_region_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)

class add_region_details(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            region_name=request.form['RegionName']
            region_code=request.form['RegionCode']
            user_id=g.user_id
            is_active=request.form['isactive']
            region_id=g.region_id
            return Master.add_region(region_name,region_code,user_id,is_active,region_id)

class get_region_details(Resource):
    @staticmethod
    def get():
        if request.method == 'GET':
            return Master.get_region(g.region_id)

api.add_resource(region_list,'/region_list')
api.add_resource(add_region_details,'/add_region_details')
api.add_resource(get_region_details,'/GetRegionDetails')


####################################################################################################

#Cluster_API's
@app.route("/cluster_list_page")
def cluster_list_page():
    if g.user:
        return render_template("Master/cluster-list.html")
    else:
        return render_template("login.html",error="Session Time Out!!")


@app.route("/cluster")
def cluster():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="cluster_list_page")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/cluster_add_edit")
def cluster_add_edit():
    if g.user:
        return render_template("Master/cluster-add-edit.html",cluster_id=g.cluster_id)
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/assign_cluster_add_edit_to_home", methods=['GET','POST'])
def assign_cluster_add_edit_to_home():
    session['cluster_id']=request.form['hdn_cluster_id']
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="cluster_add_edit")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/after_popup_cluster")
def after_popup_cluster():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="cluster")
    else:
        return render_template("login.html",error="Session Time Out!!")

class cluster_list(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            cluster_id = request.form['cluster_id'] 
            user_id = request.form['user_id']
            user_role_id = request.form['user_role_id'] 
            user_region_id = request.form['user_region_id']
            start_index = request.form['start']
            page_length = request.form['length']
            search_value = request.form['search[value]']
            order_by_column_position = request.form['order[0][column]']
            order_by_column_direction = request.form['order[0][dir]']
            draw=request.form['draw']
            return Master.cluster_list(cluster_id,user_id,user_role_id,user_region_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)

class add_cluster_details(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            cluster_name=request.form['ClusterName']
            cluster_code=request.form['ClusterCode']
            region_id=request.form['RegionId']
            user_id=g.user_id
            is_active=request.form['isactive']
            cluster_id=g.cluster_id
            return Master.add_cluster(cluster_name,cluster_code,region_id,user_id,is_active,cluster_id)

class get_cluster_details(Resource):
    @staticmethod
    def get():
        if request.method == 'GET':
            return Master.get_cluster(g.cluster_id)

class get_all_Region(Resource):
    @staticmethod
    def get():
        if request.method == 'GET':
            return Master.get_all_Region()


api.add_resource(cluster_list,'/cluster_list')
api.add_resource(add_cluster_details,'/add_cluster_details')
api.add_resource(get_cluster_details,'/GetClusterDetails')
api.add_resource(get_all_Region,'/Get_all_Region')


######################################################################################################


#QuestionType_API's
@app.route("/question_type_list_page")
def question_type_list_page():
    if g.user:
        return render_template("Content/question-type-list.html")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/question_type")
def question_type():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="question_type_list_page")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/question_type_add_edit")
def question_type_add_edit():
    if g.user:
        return render_template("Content/question-type-add-edit.html",question_type_id=g.question_type_id)
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/assign_question_type_add_edit_to_home", methods=['GET','POST'])
def assign_question_type_add_edit_to_home():
    session['question_type_id']=request.form['hdn_question_type_id']
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="question_type_add_edit")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/after_popup_question_type")
def after_popup_question_type():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="question_type")
    else:
        return render_template("login.html",error="Session Time Out!!")

class question_type_list(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            question_type_id = request.form['question_type_id'] 
            start_index = request.form['start']
            page_length = request.form['length']
            search_value = request.form['search[value]']
            order_by_column_position = request.form['order[0][column]']
            order_by_column_direction = request.form['order[0][dir]']
            draw=request.form['draw']
            return Content.question_type_list(question_type_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)


class add_question_type_details(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            question_type_name=request.form['QuestionTypeName']
            user_id=g.user_id
            is_active=request.form['isactive']
            question_type_id=g.question_type_id
            return Content.add_question_type(question_type_name,user_id,is_active,question_type_id)

class get_question_type_details(Resource):
    @staticmethod
    def get():
        if request.method == 'GET':
            return Content.get_question_type(g.question_type_id)

api.add_resource(question_type_list,'/question_type_list')
api.add_resource(add_question_type_details,'/add_question_type_details')
api.add_resource(get_question_type_details,'/GetQuestionTypeDetails')


######################################################################################################


#Section_type_API's
@app.route("/section_type_list_page")
def section_type_list_page():
    if g.user:
        return render_template("Content/section-type-list.html")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/section_type")
def section_type():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="section_type_list_page")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/section_type_add_edit")
def section_type_add_edit():
    if g.user:
        return render_template("Content/section-type-add-edit.html",section_type_id=g.section_type_id)
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/assign_section_type_add_edit_to_home", methods=['GET','POST'])
def assign_section_type_add_edit_to_home():
    session['section_type_id']=request.form['hdn_section_type_id']
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="section_type_add_edit")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/after_popup_section_type")
def after_popup_section_type():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="section_type")
    else:
        return render_template("login.html",error="Session Time Out!!")

class section_type_list(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            section_type_id = request.form['section_type_id'] 
            start_index = request.form['start']
            page_length = request.form['length']
            search_value = request.form['search[value]']
            order_by_column_position = request.form['order[0][column]']
            order_by_column_direction = request.form['order[0][dir]']
            draw=request.form['draw']
            return Content.section_type_list(section_type_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)

class add_section_type_details(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            section_type_name=request.form['SectionTypeName']
            user_id=g.user_id
            is_active=request.form['isactive']
            section_type_id=g.section_type_id
            return Content.add_section_type(section_type_name,user_id,is_active,section_type_id)

class get_section_type_details(Resource):
    @staticmethod
    def get():
        if request.method == 'GET':
            return Content.get_section_type(g.section_type_id)

api.add_resource(section_type_list,'/section_type_list')
api.add_resource(add_section_type_details,'/add_section_type_details')
api.add_resource(get_section_type_details,'/GetSectionTypeDetails')


############################################################################################################

#TMA_REPORT_API's

@app.route("/tma_report_download_page")
def tma_report_download_page():
    if g.user:
        return render_template("TMA-Report/tma-report.html")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/tma_report")
def tma_report():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="tma_report_download_page")
    else:
        return render_template("login.html",error="Session Time Out!!")



@app.route('/tma_report_download_func',methods=['GET', 'POST'])
def tma_user_download():
    print('in out')
    try:
        
        date = request.form["ActivityDate"]
        tma_report_name = 'tma_report'
        tma_path = 'C:/Sites/Neo_Skills_UAT/data/tma_report/'
        
        for i in os.listdir(tma_path):
            os.remove(tma_path + i)

        path = tma_path + '{}.xlsx'.format(tma_report_name)
        res = final_report.create_report(date, path)
        if res['Status']:
            return send_file(path, as_attachment=True)
        else:
            return res['Description']
        
    except Exception as e:
        return str(e)

############################################################################################################

#TMA_BATCH_API's

class get_trainer_data(Resource):
    @staticmethod
    def get():
        try:
            if request.method == 'GET':

                out = Database.get_trainer_data_db()
                res = []
                for i in out:
                    res.append({'trainer_name':i[0],'trainer_email':i[1]})
                
                return jsonify(res)
        except Exception as e:
            return jsonify(str(e))

class get_batch_list(Resource):
    @staticmethod
    def post():
        try:
            if request.method == 'POST':
                email_address = 'all'
                if (str(request.form['email_address']) != None) and (str(request.form['email_address']) !=''):
                    email_address = str(request.form['email_address']).lower()
                email_condition = ""
                if email_address != 'all':
                    email_condition = " AND TRIM(LOWER(TD.email)) = '{}' ".format(email_address)
                
                batch_stage_id= 0
                if (str(request.form['batch_stage_id']) != None) and (str(request.form['batch_stage_id']) != '' ):
                    batch_stage_id = int(request.form['batch_stage_id'])
                    batch_stage_id = 0 if (batch_stage_id < 1) or (batch_stage_id >3) else batch_stage_id

                batch_stage_condition = ""
                if batch_stage_id>0:
                    batch_stage_condition = " AND RES.batch_stage_id= {} ".format(batch_stage_id);

                res = {
                'draw': int(request.form['draw']),
                'recordsTotal' : 0,
                'recordsFiltered' : 0,
                'data' : [],
                'error' : 'Hi Jagdish' + email_address + email_condition
                }
                ##################return res

                

                total_record_count = Database.get_batch_list_count_db(email_condition, batch_stage_condition)[0][0]
                filter_record_count = total_record_count

                

                search_text = str(request.form['search[value]'])
                
                search_condition = ""
                if search_text!='':
                    
                    SearchColumnArray = ["RES.trainer_name",
                                         "RES.trainer_email",
                                         "RES.batch_code",
                                         "RES.batch_start_date",
                                         "RES.batch_end_date",
                                         "RES.batch_status",
                                         "RES.batch_active_status",
                                         "RES.batch_stage_name",
                                         "RES.business_unit",
                                         "RES.center_name",
                                         "RES.center_type",
                                         "RES.course_name",
                                         "RES.qp_name",
                                         "RES.customer_name",
                                         "RES.image_required"]

                    search_condition = " AND ("
                    for searchcolumn in SearchColumnArray:
                        search_condition += "(UPPER(CAST(" + searchcolumn + " AS VARCHAR)) LIKE '%"+ search_text + "%') OR "
                    search_condition = search_condition.rstrip('OR ')
                    search_condition += ") "

                    filter_record_count = Database.getfilter_batch_list_count_db(email_condition, batch_stage_condition, search_condition)[0][0]

                start_index = str(request.form['start'])
                page_length = str(request.form['length'])
                limit_statement = ""

                if (int(start_index)>=0) and (int(page_length)>=0):
                    limit_statement = " OFFSET {} ROWS ".format(start_index)
                    limit_statement += " FETCH NEXT {} ROWS ONLY ".format(page_length)

                order_by_column_array={
                    1 : 'null',
                    2 : "RES.trainer_name",
                    3 : "RES.trainer_email",
                    4 : "RES.batch_code",
                    5 : "CAST(RES.batch_start_date AS DATE)",
                    6 : "CAST(RES.batch_end_date AS DATE)",
                    7 : "RES.batch_status",
                    8 : "RES.batch_active_status",
                    9 : "RES.batch_stage_name",
                    10 : "RES.business_unit",
                    11 : "RES.center_name",
                    12 : "RES.center_type",
                    13 : "RES.course_name",
                    14 : "RES.qp_name",
                    15 : "RES.customer_name",
                    16 : "RES.image_required"}

                

                order_by_column_index = str(request.form['order[0][column]'])
                order_by_column_direction = str(request.form['order[0][dir]'])
                '''
                print ("##############33 HI ###############33")
                print(request.form)
                print(email_address, batch_stage_id)
                print(start_index, page_length)
                print(str(request.form['draw']))
                print(search_text)
                print(order_by_column_index, order_by_column_direction)
                print("##############33 END ###############33")
                '''
                order_by_statement = " ORDER BY 2,4"
                if (int(order_by_column_index) > 1):
                    order_by_statement = " ORDER BY " + order_by_column_array[int(order_by_column_index)] +' '+order_by_column_direction

                result_data = Database.result_data_db(email_condition, batch_stage_condition, search_condition, order_by_statement, limit_statement)
                response_data = []
                if len(result_data) > 0:
                    sno = int(start_index)
                    for Row in result_data:
                        sno += 1
                        data = {}

                        session_count = '<center><a title="No sessions available for this batch" class="btn" style="color:white;padding:2px 5px 2px 5px;background-color:darkgray;">' + str(Row[3])+ '</a></center>' if (Row[3] < 1) else '<center><a title="View Trainer Sessions For This Batch" class="btn btn-primary" style="color:white;cursor:pointer;padding:2px 5px 2px 5px;" onclick="ShowSessions(\'' + Row[1]+ '\',' + str(Row[16])+ ')">' + str(Row[3]) + '</a></center>';
                        data['sno'] = sno
                        data['trainer_name'] = Row[0]
                        data['trainer_email'] = Row[1]
                        data['batch_code'] = Row[2]
                        data['session_count'] = session_count
                        data['batch_start_date'] = Row[4]
                        data['batch_end_date'] = Row[5]
                        data['batch_status'] = Row[6]
                        data['batch_active_status'] = Row[7]
                        data['batch_stage_name'] = Row[8]
                        data['business_unit'] = Row[9]
                        data['center_name'] = Row[10]
                        data['center_type'] = Row[11]
                        data['course_name'] = Row[12]
                        data['qp_name'] = Row[13]
                        data['customer_name'] = Row[14]
                        data['image_required'] = Row[15]
                        
                        response_data.append(data)
                        print(data)

                

                res = {
                    'draw': int(request.form['draw']),
                    'recordsTotal' : total_record_count,
                    'recordsFiltered' : filter_record_count,
                    'data' : response_data
                    }
                return jsonify(res)


                
        except  Exception as e:
            res = {
                'draw': int(request.form['draw']),
                'recordsTotal' : 0,
                'recordsFiltered' : 0,
                'data' : [],
                'error' : 'Hi error' + str(e)
                }
            return jsonify(res)

class get_candidate_attendance(Resource):
    @staticmethod
    def post():
        try:
            if request.method == 'POST':
                #return 'lol'
                batch_id = 0
                if (str(request.form['batch_id']) != None) and (str(request.form['batch_id']) !=''):
                    batch_id = int(request.form['batch_id'])

                session_id= 0
                if (str(request.form['session_id']) != None) and (str(request.form['session_id']) != '' ):
                    session_id = int(request.form['session_id'])
                candidate_attendance = Database.get_candidate_attendance_db(batch_id, session_id)
                out = []
                for i in candidate_attendance:
                    out.append(list(i))

                #return candidate_attendance
                return jsonify(out)
        except  Exception as e:
            res = {'error':str(e)}
            return jsonify(res)



class get_candidate_group_attendance(Resource):
    @staticmethod
    def post():
        try:
            if request.method == 'POST':
                batch_id = 0
                if (str(request.form['batch_id']) != None) and (str(request.form['batch_id']) !=''):
                    batch_id = int(request.form['batch_id'])

                session_id= 0
                if (str(request.form['session_id']) != None) and (str(request.form['session_id']) != '' ):
                    session_id = int(request.form['session_id'])

                candidate_group_attendance = Database.get_candidate_group_attendance_db(batch_id, session_id)
                out = []
                for i in candidate_group_attendance:
                    out.append(list(i))
                return jsonify(out)
                

                return jsonify(candidate_group_attendance)
        except  Exception as e:
            res = {'error' :str(e)}
            return jsonify(res)



#Base URL + "/login" api will provide all the unzynched QP data as response
api.add_resource(get_trainer_data, '/get_trainer_data')


#Base URL + "/login" api will provide all the unzynched QP data as response
api.add_resource(get_batch_list, '/get_batch_list')


#Base URL + "/login" api will provide all the unzynched QP data as response
api.add_resource(get_candidate_attendance, '/get_candidate_attendance')

#Base URL + "/login" api will provide all the unzynched QP data as response
api.add_resource(get_candidate_group_attendance, '/get_candidate_group_attendance')




@app.route("/tma_batch_page")
def tma_batch_page():
    if g.user:
        return render_template("TMA-Report/tma_index.html")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/tma_batch")
def tma_batch():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="tma_batch_page")
    else:
        return render_template("login.html",error="Session Time Out!!")


@app.route("/tma_session_page")
def tma_session_page():
    if g.user:
        #return str(g.session_data)
        return render_template("TMA-Report/tma_session.html", data = g.session_data)
    else:
        return render_template("login.html",error="Session Time Out!!")


@app.route('/trainer_sessions', methods=['GET','POST'])
def trainer_sessions():
    try:
        #return 'lol'
        email = request.args['e'] if (request.args['e']!=None) and (request.args['e']!='') else 'NA'

        batch_id = request.args['b'] if (request.args['b']!=None) and (request.args['b']!='') else '0'

        image_url = 'http://neodevqa01.southindia.cloudapp.azure.com:27072/data/';
                
        data=[email, batch_id]

        
        

        trainer_name = ""
        batch_code = ""
        batch_period = ""
        center_name = ""
        course_name = ""
        trainer_batch = Database.get_trainer_batch(batch_id)

        
        if len(trainer_batch)>0:
            trainer_name = trainer_batch[0][19]
            batch_code = trainer_batch[0][1]
            batch_period = trainer_batch[0][4] + ' to ' + trainer_batch[0][5]
            center_name = trainer_batch[0][7]
            course_name = trainer_batch[0][11]

        trainer_session_data = Database.trainer_session_db(email, batch_id)
        #return str(trainer_session_data)
        data=[email, batch_id, trainer_name, batch_code, batch_period, center_name, course_name]
        
        #return str(data)
        session['session_data'] = data
        #return str(g.session_data) + str(session['session_data'])

        #return str(trainer_session_data)+ str(len(trainer_session_data))
        
        if len(trainer_session_data)>0:
            sno = 0;
            out = ""
            
            for Row in trainer_session_data:
                
                sno += 1
                action = '<a class="btn btn-primary" style="color:white;cursor:pointer;padding:2px 8px 2px 8px;" title="View Session Attendance Details" onclick="ViewSessionAttendanceDetails(' + str(Row[0]) + ',' + str(Row[1]) + ',\'' + str(Row[2]) +  '\')"><i class="fa fa-user"></i></a>';
                action += '<a class="btn btn-success" style="color:white;cursor:pointer;padding:2px 5px 2px 5px;margin-left:2px;" title="View Session Attendance Group Images" onclick="ViewSessionAttendanceGroupImages(' + str(Row[0]) + ',' + str(Row[1]) + ',\'' + str(Row[2]) + '\')"><i class="fa fa-users"></i></a>';

                one_loop = """
                <tr>
                    <td style="text-align:center;">""" + str(sno)+  """ </td>
                    <td style="text-align:center;width:90px;">""" +action +"""</td>
                    <td>""" + Row[2] + """</td>
                
                """
                one_loop += """<td style="text-align:center;">""" + Row[3] +  """</td>""" if (Row[3]!='') and (Row[3]!=None) else """<td style="text-align:center;">-</td>
                """
                #one_loop += """<td style="text-align:center;"><a href='""" + image_url + 'trainer_stage_images/' + Row[4] + """' target="_blank" title="Open image in new tab"><img src='""" + image_url + 'trainer_stage_images/' + Row[4] +"""' style="height:40px;width:60px;border:0px solid lightgray;"/></a></td>""" + Row[4] +  """</td>""" if (Row[4]!='') and (Row[4]!=None) else """<td style="text-align:center;">-</td>
                one_loop += """<td style="text-align:center;"><a href='""" + image_url + 'trainer_stage_images/' + Row[4] + """' target="_blank" title="Open image in new tab"><img src='""" + image_url + 'trainer_stage_images/' + Row[4] +"""' style="height:40px;width:60px;border:0px solid lightgray;"/></a></td>""" if (Row[4]!='') and (Row[4]!=None) else """<td style="text-align:center;">-</td>
                """
                one_loop += """<td style="text-align:center;"><a href="https://www.google.com/maps/search/?api=1&query=""" + Row[5] + ""","""  + Row[6] +  """" target="_blank" title="View location map"><img src="static/images/location.png" style="height:20px;"/></a></td>""" if (Row[5]!='') and (Row[5]!=None) and (Row[6]!='') and (Row[6]!=None) else """<td style="text-align:center;">-</td>

                
                """
                one_loop += """<td style="text-align:center;">""" + Row[7] +  """</td>""" if (Row[7]!='') and (Row[7]!=None) else """<td style="text-align:center;">-</td>
                """
                one_loop += """<td style="text-align:center;"><a href='""" + image_url + 'trainer_stage_images/' + Row[8] + """' target="_blank" title="Open image in new tab"><img src='""" + image_url + 'trainer_stage_images/' + Row[8] +"""' style="height:40px;width:60px;border:0px solid lightgray;"/></a></td>""" if (Row[8]!='') and (Row[8]!=None) else """<td style="text-align:center;">-</td>
                """
                one_loop += """<td style="text-align:center;"><a href="https://www.google.com/maps/search/?api=1&query=""" + Row[9] + ""","""  + Row[10] +  """" target="_blank" title="View location map"><img src="static/images/location.png" style="height:20px;"/></a></td>""" if (Row[9]!='') and (Row[9]!=None) and (Row[10]!='') and (Row[10]!=None) else """<td style="text-align:center;">-</td>

                
                """
                one_loop += """<td style="text-align:center;">""" + Row[11] +  """</td>""" if (Row[11]!='') and (Row[11]!=None) else """<td style="text-align:center;">-</td>
                """
                one_loop += """<td style="text-align:center;"><a href='""" + image_url + 'trainer_stage_images/' + Row[12] + """' target="_blank" title="Open image in new tab"><img src='""" + image_url + 'trainer_stage_images/' + Row[12] +"""' style="height:40px;width:60px;border:0px solid lightgray;"/></a></td>""" if (Row[12]!='') and (Row[12]!=None) else """<td style="text-align:center;">-</td>
                """
                one_loop += """<td style="text-align:center;"><a href="https://www.google.com/maps/search/?api=1&query=""" + Row[13] + ""","""  + Row[14] +  """" target="_blank" title="View location map"><img src="static/images/location.png" style="height:20px;"/></a></td>""" if (Row[13]!='') and (Row[13]!=None) and (Row[14]!='') and (Row[14]!=None) else """<td style="text-align:center;">-</td>

                
                """
                one_loop += """<td style="text-align:center;">""" + Row[15] +  """</td>""" if (Row[15]!='') and (Row[15]!=None) else """<td style="text-align:center;">-</td>
                """
                one_loop += """<td style="text-align:center;"><a href='""" + image_url + 'trainer_stage_images/' + Row[16] + """' target="_blank" title="Open image in new tab"><img src='""" + image_url + 'trainer_stage_images/' + Row[16] +"""' style="height:40px;width:60px;border:0px solid lightgray;"/></a></td>"""  if (Row[16]!='') and (Row[16]!=None) else """<td style="text-align:center;">-</td>
                """
                one_loop += """<td style="text-align:center;"><a href="https://www.google.com/maps/search/?api=1&query=""" + Row[17] + ""","""  + Row[18] +  """" target="_blank" title="View location map"><img src="static/images/location.png" style="height:20px;"/></a></td>""" if (Row[17]!='') and (Row[17]!=None) and (Row[18]!='') and (Row[18]!=None) else """<td style="text-align:center;">-</td>

                
                </tr>
                
                """
                out = out + "\n" + one_loop + "\n"  
        else:
            out = """
            <tr>
            <td colspan="15" style="text-align:center;">No records found</td>
            </tr>
            
            """
        #data.append(out)
        #return out
        
        file = open('C:/Sites/Neo_Skills_UAT/templates/TMA-Report/tma_session-old.html').read().split('abcdefghijklmnopqrstuvwxy')
        htmlpage = file[0] + out +file[1]
        file = open('C:/Sites/Neo_Skills_UAT/templates/TMA-Report/tma_session.html', 'w')
        file.write(htmlpage)
        file.close()

        if g.user:
            return render_template("home.html", values=g.User_detail_with_ids,html="tma_session_page")
        else:
            return render_template("login.html",error="Session Time Out!!")
    except Exception as e:
        #return render_template("home.html", values=g.User_detail_with_ids,html="html error",data='error data')
        #return redirect(url_for('home'))
        return 'Hi ' + str(e)
           



#################################################################################################################################
#MCL REPORT PAGE
@app.route("/mcl_report_page")
def mcl_report_page():
    if g.user:
        return render_template("MCL-Report/mcl_report_download.html")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/mcl_report")
def mcl_report():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="mcl_report_page")
    else:
        return render_template("login.html",error="Session Time Out!!")


@app.route('/download_func',methods=['GET', 'POST'])
def mcl_user_download():
    try:
        
        practice = request.form["PraticeId"]
        
        course = request.form["CourseId"]
        
        date_from = request.form["FromDate"]
        date_from = datetime.strptime(date_from, '%Y-%m-%d').strftime('%m/%d/%Y')
        
        date_to = request.form["ToDate"]
        date_to = datetime.strptime(date_to, '%Y-%m-%d').strftime('%m/%d/%Y')
        
        csv_excel = request.form["customRadio"]
        
        user_id = g.user_id

        #print(user_id, practice, course, date_from, date_to,csv_excel)
        #return (date_from + '   ' + date_to + '   ' + csv_excel + str(user_id))
        
        f=open(config.neo_report_file_path+'audit_report.txt','a', encoding='utf-8')
        f.write('{}|{}|{}|{}|{}|\n'.format('Download',str(user_id),practice,course,str(datetime.now())))
        f.close()
        #return(str(datetime.now()))
        for i in os.listdir(config.neo_report_file_path)[1:]:
            os.remove(config.neo_report_file_path + i)

	
        #return str(user_id) + practice + course + date_from + date_to + csv_excel
        data = Database.report_table_db(user_id, practice, course, date_from, date_to)
        #return(str(datetime.now()))
        report_name = "MCL_REPORT_"+datetime.now().strftime('%Y-%m-%d %H_%M_%S')
        """
        
        """
        
        try:

            tma_path = config.neo_report_file_path

            if csv_excel == 'csv':
                path = tma_path + '{}.csv'.format(report_name)
                res = MCL_updated_report.create_report(data, path)
                
                

            else:
                path = tma_path + '{}.xlsx'.format(report_name)
                res = MCL_updated_report.create_report(data, path)
            
            if res['Status']:
                return send_file(path, as_attachment=True)
            else:
                return res['Description']
            
        except Exception as e:
            return str(e)

    
        
        return send_file(path, as_attachment=True)
        #return render_template("result.html")
    except Exception as e:

        return(str(e))
    
        return render_template("index.html")


class practicebasedonuser(Resource):
    @staticmethod
    def get():
        return Database.practicebasedonuser(g.user_id)

class CourseBasedOnUserPractice(Resource):
    @staticmethod
    def post():
        practice_id = request.form['PracticeId']
        return Database.CourseBasedOnUserPractice(g.user_id,practice_id)

api.add_resource(practicebasedonuser,'/PracticeBasedOnUser')
api.add_resource(CourseBasedOnUserPractice,'/CourseBasedOnUserPractice')


############################################################################################################

#Section_API's
@app.route("/section_list_page")
def section_list_page():
    if g.user:
        return render_template("Content/section-list.html")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/section")
def section():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="section_list_page")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/section_add_edit")
def section_add_edit():
    if g.user:
        return render_template("Content/section-add-edit.html",section_id=g.section_id)
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/assign_section_add_edit_to_home", methods=['GET','POST'])
def assign_section_add_edit_to_home():
    session['section_id']=request.form['hdn_section_id']
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="section_add_edit")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/after_popup_section")
def after_popup_section():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="section")
    else:
        return render_template("login.html",error="Session Time Out!!")

class section_list(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            section_id = request.form['section_id'] 
            start_index = request.form['start']
            page_length = request.form['length']
            search_value = request.form['search[value]']
            order_by_column_position = request.form['order[0][column]']
            order_by_column_direction = request.form['order[0][dir]']
            draw=request.form['draw']
            return Content.section_list(section_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)

class add_section_details(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            section_name=request.form['SectionName']
            section_type_id=request.form['SectionType']
            p_section=request.form['P_Section']
            user_id=g.user_id
            is_active=request.form['isactive']
            section_id=g.section_id
            return Content.add_section(section_name,section_type_id,p_section,user_id,is_active,section_id)

class get_section_details(Resource):
    @staticmethod
    def get():
        if request.method == 'GET':
            return Content.get_section(g.section_id)
        
class all_section_types(Resource):
    @staticmethod
    def get():
        if request.method == 'GET':
            return Content.all_section_types()

class all_parent_section(Resource):
    @staticmethod
    def get():
        if request.method == 'GET':
            return Content.all_parent_section()

api.add_resource(section_list,'/section_list')
api.add_resource(add_section_details,'/add_section_details')
api.add_resource(get_section_details,'/GetSectionDetails')
api.add_resource(all_section_types,'/AllSectionTypeList')
api.add_resource(all_parent_section,'/AllP_SectionList')


############################################################################################################

#State_and_District_API's
# @app.route("/state_and_district_page")
# def state_and_district_page():
#     if g.user:
#         return render_template("MCL/Master/state_and_district-list.html")
#     else:
#         return render_template("login.html",error="Session Time Out!!")

# @app.route("/state_and_district")
# def state_and_district():
#     if g.user:
#         return render_template("home.html",values=g.User_detail_with_ids,html="state_and_district_page")
#     else:
#         return render_template("login.html",error="Session Time Out!!")

# @app.route("/state_and_district_add_edit")
# def state_and_district_add_edit():
#     if g.user:
#         return render_template("MCL/Master/state_and_district-add-edit.html",state_id=g.state_id)
#     else:
#         return render_template("login.html",error="Session Time Out!!")

# @app.route("/assign_state_and_district_add_edit_to_home", methods=['GET','POST'])
# def assign_state_and_district_add_edit_to_home():
#     session['state_id']=request.form['hdn_state_id']
#     if g.user:
#         return render_template("home.html",values=g.User_detail_with_ids,html="state_and_district_add_edit")
#     else:
#         return render_template("login.html",error="Session Time Out!!")

# @app.route("/after_popup_state_and_district")
# def after_popup_state_and_district():
#     if g.user:
#         return render_template("home.html",values=g.User_detail_with_ids,html="state_and_district")
#     else:
#         return render_template("login.html",error="Session Time Out!!")


# class state_and_district_list(Resource):
#     @staticmethod
#     def post():
#         if request.method == 'POST':
#             state_id = request.form['state_id'] 
#             start_index = request.form['start']
#             page_length = request.form['length']
#             search_value = request.form['search[value]']
#             order_by_column_position = request.form['order[0][column]']
#             order_by_column_direction = request.form['order[0][dir]']
#             draw=request.form['draw']
#             return Content.section_list(state_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)


# api.add_resource(state_and_district_list,'/state_and_district_list')


############################################################################################################

@app.route("/assign_parent_center_id_for_sub_center", methods=['GET','POST'] )
def assign_parent_center_id_for_sub_center():
    if request.method == 'POST':
        session['parent_center_id']=request.form['hdn_center_id']
        return redirect('/sub_center')

#Sub_center_API's
@app.route("/sub_center_list_page")
def sub_center_list_page():
    if g.user:
        return render_template("Master/sub_center-list.html")
    else:
        return render_template("login.html",error="Session Time Out!!")


@app.route("/sub_center")
def sub_center():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="sub_center_list_page")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/sub_center_add_edit")
def sub_center_add_edit():
    if g.user:
        return render_template("Master/sub_center-add-edit.html",sub_center_id=g.sub_center_id)
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/assign_sub_center_add_edit_to_home", methods=['GET','POST'])
def assign_sub_center_add_edit_to_home():
    session['sub_center_id']=request.form['hdn_sub_center_id']
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="sub_center_add_edit")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/after_popup_sub_center")
def after_popup_sub_center():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="sub_center")
    else:
        return render_template("login.html",error="Session Time Out!!")

class sub_center_list(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            sub_center_id = request.form['sub_center_id'] 
            parent_center_id = g.parent_center_id
            start_index = request.form['start']
            page_length = request.form['length']
            search_value = request.form['search[value]']
            order_by_column_position = request.form['order[0][column]']
            order_by_column_direction = request.form['order[0][dir]']
            draw=request.form['draw']
            return Master.sub_center_list(sub_center_id,parent_center_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)

class add_sub_center_details(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            sub_center_name=request.form['SubCenterName']
            sub_center_loc=request.form['SubCenterLoc']
            parent_center_id=g.parent_center_id
            user_id=g.user_id
            is_active=request.form['isactive']
            sub_center_id=g.sub_center_id
            return Master.add_sub_center(sub_center_name,sub_center_loc,parent_center_id,user_id,is_active,sub_center_id)

class get_sub_center_details(Resource):
    @staticmethod
    def get():
        if request.method == 'GET':
            return Master.get_sub_center(
                
            )

api.add_resource(sub_center_list,'/sub_center_list')
api.add_resource(add_sub_center_details,'/add_sub_center_details')
api.add_resource(get_sub_center_details,'/GetSubCenterDetails')

######################################################################################################

#Map_session_course_API's
@app.route("/assign_course_id_for_session", methods=['GET', 'POST'])
def assign_course_id_for_session():
    if request.method == 'POST':
        session['session_course_id']=request.form['hdn_course_id']
        return redirect('/session_course')


#Sub_center_API's
@app.route("/session_course_list_page")
def session_course_list_page():
    if g.user:
        return render_template("Content/session_course-list.html")
    else:
        return render_template("login.html",error="Session Time Out!!")


@app.route("/session_course")
def session_course():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="session_course_list_page")
    else:
        return render_template("login.html",error="Session Time Out!!")


class all_session_plan(Resource):
    @staticmethod
    def get():
        if request.method == 'GET':
            return Content.all_session_plan(g.session_course_id)

class all_module(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            session_plan_id=request.form['session_plan_id']
            return Content.all_module(session_plan_id)

class module_session_list(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            session_id = request.form['session_id'] 
            module_id = request.form['module_id']
            start_index = request.form['start']
            page_length = request.form['length']
            search_value = request.form['search[value]']
            order_by_column_position = request.form['order[0][column]']
            order_by_column_direction = request.form['order[0][dir]']
            draw=request.form['draw']
            return Content.module_session_list(session_id,module_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)

class add_session_plan_details(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            session_plan_name=request.form['SessionPlanName']
            session_plan_duration = request.form['SessionPlanDuration']
            course_id=g.session_course_id
            user_id=g.user_id
            is_active=request.form['isactive']
            session_plan_id='0'
            return Content.add_session_plan(session_plan_name,session_plan_duration,course_id,user_id,is_active,session_plan_id)

class add_module_details(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            module_name=request.form['ModuleName']
            module_code = request.form['ModuleCode']
            module_order = request.form['ModuleOrder']
            session_plan_id= request.form['SessionPlanId']
            user_id=g.user_id
            is_active=request.form['isactive']
            module_id='0'
            return Content.add_module(module_name,module_code,module_order,session_plan_id,user_id,is_active,module_id)

class get_session_order_for_module(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            module_id=request.form['module_id']
            return Content.get_session_order_for_module(module_id)

class add_edit_session_details(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            session_name=request.form['SessionName']
            session_code = request.form['SessionCode']
            session_order = request.form['SessionOrder']
            module_id= request.form['ModuleId']
            session_des = request.form['SessionDescription']
            learning_out = request.form['LearningOutcome']
            learning_act = request.form['LearningAct']
            learning_aids = request.form['LearningAids']
            user_id=g.user_id
            is_active=request.form['isactive']
            session_id = request.form['SessionId']
            session_duration = request.form['SessionDuration']
            print(session_name,session_code,session_order,module_id,session_des,learning_out,learning_act,learning_aids,user_id,is_active,session_id,session_duration)
            return Content.add_edit_session(session_name,session_code,session_order,module_id,session_des,learning_out,learning_act,learning_aids,user_id,is_active,session_id,session_duration)
            
class GetSessionDetails(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            session_id = request.form['session_id']
            print(session_id)
            return Content.get_session_detail(session_id)

api.add_resource(all_session_plan,'/AllSessionPlanList')
api.add_resource(all_module,'/AllModuleList')
api.add_resource(module_session_list,'/module_session_list')
api.add_resource(add_session_plan_details,'/add_session_plan_details')
api.add_resource(add_module_details,'/add_module_details')
api.add_resource(get_session_order_for_module,'/get_session_order_for_module')
api.add_resource(add_edit_session_details,'/add_edit_session_details')
api.add_resource(GetSessionDetails,'/GetSessionDetails')


#####################################################################################################
#Project_API's
@app.route("/project_list_page")
def project_list_page():
    if g.user:
        status=request.args.get('status',-1,type=int)
        return render_template("Master/project-list.html", status=status)
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/project")
def project():
    if g.user:
        status=request.args.get('status',-1,type=int) 
        html_str="project_list_page?status=" + str(status)
        return render_template("home.html",values=g.User_detail_with_ids,html=html_str)
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/project_add_edit")
def project_add_edit():
    if g.user:
        return render_template("Master/project-add-edit.html",project_id=g.project_id)
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/assign_project_add_edit_to_home", methods=['GET','POST'])
def assign_project_add_edit_to_home():
    session['project_id']=request.form['hdn_project_id']
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="project_add_edit")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/after_popup_project")
def after_popup_project():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="project")
    else:
        return render_template("login.html",error="Session Time Out!!")

####################  API  #######################
class project_list(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            entity = request.form['entity']
            customer = request.form['customer']
            p_group = request.form['p_group']
            block = request.form['block']
            practice = request.form['practice']
            bu = request.form['bu']
            product = request.form['product']
            status = request.form['status']
            
            user_id = request.form['user_id']
            user_role_id = request.form['user_role_id'] 
            user_region_id = request.form['user_region_id']
            start_index = request.form['start']
            page_length = request.form['length']
            search_value = request.form['search[value]']
            order_by_column_position = request.form['order[0][column]']
            order_by_column_direction = request.form['order[0][dir]']
            draw=request.form['draw']
            print(user_id,user_role_id,user_region_id,entity,customer,p_group,block,practice,bu,product,status)
            return Master.project_list(user_id,user_role_id,user_region_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw,entity,customer,p_group,block,practice,bu,product,status)

class add_project_details(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            ProjectName=request.form['ProjectName']
            ProjectCode=request.form['ProjectCode']
            ClientName=request.form['ClientName']
            ContractName=request.form['ContractName']
            Practice=request.form['Practice']
            BU=request.form['BU']
            projectgroup=request.form['projectgroup']
            ProjectType=request.form['ProjectType']
            Block=request.form['Block']
            Product=request.form['Product']
            PlannedStartDate=request.form['PlannedStartDate']
            PlannedEndDate=request.form['PlannedEndDate']
            ActualStartDate=request.form['ActualStartDate']
            ActualEndDate=request.form['ActualEndDate']
            ProjectManager=request.form['ProjectManager']
            
            
            user_id=g.user_id
            project_id=g.project_id
            isactive=request.form['isactive']
            return Master.add_project_details(ProjectName, ProjectCode, ClientName, ContractName, Practice, BU, projectgroup, ProjectType, Block, Product, ProjectManager, ActualEndDate, ActualStartDate, PlannedEndDate, PlannedStartDate, isactive, project_id, user_id)
                    
class client_all(Resource):
    @staticmethod
    def get():
        if request.method == 'GET':
            user_id=request.args.get('user_id',0,type=int)
            user_role_id=request.args.get('user_role_id',0,type=int)
            return Master.all_client(user_id,user_role_id)

class get_project_details(Resource):
    @staticmethod
    def get():
        if request.method == 'GET':
            return Master.get_project_details(g.project_id)

class get_subproject_details(Resource):
    @staticmethod
    def get():
        if request.method == 'GET':
            return Master.get_subproject_details(g.subproject_id)


api.add_resource(project_list, '/project_list')
api.add_resource(client_all, '/GetALLClient')
api.add_resource(add_project_details, '/add_project_details')
api.add_resource(get_project_details, '/GetProjectDetails')
api.add_resource(get_subproject_details, '/get_subproject_details')

####################################################################################################

############################################################################################################
#MCL_Center_wise_count_report_API's
@app.route("/mcl_center_wise_count_report_page")
def mcl_center_wise_count_report_page():
    if g.user:
        return render_template("MCL-Report/mcl_center_wise_count_report_download.html")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/mcl_center_wise_count_report")
def mcl_center_wise_count_report():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="mcl_center_wise_count_report_page")
    else:
        return render_template("login.html",error="Session Time Out!!")


class preview_center_count(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            course = request.form["course_id"]
            start_index = request.form['start']
            page_length = request.form['length']
            search_value = request.form['search[value]']
            order_by_column_position = request.form['order[0][column]']
            order_by_column_direction = request.form['order[0][dir]']
            draw = request.form["draw"]
            print("hello"+course)
            return Database.preview_center_count(course,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)

api.add_resource(preview_center_count,'/Preview_Center_Count')
############################################################################################################

#Trainer's
@app.route("/trainer_list_page")
def trainer_list_page():
    if g.user:
        if int(g.user_role) in [11,12,13,14,18]:
            return render_template("User_Management/trainer-view-list.html")
        else:
            return render_template("User_Management/trainer-list.html")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/trainer")
def trainer():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="trainer_list_page")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/trainer_add_edit")
def trainer_add_edit():
    if g.user:
        return render_template("User_Management/trainer-add-edit.html",user_id=g.web_user_id)
    else:
        return render_template("login.html",error="Session Time Out!!")
    


@app.route("/assign_trainer_add_edit_to_home", methods=['GET','POST'])
def assign_trainer_add_edit_to_home():
    session['web_user_id']=request.form['hdn_user_id']
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="trainer_add_edit")
    else:
        return render_template("login.html",error="Session Time Out!!")



@app.route("/after_popup_trainer")
def after_popup_trainer():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="trainer")
    else:
        return render_template("login.html",error="Session Time Out!!")


class trainer_list(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            user_id = request.form['user_id']
            user_region_id=0
            if 'user_region_id' in request.form:
                user_region_id = request.form['user_region_id']
            
            start_index = request.form['start']
            page_length = request.form['length']
            search_value = request.form['search[value]']
            order_by_column_position = request.form['order[0][column]']
            order_by_column_direction = request.form['order[0][dir]']
            draw=request.form['draw']
            user_role_id=request.form['user_role_id']
            centers=request.form['centers']
            status=request.form['status']
            Region_id = request.form['Region_id']
            Cluster_id = request.form['Cluster_id']
            Dept = request.form['Dept']
            entity_ids= request.form['entity_ids']
            project_ids= request.form['project_ids']
            sector_ids= request.form['sector_ids']
            return UsersM.trainer_list(user_id,user_region_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw,user_role_id, centers, status, Region_id, Cluster_id, Dept,entity_ids,project_ids,sector_ids)

api.add_resource(trainer_list, '/trainer_list')


api.add_resource(course_api.AllClusterList, '/AllClusterList')
api.add_resource(course_api.AllRegionList, '/AllRegionList')
api.add_resource(course_api.AllProjectList, '/AllProjectList')


#########################################TMA REPORT###################################################################


@app.route("/trainer_deployment")
def trainer_deployment_page():
    if g.user:
        return render_template("TMA-Report/report-trainer-deployment.html")
    else:
        return redirect("/")

@app.route("/TrainerDeployment")
def TrainerDeployment():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="trainer_deployment")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/attendance_report")
def attendance_report_page():
    if g.user:
        return render_template("TMA-Report/report-attendance.html")
    else:
        return redirect("/")

@app.route("/AttendanceReport")
def AttendanceReport():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="attendance_report")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/BatchSessions" ,methods=['GET','POST'])
def BatchSessions():
    if g.user:
        Batch = request.args['Batch'] if (request.args['Batch']!=None) and (request.args['Batch']!='') else '0'
        Course = request.args['Course'] if (request.args['Course']!=None) and (request.args['Course']!='') else '0'
                        
        data=[Batch, Course]
        session['Batch_Sessions']=data
        return render_template("home.html",values=g.User_detail_with_ids,html="batch_sessions")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/batch_sessions")
def batch_sessions_page():
    if g.user:
        
        return render_template("TMA-Report/report-batch-sessions.html", data=g.Batch_Sessions)
    else:
        return redirect("/")

@app.route("/mobilization_report")
def mobilization_report_page():
    if g.user:
        return render_template("MCL-Report/report-mobilization.html")
    else:
        return redirect("/")

@app.route("/MobilizationReport")
def MobilizationReport():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="mobilization_report")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/RegisteredCandidatesList" ,methods=['GET','POST'])
def RegisteredCandidatesList():
    if g.user:
        Center = request.args['Center'] if (request.args['Center']!=None) and (request.args['Center']!='') else '0'
        Course = request.args['Course'] if (request.args['Course']!=None) and (request.args['Course']!='') else '0'
        Mobilizer=  request.args['Mobilizer'] if (request.args['Mobilizer']!=None) and (request.args['Mobilizer']!='') else '0'              
        CenterName=  request.args['CenterName'] if (request.args['CenterName']!=None) and (request.args['CenterName']!='') else 'NA'              
        CourseName=  request.args['CourseName'] if (request.args['CourseName']!=None) and (request.args['CourseName']!='') else 'NA'              
        
        data=[Center, Course, Mobilizer,CenterName,CourseName]
        session['RegisteredCandidatesList']=data
        return render_template("home.html",values=g.User_detail_with_ids,html="registered_candidates_list")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/registered_candidates_list")
def registered_candidates_list_page():
    if g.user:        
        return render_template("MCL-Report/report-reg-candidates.html", data=g.RegisteredCandidatesList)
    else:
        return redirect("/")

#################################################################################################
class AllRegionsBasedOnUser(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            response=[]
            try:
                UserId=request.args.get('user_id',0,type=int)
                UserRoleId=request.args.get('user_role_id',0,type=int)
                UserRegionId=request.args.get('user_region_id',0,type=int)
                response=Report.AllRegionsBasedOnUser(UserId,UserRoleId,UserRegionId)
                return {'Regions':response}
            except Exception as e:
                return {'exception':str(e)}

api.add_resource(AllRegionsBasedOnUser,'/AllRegionsBasedOnUser')

class GetAllCentersBasedOnRegion_User(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            response=[]
            try:
                UserId=request.args.get('user_id',0,type=int)
                UserRoleId=request.args.get('user_role_id',0,type=int)
                RegionId=request.args.get('region_id','',type=str)
                print(UserId,UserRoleId,RegionId)
                response=Report.GetAllCentersBasedOnRegion_User(UserId,UserRoleId,RegionId)
                return {'Centers':response}
            except Exception as e:
                return {'exception':str(e)} 

api.add_resource(GetAllCentersBasedOnRegion_User,'/GetAllCentersBasedOnRegion_User')

class GetAllCoursesBasedOnCenter_User(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            response=[]
            try:
                UserId=request.args.get('user_id',0,type=int)
                UserRoleId=request.args.get('user_role_id',0,type=int)
                CenterId=request.args.get('center_id',0,type=int)
                response=Report.GetAllCoursesBasedOnCenter_User(UserId,UserRoleId,CenterId)
                return {'Courses':response}
            except Exception as e:
                return {'exception':str(e)} 

api.add_resource(GetAllCoursesBasedOnCenter_User,'/GetAllCoursesBasedOnCenter_User')

class GetAllTrainersBasedOnCenter_User(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            response=[]
            try:
                UserId=request.args.get('user_id',0,type=int)
                UserRoleId=request.args.get('user_role_id',0,type=int)
                CenterId=request.args.get('center_id',0,type=int)
                response=Report.GetAllTrainersBasedOnCenter_User(UserId,UserRoleId,CenterId)
                return {'Trainers':response}
            except Exception as e:
                return {'exception':str(e)} 

api.add_resource(GetAllTrainersBasedOnCenter_User,'/GetAllTrainersBasedOnCenter_User')

class GetAllMobilizersBasedOnCenter_User(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            response=[]
            try:
                UserId=request.args.get('user_id',0,type=int)
                UserRoleId=request.args.get('user_role_id',0,type=int)
                CenterId=request.args.get('center_id',0,type=int)
                response=Report.GetAllMobilizersBasedOnCenter_User(UserId,UserRoleId,CenterId)
                return {'Mobilizers':response}
            except Exception as e:
                return {'exception':str(e)} 

api.add_resource(GetAllMobilizersBasedOnCenter_User,'/GetAllMobilizersBasedOnCenter_User')

class TrainerDeploymentBatches(Resource):
    @staticmethod
    def post():
        if request.method=='POST':
            try:
                region_id = request.form['region_id']
                center_id =request.form['center_id']
                course_ids = request.form['course_ids']
                trainer_ids =request.form['trainer_ids']
                from_date =request.form['from_date']
                to_date = request.form['to_date']
                batch_stage_id = request.form['batch_stage_id']
                '''start_index=0
                page_length = '10'
                search_value = ''
                order_by_column_position =0 
                order_by_column_direction = 'asc'
                draw=0'''
                if 'start' in request.form:
                    start_index = request.form['start']
                if 'length' in request.form:
                    page_length = request.form['length']
                if 'search[value]' in request.form:
                    search_value = request.form['search[value]']
                if 'order[0][column]' in request.form:
                    order_by_column_position = request.form['order[0][column]']
                if 'order[0][dir]' in request.form:
                    order_by_column_direction = request.form['order[0][dir]']
                if 'draw' in request.form:
                    draw = request.form['draw']
                
                
                print(region_id,center_id,course_ids,trainer_ids,from_date,to_date,batch_stage_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)
                response=Report.TrainerDeploymentBatches(region_id,center_id,course_ids,trainer_ids,from_date,to_date,batch_stage_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)
                #print(response)
                return response
            except Exception as e:
                print(str(e))
                return {"exceptione":str(e)}

api.add_resource(TrainerDeploymentBatches,'/trainer_deployment_batches')

class ReportAttendanceBatches(Resource):
    @staticmethod
    def post():
        if request.method=='POST':
            try:
                region_id = request.form['region_id']
                center_id =request.form['center_id']
                course_ids = request.form['course_ids']
                trainer_ids =request.form['trainer_ids']
                from_date =request.form['from_date']
                to_date = request.form['to_date']
                batch_stage_id = request.form['batch_stage_id']
                if 'start' in request.form:
                    start_index = request.form['start']
                if 'length' in request.form:
                    page_length = request.form['length']
                if 'search[value]' in request.form:
                    search_value = request.form['search[value]']
                if 'order[0][column]' in request.form:
                    order_by_column_position = request.form['order[0][column]']
                if 'order[0][dir]' in request.form:
                    order_by_column_direction = request.form['order[0][dir]']
                if 'draw' in request.form:
                    draw = request.form['draw']
                print(region_id,center_id,course_ids,trainer_ids,from_date,to_date,batch_stage_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)
                response=Report.ReportAttendanceBatches(region_id,center_id,course_ids,trainer_ids,from_date,to_date,batch_stage_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)
                
                return response
            except Exception as e:
                print(str(e))
                return {"exceptione":str(e)}

api.add_resource(ReportAttendanceBatches,'/report_attendance_batches')

class ReportBatchSession(Resource):
    @staticmethod
    def post():
        if request.method=='POST':
            try:
                batch_id = request.form['batch_id']
                course_id =request.form['course_id']
                if 'start' in request.form:
                    start_index = request.form['start']
                if 'length' in request.form:
                    page_length = request.form['length']
                if 'search[value]' in request.form:
                    search_value = request.form['search[value]']
                if 'order[0][column]' in request.form:
                    order_by_column_position = request.form['order[0][column]']
                if 'order[0][dir]' in request.form:
                    order_by_column_direction = request.form['order[0][dir]']
                if 'draw' in request.form:
                    draw = request.form['draw']
                print(batch_id,course_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)
                response=Report.ReportBatchSession(batch_id,course_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)
                
                return response
            except Exception as e:
                print(str(e))
                return {"exceptione":str(e)}
api.add_resource(ReportBatchSession,'/report_batch_session')

class GetBatchDetailsForAttReport(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            batch_id=request.args.get('batch_id',0,type=int)
            response={"BatchDetails":Report.GetBatchDetailsForAttReport(batch_id)}
            return response

api.add_resource(GetBatchDetailsForAttReport,'/get_batch_details_for_att_report')

class GetSessionTrainerActivity(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            batch_id=request.args.get('batch_id',0,type=int)
            session_id=request.args.get('session_id',0,type=int)
            response={"TrainerActivity":Report.GetSessionTrainerActivity(batch_id,session_id),"TMAStageLogImagePath":config.tma_stage_log_image_path}
            return response
api.add_resource(GetSessionTrainerActivity,'/GetSessionTrainerActivity')

class GetCandidateSessionAttendance(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            batch_id=request.args.get('batch_id',0,type=int)
            session_id=request.args.get('session_id',0,type=int)
            attendance_type=request.args.get('attendance_type',0,type=int)
            GrpAttendance=[]
            if attendance_type==1:
                GrpAttendance=Report.GetCandidateGrpAttendance(batch_id,session_id)
            response={"CandidateAttendance":Report.GetCandidateSessionAttendance(batch_id,session_id),"GroupAttendance":GrpAttendance,"TMACandidateImagePath":config.tma_candidate_image_path}
            return response
api.add_resource(GetCandidateSessionAttendance,'/GetCandidateSessionAttendance')

class GetMobilizationReportData(Resource):
    @staticmethod
    def post():
        if request.method=='POST':
            try:
                region_id = request.form['region_id']
                center_id =request.form['center_id']
                course_ids = request.form['course_ids']
                mobilizer_ids =request.form['mobilizer_ids']
                if 'start' in request.form:
                    start_index = request.form['start']
                if 'length' in request.form:
                    page_length = request.form['length']
                if 'search[value]' in request.form:
                    search_value = request.form['search[value]']
                if 'order[0][column]' in request.form:
                    order_by_column_position = request.form['order[0][column]']
                if 'order[0][dir]' in request.form:
                    order_by_column_direction = request.form['order[0][dir]']
                if 'draw' in request.form:
                    draw = request.form['draw']
                response=Report.GetMobilizationReportData(region_id,center_id,course_ids,mobilizer_ids,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)
                #print(response)
                return response
            except Exception as e:
                print(str(e))
                return {"exceptione":str(e)}

api.add_resource(GetMobilizationReportData,'/GetMobilizationReportData')

class GetRegisteredCandidatesList(Resource):
    @staticmethod
    def post():
        if request.method=='POST':
            try:
                center_id = request.form['center_id']
                course_id =request.form['course_id']
                mobilizer_id=request.form['mobilizer_id']
                if 'start' in request.form:
                    start_index = request.form['start']
                if 'length' in request.form:
                    page_length = request.form['length']
                if 'search[value]' in request.form:
                    search_value = request.form['search[value]']
                if 'order[0][column]' in request.form:
                    order_by_column_position = request.form['order[0][column]']
                if 'order[0][dir]' in request.form:
                    order_by_column_direction = request.form['order[0][dir]']
                if 'draw' in request.form:
                    draw = request.form['draw']
                response=Report.GetRegisteredCandidatesList(center_id,course_id,mobilizer_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)
                
                return response
            except Exception as e:
                print(str(e))
                return {"exceptione":str(e)}

api.add_resource(GetRegisteredCandidatesList,'/GetRegisteredCandidatesList')

class GetCandidateBasicDetails(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            candidate_id=request.args.get('candidate_id',0,type=int)
            response={"CandidateDetails":Report.GetCandidateBasicDetails(candidate_id)}
            return response

api.add_resource(GetCandidateBasicDetails,'/GetCandidateBasicDetails')
############################################################################################################
@app.route("/forget_password")
def forget_password():
    return render_template('recoverpw.html')

class recover_pass(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            reco_email = request.args['reco_email']
            
            data = Database.recover_pass_db(reco_email)
            if len(data)>0:
                res = sent_mail.forget_password(reco_email,data[0][1],data[0][3] + ' ' + data[0][4])
                if res['status']:
                    msg = {"message":res['description'], "title":'Sucess',"UserId":data[0][0]}
                else:
                    msg = {"message":res['description'], "title":'Unable to sent',"UserId":data[0][0]}
            else:
                msg = {"message":'Please check email or contact to admin',"title":'Invalid Email',"UserId":0}

            response={"PopupMessage":msg}
            return response

api.add_resource(recover_pass,'/recover_pass')

@app.route("/change_password_page")
def change_password_page():
    return render_template('change_password.html')

@app.route("/change_password")
def change_password():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="change_password_page")
    else:
        return render_template("login.html",error="Session Time Out!!")

class change_password_api(Resource):
    @staticmethod
    def post():
        if request.method=='POST':
            try:
                old_password = request.form['old_password']
                new_password = request.form['new_password']
                user_id = g.user_id

                print(old_password, new_password, user_id)


                message = Database.change_password_api_db(old_password, new_password, user_id)
                return {'PopupMessage':message}
                

            except Exception as e:
                
                print(str(e))
                return {"exceptione":str(e)}

api.add_resource(change_password_api,'/change_password_api')

#########################################Compliance Reports###################################################################
@app.route("/data/<path:path>")
def get_file(path):
    """Download a file."""
    filename = r"{}{}".format(config.ReportDownloadPathLocal,path)
    print(filename)
    if not(os.path.exists(filename)):
        filename = r"{}No-image-found.jpg".format(config.ReportDownloadPathWeb)
    return send_file(filename)

@app.route("/tma_registration")
def tma_registration_page():
    if g.user:
        return render_template("Compliance-Report/TMA-Registraion.html")
    else:
        return redirect("/")

@app.route("/TMARegistration")
def TMARegistration():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="tma_registration")
    else:
        return render_template("login.html",error="Session Time Out!!")


@app.route("/trainerwise_tma_registration")
def trainerwise_tma_registration_page():
    if g.user:
        return render_template("Compliance-Report/TrainerWise-TMA-Registraion.html")
    else:
        return redirect("/")

@app.route("/TrainerwiseTMARegistration")
def TrainerwiseTMARegistration():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="trainerwise_tma_registration")
    else:
        return render_template("login.html",error="Session Time Out!!")


class GetAllClustersBasedOnMultipleRegion_User(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            response=[]
            try:
                UserId=request.args.get('user_id',0,type=int)
                UserRoleId=request.args.get('user_role_id',0,type=int)
                RegionIds=request.args.get('region_id','',type=str)
                response=Report.GetAllClustersBasedOnMultipleRegion_User(UserId,UserRoleId,RegionIds)
                return {'Clusters':response}
            except Exception as e:
                return {'exception':str(e)} 

api.add_resource(GetAllClustersBasedOnMultipleRegion_User,'/GetAllClustersBasedOnMultipleRegion_User')

class GetAllCentersBasedOnMultipleClusters_User(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            response=[]
            try:
                UserId=request.args.get('user_id',0,type=int)
                UserRoleId=request.args.get('user_role_id',0,type=int)
                ClusterIds=request.args.get('cluster_id','',type=str)
                response=Report.GetAllCentersBasedOnMultipleClusters_User(UserId,UserRoleId,ClusterIds)
                return {'Centers':response}
            except Exception as e:
                return {'exception':str(e)} 

api.add_resource(GetAllCentersBasedOnMultipleClusters_User,'/GetAllCentersBasedOnMultipleClusters_User')

class GetAllCoursesBasedOnMultipleCenters_User(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            response=[]
            try:
                UserId=request.args.get('user_id',0,type=int)
                UserRoleId=request.args.get('user_role_id',0,type=int)
                CenterIds=request.args.get('center_id','',type=str)
                response=Report.GetAllCoursesBasedOnMultipleCenters_User(UserId,UserRoleId,CenterIds)
                return {'Courses':response}
            except Exception as e:
                return {'exception':str(e)} 

api.add_resource(GetAllCoursesBasedOnMultipleCenters_User,'/GetAllCoursesBasedOnMultipleCenters_User')

class GetAllCooBasedOnMultipleRegions_User(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            response=[]
            try:
                UserId=request.args.get('user_id',0,type=int)
                UserRoleId=request.args.get('user_role_id',0,type=int)
                RegionIds=request.args.get('region_id','',type=str)
                response=Report.GetAllCooBasedOnMultipleRegions_User(UserId,UserRoleId,RegionIds)
                return {'Coo':response}
            except Exception as e:
                return {'exception':str(e)} 

api.add_resource(GetAllCooBasedOnMultipleRegions_User,'/GetAllCooBasedOnMultipleRegions_User')

class GetAllTmBasedOnMultipleClusters_User(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            response=[]
            try:
                UserId=request.args.get('user_id',0,type=int)
                UserRoleId=request.args.get('user_role_id',0,type=int)
                ClusterIds=request.args.get('cluster_id','',type=str)
                response=Report.GetAllTmBasedOnMultipleClusters_User(UserId,UserRoleId,ClusterIds)
                return {'TM':response}
            except Exception as e:
                return {'exception':str(e)} 

api.add_resource(GetAllTmBasedOnMultipleClusters_User,'/GetAllTmBasedOnMultipleClusters_User')

class tma_registration_compliance_report(Resource):
    @staticmethod
    def post():
        if request.method=='POST':
            try:
                region_id = request.form['region_id']
                cluster_id = request.form['cluster_id']
                center_id = request.form['center_id']
                course_id =request.form['course_id']
                center_type_id = request.form['center_type_id']
                tm = request.form['tm']
                coo = request.form['coo']
                if 'start' in request.form:
                    start_index = request.form['start']
                if 'length' in request.form:
                    page_length = request.form['length']
                if 'search[value]' in request.form:
                    search_value = request.form['search[value]']
                if 'order[0][column]' in request.form:
                    order_by_column_position = request.form['order[0][column]']
                if 'order[0][dir]' in request.form:
                    order_by_column_direction = request.form['order[0][dir]']
                if 'draw' in request.form:
                    draw = request.form['draw']
                #print(batch_id,course_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)
                response=Report.tma_registration_compliance_report(region_id,cluster_id,center_id,center_type_id,course_id,tm,coo,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)
                
                return response
            except Exception as e:
                print(str(e))
                return {"exceptione":str(e)}
api.add_resource(tma_registration_compliance_report,'/tma_registration_compliance_report')

class download_tma_registration_compliance_report(Resource):
    DownloadPath=config.ReportDownloadPathLocal
    report_name = "TMA_Registration_Compliance"+datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    @staticmethod
    def post():
        if request.method=='POST':
            try:
                region_id = request.form['region_id']
                cluster_id = request.form['cluster_id']
                center_id = request.form['center_id']
                course_id =request.form['course_id']
                center_type_id = request.form['center_type_id']
                tm = request.form['tm']
                coo = request.form['coo']
                r=re.compile("TMA_Registration_Compliance.*")
                lst=os.listdir(download_tma_registration_compliance_report.DownloadPath)
                newlist = list(filter(r.match, lst))
                for i in newlist:
                    os.remove( download_tma_registration_compliance_report.DownloadPath + i)
                path = '{}{}.xlsx'.format(download_tma_registration_compliance_report.DownloadPath,download_tma_registration_compliance_report.report_name)
                res=Report.download_tma_registration_compliance_report(region_id,cluster_id,center_id,center_type_id,course_id,tm,coo,path)
                print(download_tma_registration_compliance_report.report_name)
                print(path)
                ImagePath=config.ReportDownloadPathWeb
                #send_file(config.ReportDownloadPathLocal+download_tma_registration_compliance_report.report_name+'.xlsx')
                return {'FileName':download_tma_registration_compliance_report.report_name,'FilePath':ImagePath}
            except Exception as e:
                print(str(e))
                return {"exceptione":str(e)}
api.add_resource(download_tma_registration_compliance_report,'/download_tma_registration_compliance_report')

class trainerwise_tma_registration_compliance_report(Resource):
    @staticmethod
    def post():
        if request.method=='POST':
            try:
                region_id = request.form['region_id']
                cluster_id = request.form['cluster_id']
                center_id = request.form['center_id']
                course_id =request.form['course_id']
                center_type_id = request.form['center_type_id']
                tm = request.form['tm']
                coo = request.form['coo']
                if 'start' in request.form:
                    start_index = request.form['start']
                if 'length' in request.form:
                    page_length = request.form['length']
                if 'search[value]' in request.form:
                    search_value = request.form['search[value]']
                if 'order[0][column]' in request.form:
                    order_by_column_position = request.form['order[0][column]']
                if 'order[0][dir]' in request.form:
                    order_by_column_direction = request.form['order[0][dir]']
                if 'draw' in request.form:
                    draw = request.form['draw']
                #print(batch_id,course_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)
                response=Report.trainerwise_tma_registration_compliance_report(region_id,cluster_id,center_id,center_type_id,course_id,tm,coo,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)
                
                return response
            except Exception as e:
                print(str(e))
                return {"exceptione":str(e)}
api.add_resource(trainerwise_tma_registration_compliance_report,'/trainerwise_tma_registration_compliance_report')

class download_trainerwise_tma_registration_compliance_report(Resource):
    DownloadPath=config.ReportDownloadPathLocal
    report_name = "Trainerwise_TMA_Registration_Compliance"+datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    @staticmethod
    def post():
        if request.method=='POST':
            try:
                region_id = request.form['region_id']
                cluster_id = request.form['cluster_id']
                center_id = request.form['center_id']
                course_id =request.form['course_id']
                center_type_id = request.form['center_type_id']
                tm = request.form['tm']
                coo = request.form['coo']
                r=re.compile("Trainerwise_TMA_Registration_Compliance.*")
                lst=os.listdir(download_trainerwise_tma_registration_compliance_report.DownloadPath)
                newlist = list(filter(r.match, lst))
                for i in newlist:
                    os.remove( download_trainerwise_tma_registration_compliance_report.DownloadPath + i)
                path = '{}{}.xlsx'.format(download_trainerwise_tma_registration_compliance_report.DownloadPath,download_trainerwise_tma_registration_compliance_report.report_name)
                res=Report.download_trainerwise_tma_registration_compliance_report(region_id,cluster_id,center_id,center_type_id,course_id,tm,coo,path)
                #print(download_trainerwise_tma_registration_compliance_report.report_name)
                #print(path)
                ImagePath=config.ReportDownloadPathWeb
                return {'FileName':download_trainerwise_tma_registration_compliance_report.report_name,'FilePath':ImagePath}
            except Exception as e:
                print(str(e))
                return {"exceptione":str(e)}
api.add_resource(download_trainerwise_tma_registration_compliance_report,'/download_trainerwise_tma_registration_compliance_report')

######################################################################################################

#Sector_API's
@app.route("/sector_list_page")
def sector_list_page():
    if g.user:
        return render_template("Master/sector-list.html")
    else:
        return render_template("login.html",error="Session Time Out!!")


@app.route("/sector")
def sector():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="sector_list_page")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/sector_add_edit")
def sector_add_edit():
    if g.user:
        return render_template("Master/sector-add-edit.html",sector_id=g.sector_id)
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/assign_sector_add_edit_to_home", methods=['GET','POST'])
def assign_sector_add_edit_to_home():
    session['sector_id']=request.form['hdn_sector_id']
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="sector_add_edit")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/after_popup_sector")
def after_popup_sector():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="sector")
    else:
        return render_template("login.html",error="Session Time Out!!")

class sector_list(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            sector_id = request.form['sector_id'] 
            start_index = request.form['start']
            page_length = request.form['length']
            search_value = request.form['search[value]']
            order_by_column_position = request.form['order[0][column]']
            order_by_column_direction = request.form['order[0][dir]']
            draw=request.form['draw']
            print(order_by_column_position,order_by_column_direction)
            return Master.sector_list(sector_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)

class add_sector_details(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            sector_name=request.form['SectorName']
            sector_code=request.form['SectorCode']
            user_id=g.user_id
            is_active=request.form['isactive']
            sector_id=g.sector_id
            return Master.add_sector(sector_name,sector_code,user_id,is_active,sector_id)

class get_sector_details(Resource):
    @staticmethod
    def get():
        if request.method == 'GET':
            return Master.get_sector(g.sector_id)

api.add_resource(sector_list,'/sector_list')
api.add_resource(add_sector_details,'/add_sector_details')
api.add_resource(get_sector_details,'/GetSectorDetails')


####################################################################################################
#Contract_API's

@app.route("/contract_list_page")
def contract_list_page():
    if g.user:
        status=request.args.get('status',-1,type=int)
        return render_template("Master/contract-list.html", status=status)
    else:
        return render_template("login.html",error="Session Time Out!!")


@app.route("/contract")
def contract():
    if g.user:
        status=request.args.get('status',-1,type=int) 
        html_str="contract_list_page?status=" + str(status)
        return render_template("home.html",values=g.User_detail_with_ids,html=html_str)
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/contract_add_edit")
def contract_add_edit():
    if g.user:
        return render_template("Master/contract-add-edit.html", contract_id=g.contract_id )
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/assign_contract_add_edit_to_home", methods=['GET','POST'])
def assign_contract_add_edit_to_home():
    session['contract_id']=request.form['hdn_contract_id']
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="contract_add_edit")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/after_popup_contract")
def after_popup_contract():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="contract")
    else:
        return render_template("login.html",error="Session Time Out!!")

class contract_list(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            user_id=request.form['user_id']
            user_role_id=request.form['user_role_id']
            contract_id = request.form['contract_id'] 
            customer_ids = request.form['customer_ids'] 
            stage_ids = request.form['stage_ids'] 
            from_date = request.form['from_date'] 
            to_date = request.form['to_date'] 
            entity_ids = request.form['entity_ids'] 
            sales_category_ids = request.form['sales_category_ids'] 
            start_index = request.form['start']
            page_length = request.form['length']
            search_value = request.form['search[value]']
            order_by_column_position = request.form['order[0][column]']
            order_by_column_direction = request.form['order[0][dir]']
            draw=request.form['draw']
            return Master.contract_list(user_id,user_role_id,contract_id,customer_ids,stage_ids,from_date,to_date,entity_ids,sales_category_ids,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)

class add_contract_details(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            ContractName=request.form['ContractName']
            ContractCode=request.form['ContractCode']
            ClientName=request.form['ClientName']
            EntityName=request.form['EntityName']
            SalesCatergory=request.form['SalesCatergory']
            StartDate=request.form['StartDate']
            EndDate=request.form['EndDate']
            SalesManager=request.form['SalesManager']
            ContractValue=request.form['ContractValue']
            isactive=request.form['isactive']
            user_id=g.user_id
            contract_id=g.contract_id
            
            return Master.add_contract(ContractName, ContractCode, ClientName, EntityName, SalesCatergory, StartDate, EndDate, SalesManager, ContractValue, isactive, user_id, contract_id)

class get_contract_details(Resource):
    @staticmethod
    def get():
        if request.method == 'GET':
            return Master.get_contract(g.contract_id)

api.add_resource(contract_list,'/contract_list')
api.add_resource(add_contract_details,'/add_contract_details')
api.add_resource(get_contract_details,'/GetContractDetails')


####################################################################################################

class GetAllBusBasedOn_User(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            response=[]
            try:
                UserId=request.args.get('user_id',0,type=int)
                UserRoleId=request.args.get('user_role_id',0,type=int)
                response=Master.GetAllBusBasedOn_User(UserId,UserRoleId)
                return {'Bu':response}
            except Exception as e:
                return {'exception':str(e)}

api.add_resource(GetAllBusBasedOn_User,'/GetAllBusBasedOn_User')

@app.route("/Downloads/<path:path>")
def get_download_file(path):
    """Download a file."""
    print(path)
    filename = r"{}{}".format(config.DownloadPathLocal,path)
    print(filename)
    if not(os.path.exists(filename)):
        filename = r"{}No-image-found.jpg".format(config.DownloadPathWeb)
    return send_file(filename)


#######################  GIGS API
class authentication(Resource):
    @staticmethod
    def post():
        if request.method=='POST':
            try:
                username = request.form['username']
                password = request.form['password']
                token_id = request.form['token_id']
                
                tr = Database.Login(username,password)
                if tr != []:
                    if tr[0]['Is_Active'] == 1:
                        res = {'success':True, 'description':'Authentication Successful', 'user_name': tr[0]['User_Name'], 'user_id':int(tr[0]['User_Id']), 'user_role_id':int(tr[0]['User_Role_Id'])}

                    elif tr[0]['Is_Active'] == 0:
                        res = {'success':False, 'description':'Inactive User Credential'}
                    
                    else:
                        res = {'success':False, 'description':'Authentication failed'}
                else:
                    res = {'success':False, 'description':'Invalid Username Password'}

                return jsonify(res)

            except Exception as e:

                res = {'success':False, 'description':'error: '+str(e)}
                return jsonify(res)
               

api.add_resource(authentication,'/authentication')

class get_password(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            email = request.args['email']
            token_id = request.args['token_id']
            
            data = Database.recover_pass_db(email)
            if len(data)>0:
                res = sent_mail.forget_password(email,data[0][1],data[0][3] + ' ' + data[0][4])
                if res['status']:
                    res = {'success':True, 'description':res['description']}
                    #msg = {"message":, "title":'Sucess',"UserId":data[0][0]}
                else:
                    res = {'success':False, 'description':res['description']}
                   
            else:
                res = {'success':False, 'description':'Invalid Email'}

            
            return jsonify(res)

api.add_resource(get_password,'/get_password')

class get_all_me(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            token_id = request.args['token_id']

            data = Database.get_all_me()
            if len(data)>0:
                res = {'success':True, 'description':'data found', 'me_array':data}
                return jsonify(res)
                                   
            else:
                res = {'success':False, 'description':'No data found'}
                return jsonify(res)
            
            

api.add_resource(get_all_me,'/get_all_me')

class client_basedon_user(Resource):
    @staticmethod
    def get():
        if request.method == 'GET':
            user_id = request.args['user_id']
            user_role_id = request.args['user_role_id']
            return Master.client_basedon_user(user_id, user_role_id)

api.add_resource(client_basedon_user, '/client_basedon_user')


class get_me_category(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            token_id = request.args['token_id']
            
            if token_id!='398722':
                res = {'success':False, 'description':'Invalid Token Id'}
                return jsonify(res)
            
            data = Database.get_me_category_db()
            #data = Database.get_all_me()
            if len(data)>0:
                res = {'success':True, 'description':'data found', 'me_category':data}
                return jsonify(res)
                                   
            else:
                res = {'success':False, 'description':'No data found'}
                return jsonify(res)

api.add_resource(get_me_category,'/get_me_category')

    
#tma-filter-report

@app.route("/report file/<path:path>")
def get_tma_file(path):
    """Download a file."""
    filename = r"{}{}".format(config.neo_report_file_path,path)
    if not(os.path.exists(filename)):
        filename = r"{}No-image-found.jpg".format(config.ReportDownloadPathWeb)
    return send_file(filename)


class download_trainer_filter(Resource):
    DownloadPath=config.neo_report_file_path
    file_name = "Trainer_Filtered"+datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    @staticmethod
    def post():
        if request.method=='POST':
            try:
                user_id = request.form['user_id']
                user_role_id=request.form['user_role_id']
                centers=request.form['centers']
                status=request.form['status']
                
                path = download_trainer_filter.DownloadPath + download_trainer_filter.file_name +'.xlsx'
                Database.download_trainer_filter(user_id, user_role_id, centers, status, path)
                
                #send_file(config.ReportDownloadPathLocal+download_tma_registration_compliance_report.report_name+'.xlsx')
                return {'FileName':download_trainer_filter.file_name,'FilePath':config.neo_report_file_path_web}
            except Exception as e:
                print(str(e))
                return {"exceptione":str(e)}
api.add_resource(download_trainer_filter,'/download_trainer_filter')


@app.route("/tma_report_filter_page")
def tma_report_filter_page():
    if g.user:
        return render_template("TMA-Report/tma-filter-report.html")
    else:
        return redirect("/")

@app.route("/tma_report_filter")
def tma_report_filter():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="tma_report_filter_page")
    else:
        return render_template("login.html",error="Session Time Out!!")

class AllCustomer_report(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            try:
                response = Database.AllCustomer_report_db()
                return {'Customer':response}
            except Exception as e:
                return {'exception':str(e)}

api.add_resource(AllCustomer_report,'/AllCustomer_report_new')
class AllCustomer_report_new(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            try:
                response = Database.AllCustomer_report_db()
                return {'Customer':response}
            except Exception as e:
                return {'exception':str(e)}
api.add_resource(AllCustomer_report_new,'/AllCustomer_report_new')

class All_Center_based_on_customer(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            try:
                customer_id=request.args['Customer_id']
                response = Database.AllCenter_customer_db(customer_id)
                return {'Centers':response}
            except Exception as e:
                return {'exception':str(e)}

api.add_resource(All_Center_based_on_customer,'/All_Center_based_on_customer')

class All_Course_basedon_customer_center(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            try:
                customer_id=request.args['Customer_id']
                center_id=request.args['Center_id']
                response = Database.AllCourse_customercenter_db(customer_id, center_id)
                return {'Courses':response}
            except Exception as e:
                return {'exception':str(e)}

api.add_resource(All_Course_basedon_customer_center,'/All_Course_basedon_customer_center')

class updated_tma_report(Resource):
    report_name = "Trainerwise_TMA_Registration_Compliance"+datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    @staticmethod
    def post():
        if request.method=='POST':
            try:
                
                from_date = request.form["from_date"]
                to_date = request.form["to_date"]
                Customers = request.form["Customers"]
                Centers =request.form["Centers"]
                Courses = request.form["Courses"]

                file_name='tma_report_'+str(datetime.now().strftime('%Y%m%d_%H%M%S'))+'.xlsx'

                resp = filter_tma_report.create_report(from_date, to_date, Customers, Centers, Courses, file_name)
                
                return resp
                #return {'FileName':"abc.excel",'FilePath':'lol', 'download_file':''}
            except Exception as e:
                #print(str(e))
                return {"exceptione":str(e)}
api.add_resource(updated_tma_report,'/updated_tma_report')

class updated_new_tma_report(Resource):
    report_name = "Trainerwise_TMA_Registration_Compliance"+datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    @staticmethod
    def post():
        if request.method=='POST':
            try:
                
                from_date = request.form["from_date"]
                to_date = request.form["to_date"]
                Customers = request.form["Customers"]
                Centers =request.form["Centers"]
                Courses = request.form["Courses"]

                file_name='tma_report_'+str(datetime.now().strftime('%Y%m%d_%H%M%S'))+'.xlsx'

                resp = filter_tma_report_new.create_report(from_date, to_date, Customers, Centers, Courses, file_name)
                
                return resp
                #return {'FileName':"abc.excel",'FilePath':'lol', 'download_file':''}
            except Exception as e:
                #print(str(e))
                return {"exceptione":str(e)}
api.add_resource(updated_new_tma_report,'/updated_new_tma_report')


class GetAllContractStages(Resource):
    @staticmethod
    def get():
        try:
            if request.method=='GET':
                return {"Stages":Master.GetAllContractStages()}
        except Exception as e:
            return {"exception":str(e)}

api.add_resource(GetAllContractStages,'/GetAllContractStages')
          
class All_Sector(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            try:
                
                response = Database.AllSector_db()
                return {'Sectors':response}
            except Exception as e:
                return {'exception':str(e)}
api.add_resource(All_Sector,'/All_Sector')

class All_Emp_Status(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            try:
                
                response = Database.All_Emp_Status_db()
                return {'emp_status':response}
            except Exception as e:
                return {'exception':str(e)}
api.add_resource(All_Emp_Status,'/All_Emp_Status')

class AllQPBasedOnSector(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            try:
                sector_id =request.args["sector_id"]
                response = Database.AllQPBasedOnSector_db(sector_id)
                return {'QP':response}
            except Exception as e:
                return {'exception':str(e)}

api.add_resource(AllQPBasedOnSector,'/AllQPBasedOnSector')

class All_RM_role(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            try:
                
                response = Database.All_RM_role_db()
                return {'RM_ROLE':response}
            except Exception as e:
                return {'exception':str(e)}
api.add_resource(All_RM_role,'/All_RM_role')

class All_Reporting_manager_basedon_role_id(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            try:
                rm_role_id =request.args["rm_role_id"]
                response = Database.All_RM_basedon_role_db(rm_role_id)
                return {'Users':response}
            except Exception as e:
                return {'exception':str(e)}

api.add_resource(All_Reporting_manager_basedon_role_id,'/All_Reporting_manager_basedon_role_id')

class All_entity(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            try:
                response = Database.All_entity_db()
                return {'Entity':response}
            except Exception as e:
                return {'exception':str(e)}
api.add_resource(All_entity,'/All_entity')

class All_role(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            try:
                response = Database.All_role_db()
                return {'Role':response}
            except Exception as e:
                return {'exception':str(e)}
api.add_resource(All_role,'/All_role')

class All_dept(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            try:
                response = Database.All_dept_db()
                return {'Dept':response}
            except Exception as e:
                return {'exception':str(e)}
api.add_resource(All_dept,'/All_dept')


class Get_All_Courses(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            try:
                
                response = Database.AllCourse_db()
                return {'Courses':response}
            except Exception as e:
                return {'exception':str(e)}

api.add_resource(Get_All_Courses,'/Get_All_Courses')


api.add_resource(DownloadDump,'/DownloadDump')

####################################################################################################
#Center_Type_API's
@app.route("/download_master_data_page")
def download_master_data_page():
    if g.user:
        return render_template("download-master-data.html")
    else:
        return render_template("login.html",error="Session Time Out!!")


@app.route("/download_master_data")
def download_master_data():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="download_master_data_page")
    else:
        return render_template("login.html",error="Session Time Out!!") 
####################################################################################################

class Get_all_Funding_resources(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            try:
                response = Database.All_Funding_resources_db()
                return {'Funding_Resources':response}
            except Exception as e:
                return {'exception':str(e)}
api.add_resource(Get_all_Funding_resources,'/Get_all_Funding_resources')

class GetDashboardCount(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            try:
                UserId=request.args.get('user_id',0,type=int)
                UserRoleId=request.args.get('user_role_id',0,type=int)
                UserRegionId=request.args.get('user_region_id',0,type=int)
                response=Master.GetDashboardCount(UserId,UserRoleId,UserRegionId)
                return { "Dashboard" : response}
            except Exception as e:
                print(str(e))
                return {} 
api.add_resource(GetDashboardCount,'/GetDashboardCount')

class GetDepartmentUsers(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            try:
                UserId=request.args.get('user_id',0,type=int)
                UserRoleId=request.args.get('user_role_id',0,type=int)
                UserRegionId=request.args.get('user_region_id',0,type=int)
                response=Master.GetDepartmentUsers(UserId,UserRoleId,UserRegionId)
                return { "Departments" : response}
            except Exception as e:
                print(str(e))
                return {} 
api.add_resource(GetDepartmentUsers,'/GetDepartmentUsers')

#All_Department_db
class GetAllDepartment(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            try:
                response=Database.All_Department_db()
                return { "Departments" : response}
            except Exception as e:
                print(str(e))
                return {} 
api.add_resource(GetAllDepartment,'/GetAllDept')


class GetAllSalesCategory(Resource):
    @staticmethod
    def get():
        if request.method == 'GET':
            return Master.GetAllSalesCategory()
api.add_resource(GetAllSalesCategory,'/GetAllSalesCategory')

class Get_all_Customer_Group(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            try:
                customer_group_id=request.args.get('customer_group_id',0,type=int)
                response = Database.Get_all_Customer_Group_db(customer_group_id)
                return {'Customer_Group':response}
            except Exception as e:
                return {'exception':str(e)}
api.add_resource(Get_all_Customer_Group,'/Get_all_Customer_Group')
#####################################################################################################
class Get_all_Entity(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            try:
                response = Database.Get_all_Entity_db()
                return {'Entity':response}
            except Exception as e:
                return {'exception':str(e)}
api.add_resource(Get_all_Entity,'/Get_all_Entity')

class Get_all_Project_Group(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            try:
                response = Database.Get_all_Project_Group_db()
                return {'Project_Group':response}
            except Exception as e:
                return {'exception':str(e)}
api.add_resource(Get_all_Project_Group,'/Get_all_Project_Group')

class Get_all_Block(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            try:
                response = Database.Get_all_Block_db()
                return {'Block':response}
            except Exception as e:
                return {'exception':str(e)}
api.add_resource(Get_all_Block,'/Get_all_Block')

class Get_all_Product(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            try:
                response = Database.Get_all_Product_db()
                return {'Product':response}
            except Exception as e:
                return {'exception':str(e)}
api.add_resource(Get_all_Product,'/Get_all_Product')


class GetContractbycustomer(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            try:
                Customer_Id=request.args.get('Customer_Id',0,type=int)
                response = Database.GetContractbycustomer_db(Customer_Id)
                return response 
            except Exception as e:
                return {'exception':str(e)}
api.add_resource(GetContractbycustomer,'/GetContractbycustomer')

class Getsubprojectbyproject(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            try:
                Project_Id=request.args.get('Project_Id',0,type=int)
                response = Database.Getsubprojectbyproject_db(Project_Id)
                return response 
            except Exception as e:
                return {'exception':str(e)}
api.add_resource(Getsubprojectbyproject,'/Getsubprojectbyproject')



class GetAllCategoryTypes(Resource):
    @staticmethod
    def get():
        if request.method == 'GET':
            return Master.GetAllCategoryTypes()
api.add_resource(GetAllCategoryTypes,'/GetAllCategoryTypes')

class GetSubProjectsForCenter(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            center_id=request.args.get('center_id',0,type=int)
            response={"SubProjects":Master.GetSubProjectsForCenter(center_id)}
            return response
api.add_resource(GetSubProjectsForCenter,'/GetSubProjectsForCenter')

class Get_all_Center(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            try:
                user_id=request.args.get('user_id',0,type=int)
                user_role_id=request.args.get('user_role_id',0,type=int)
                response = Database.Get_all_Center_db(user_id,user_role_id)
                return {'Center':response}
            except Exception as e:
                return {'exception':str(e)}
api.add_resource(Get_all_Center,'/Get_all_Center')

class get_subproject_basedon_proj_multiple(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            project_id=request.form['ProjectId']
            user_id=0
            if 'user_id' in request.form:
                user_id=request.form['user_id']
            user_role_id=0
            if 'user_role_id' in request.form:
                user_role_id=request.form['user_role_id']
            return {"Sub_Project": Database.get_subproject_basedon_proj_multiple(user_id,user_role_id,project_id)} 
api.add_resource(get_subproject_basedon_proj_multiple,'/get_subproject_basedon_proj_multiple')

#QP_API's
@app.route("/sales_dashboard_page")
def sales_dashboard_page():
    if g.user:
        return render_template("Report-powerbi/sales_dashboard.html")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/sales_dashboard")
def sales_dashboard():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="sales_dashboard_page")
    else:
        return render_template("login.html",error="Session Time Out!!")

class get_user_details_new(Resource):
    @staticmethod
    def get():
        if request.method == 'GET':
            user_id=int(request.args['user_id'])
            return UsersM.get_user(user_id)
api.add_resource(get_user_details_new,'/get_user_details_new')

class GetProjectsForCourse(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            try:
                CourseId=request.args.get('CourseId',0,type=int)
                response = Master.GetProjectsForCourse(CourseId)
                return response 
            except Exception as e:
                return {'exception':str(e)}
api.add_resource(GetProjectsForCourse,'/GetProjectsForCourse')

class Get_all_industry(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            try:
                response = Database.Get_all_industry_db()
                return {'Industry':response}
            except Exception as e:
                return {'exception':str(e)}
api.add_resource(Get_all_industry,'/Get_all_industry')

class GetSubProjectsForCourse(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            try:
                CourseId=request.args.get('CourseId',0,type=int)
                response = Master.GetSubProjectsForCourse(CourseId)
                return response 
            except Exception as e:
                return {'exception':str(e)}
api.add_resource(GetSubProjectsForCourse,'/GetSubProjectsForCourse')
             

class GetCourseVariantsForCourse(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            try:
                CourseId=request.args.get('CourseId',0,type=int)
                response = Master.GetCourseVariantsForCourse(CourseId)
                return response 
            except Exception as e:
                return {'exception':str(e)}
api.add_resource(GetCourseVariantsForCourse,'/GetCourseVariantsForCourse')

class GetCentersForCourse(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            try:
                CourseId=request.args.get('CourseId',0,type=int)
                response = Master.GetCentersForCourse(CourseId)
                return response 
            except Exception as e:
                return {'exception':str(e)}
api.add_resource(GetCentersForCourse,'/GetCentersForCourse')

class Get_all_ProjectType(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            try:
                response = Database.Get_all_ProjectType_db()
                return {'ProjectType':response}
            except Exception as e:
                return {'exception':str(e)}
api.add_resource(Get_all_ProjectType,'/Get_all_ProjectType')

class All_Course_basedon_center(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            try:
                user_id=request.args.get('user_id',0,type=int)
                user_role_id=request.args.get('user_role_id',0,type=int)
                center_id=request.args['Center_id']
                response = Database.AllCourse_center_db(user_id,user_role_id,center_id)
                return {'Courses':response}
            except Exception as e:
                return {'exception':str(e)}
api.add_resource(All_Course_basedon_center,'/All_Course_basedon_center')

class GetSubProjectsForCenter_Course(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            user_id=request.args.get('user_id',0,type=int)
            user_role_id=request.args.get('user_role_id',0,type=int)
            center_id=request.args.get('center_id',0,type=int)
            course_id=request.args.get('course_id',0,type=int)
            sub_project_id=request.args.get('sub_project_id',0,type=int)
            response={"SubProjects":Master.GetSubProjectsForCenter_course(user_id,user_role_id,center_id, course_id, sub_project_id)}
            return response
api.add_resource(GetSubProjectsForCenter_Course,'/GetSubProjectsForCenter_Course')

class GetcofundingForCenter_Course(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            center_id=request.args.get('center_id',0,type=int)
            course_id=request.args.get('course_id',0,type=int)
            sub_project_id = request.args.get('sub_project_id',0,type=int)
            response={"SubProjects":Master.GetSubProjectsForCenter(center_id, course_id, sub_project_id)}
            return response
api.add_resource(GetcofundingForCenter_Course,'/GetcofundingForCenter_Course')

####################################################################################################
#Assessment_API's

@app.route("/assessment_page")
def assessment_page():
    if g.user:
        status=request.args.get('status',-1,type=int)
        return render_template("Assessment/assessments-batch-list.html", status=status)
    else:
        return render_template("login.html",error="Session Time Out!!")


@app.route("/assessment")
def assessment():
    if g.user:
        status=request.args.get('status',-1,type=int) 
        html_str="assessment_page?status=" + str(status)
        return render_template("home.html",values=g.User_detail_with_ids,html=html_str)
    else:
        return render_template("login.html",error="Session Time Out!!")

class GetBatchAssessments(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            try:
                BatchId=request.args.get('BatchId',0,type=int)
                response = Assessments.GetBatchAssessments(BatchId)
                return response 
            except Exception as e:
                return {'exception':str(e)}
api.add_resource(GetBatchAssessments,'/GetBatchAssessments')

class GetAssessmentTypes(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            try:
                response = Assessments.GetAssessmentTypes()
                return response 
            except Exception as e:
                return {'exception':str(e)}
api.add_resource(GetAssessmentTypes,'/GetAssessmentTypes')

class GetAssessmentAgency(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            try:
                response = Assessments.GetAssessmentAgency()
                return response 
            except Exception as e:
                return {'exception':str(e)}
api.add_resource(GetAssessmentAgency,'/GetAssessmentAgency')

class ScheduleAssessment(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            batch_id=request.form['batch_id']
            user_id=request.form['user_id']
            requested_date=request.form['requested_date']
            scheduled_date=request.form['scheduled_date']
            assessment_type_id=request.form['assessment_type_id']
            assessment_agency_id=request.form['assessment_agency_id']
            assessment_id=request.form['assessment_id']
            return Assessments.ScheduleAssessment(batch_id,user_id,requested_date,scheduled_date,assessment_type_id,assessment_agency_id,assessment_id)
api.add_resource(ScheduleAssessment,'/ScheduleAssessment')

api.add_resource(DownloadAssessmentResult,'/DownloadAssessmentResult')
################################################################################################################
@app.route("/PostgreSqlServerApi", defaults={"param": None})
@app.route("/PostgreSqlServerApi/<string:param>", methods=["GET"])
def postgre_sql_server_api(param):
    try:
        postgre_sql = PostgreSql()
        #log.info("> POSTGRE_SQL data request")
        data = postgre_sql.get_data(param)
        response = {"status": 200, "data": data}
    except Exception as error:
        #log.error("PostgreSqlServerApi request error: {}".format(error))
        response = {"status": 400, "message": str(error)}
    finally:
        #log.info("< PostgreSqlServerApi --> " + Log.str(response))
        return jsonify(response)

#QP_API's
@app.route("/operational_dashboard_page")
def operational_dashboard_page():
    if g.user:
        return render_template("Report-powerbi/operational_dashboard.html")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/operation_dashboard")
def operation_dashboard():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="operational_dashboard_page")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/Trainer_Dashboard_page")
def Trainer_Dashboard_page():
    if g.user:
        return render_template("Report-powerbi/Trainer_Dashboard.html")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/trainer_dashboard")
def trainer_dashboard():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="Trainer_Dashboard_page")
    else:
        return render_template("login.html",error="Session Time Out!!")


class Getcandidatebybatch(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            try:
                batch_id=request.args.get('batch_id',0,type=int)
                response = Database.Getcandidatebybatch_db(batch_id)
                return response 
            except Exception as e:
                return {'exception':str(e)}
api.add_resource(Getcandidatebybatch,'/Getcandidatebybatch')

#####################################################################################################
#Project_API's
@app.route("/my_project_list_page")
def my_project_list_page():
    if g.user:
        return render_template("Master/my-project-list.html")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/my_projects")
def my_projects():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html='my_project_list_page')
    else:
        return render_template("login.html",error="Session Time Out!!")

class my_project_list(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            user_id = request.form['user_id']
            user_role_id = request.form['user_role_id'] 
            user_region_id = request.form['user_region_id']
            start_index = request.form['start']
            page_length = request.form['length']
            search_value = request.form['search[value]']
            order_by_column_position = request.form['order[0][column]']
            order_by_column_direction = request.form['order[0][dir]']
            draw=request.form['draw']
            return Master.my_project_list(user_id,user_role_id,user_region_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)
api.add_resource(my_project_list,'/my_project_list')

##################################################################################################
class GetCoursesForCenter(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            center_id=request.args.get('center_id',0,type=int)
            response={"Courses":Master.GetCoursesForCenter(center_id)}
            return response
api.add_resource(GetCoursesForCenter,'/GetCoursesForCenter')

class GetCoursesForProject(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            project_id=request.args.get('project_id',0,type=int)
            response={"Courses":Master.GetCoursesForProject(project_id)}
            return response
api.add_resource(GetCoursesForProject,'/GetCoursesForProject')

class GetCentersForProject(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            project_id=request.args.get('project_id',0,type=int)
            response={"Centers":Master.GetCentersForProject(project_id)}
            return response
api.add_resource(GetCentersForProject,'/GetCentersForProject')

class PMT_Department_user(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            try:
                response = Database.PMT_Department_user_db()
                return response 
            except Exception as e:
                return {'exception':str(e)}
api.add_resource(PMT_Department_user,'/PMT_Department_user')

class sales_Department_user(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            try:
                response = Database.sales_Department_user_db()
                return response 
            except Exception as e:
                return {'exception':str(e)}
api.add_resource(sales_Department_user,'/sales_Department_user')

@app.route("/subproject_add_edit")
def subproject_add_edit():
    if g.user:
        return render_template("Master/subproject-add-edit.html",project_code=g.project_code, subproject_id=g.subproject_id)
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/assign_subproject_add_edit_to_home", methods=['GET','POST'])
def assign_subproject_add_edit_to_home():
    session['subproject_id']=request.form['hdn_subproject_id']
    session['project_code']=request.form['hdn_project_code']
    #print(request.form['hdn_subproject_id'], request.form['hdn_project_code'])
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="subproject_add_edit")
    else:
        return render_template("login.html",error="Session Time Out!!")

class all_states_based_on_region(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            try:
                region_id=request.args.get('region_id',0,type=int)
                response = Database.Getstatebasedonregion_db(region_id)
                return response 
            except Exception as e:
                return {'exception':str(e)}
api.add_resource(all_states_based_on_region,'/all_states_based_on_region')

class all_center_based_on_state(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            try:
                state_id=request.args.get('state_id',0,type=int)
                response = Database.Getcenterbasedonstate_db(state_id)
                return response 
            except Exception as e:
                return {'exception':str(e)}
api.add_resource(all_center_based_on_state,'/all_center_based_on_state')

class all_course_based_on_center(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            center_ids=request.form['center_ids']
            project_code=request.form['project_code']
            return Database.Getcoursebasedoncenter_db(center_ids,project_code)
api.add_resource(all_course_based_on_center,'/all_course_based_on_center')

class add_subproject_details(Resource):
    @staticmethod
    def post():
        
        if request.method == 'POST':
            SubProjectName=request.form['SubProjectName']
            SubProjectCode=request.form['SubProjectCode']
            Region=request.form['Region']
            State=request.form['State']
            Centers=request.form['Centers']
            Course=request.form['Course']
            PlannedStartDate=request.form['PlannedStartDate']
            PlannedEndDate=request.form['PlannedEndDate']
            ActualStartDate=request.form['ActualStartDate']
            ActualEndDate=request.form['ActualEndDate']
            
            user_id=g.user_id
            subproject_id=g.subproject_id
            project_code = g.project_code       
            isactive=request.form['isactive']
            return Master.add_subproject_details(SubProjectName, SubProjectCode, Region, State, Centers, Course, PlannedStartDate, PlannedEndDate, ActualStartDate, ActualEndDate, user_id, subproject_id, project_code, isactive)
api.add_resource(add_subproject_details,'/add_subproject_details')

@app.route("/SqlServerApi", defaults={"param": None})
@app.route("/SqlServerApi/<string:param>", methods=["GET"])
def SqlServerApi(param):
    try:
        ms_sql = MsSql()
        #log.info("> POSTGRE_SQL data request")
        data = ms_sql.get_data(param)
        response = {"status": 200, "data": data}
    except Exception as error:
        #log.error("PostgreSqlServerApi request error: {}".format(error))
        response = {"status": 400, "message": str(error)}
    finally:
        #log.info("< PostgreSqlServerApi --> " + Log.str(response))
        return jsonify(response)

class GetSubProjectsForUser(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            user_id=request.args.get('user_id',0,type=int)
            response={"SubProjects":Master.GetSubProjectsForuser(user_id)}
            return response
api.add_resource(GetSubProjectsForUser,'/GetSubProjectsForUser')

class candidate_download_report(Resource):
    report_name = "Trainerwise_TMA_Registration_Compliance"+datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    @staticmethod
    def post():
        if request.method=='POST':
            try:
                #candidate_id, user_id, user_role_id, status, customer, project, sub_project, region, center, center_type
                candidate_id = request.form["candidate_id"]
                user_id = request.form["user_id"]
                user_role_id = request.form["user_role_id"]
                status = request.form["status"]
                customer = request.form["customer"]
                project = request.form["project"]
                sub_project = request.form["sub_project"]
                region = request.form["region"]
                center = request.form["center"]
                center_type = request.form["center_type"]
                
                file_name='candidate_report_'+str(user_id) +'_'+ str(datetime.now().strftime('%Y%m%d_%H%M%S'))+'.xlsx'
                print(candidate_id, user_id, user_role_id, status, customer, project, sub_project, region, center, center_type, file_name)
                resp = candidate_report.create_report(candidate_id, user_id, user_role_id, status, customer, project, sub_project, region, center, center_type, file_name)
                
                return resp
                #return {'FileName':"abc.excel",'FilePath':'lol', 'download_file':''}
            except Exception as e:
                #print(str(e))
                return {"exceptione":str(e)}
api.add_resource(candidate_download_report,'/candidate_download_report')

#################################################################################################################################
#ECP REPORT PAGE
@app.route("/ecp_report_page")
def ecp_report_page():
    if g.user:
        return render_template("Reports/ecp_report.html")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/ecp_report")
def ecp_report():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="ecp_report_page")
    else:
        return render_template("login.html",error="Session Time Out!!")

class GetECPReportData(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            try:
                user_id=request.args.get('user_id',0,type=int)
                user_role_id=request.args.get('user_role_id',0,type=int)
                from_date=request.args.get('from_date','',type=str)
                to_date=request.args.get('to_date','',type=str)
                response = Report.GetECPReportData(user_id,user_role_id,from_date,to_date)
                return response 
            except Exception as e:
                return {'exception':str(e)}
api.add_resource(GetECPReportData,'/GetECPReportData')
###############################################################################

if __name__ == '__main__':    
    app.run(debug=True)

#app.run(debug=True)
