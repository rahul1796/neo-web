from flask import Flask,render_template,request,redirect,url_for,session,g,jsonify,send_file
from flask_restful import Resource
from flask_restful import Api
from flask_cors import CORS
#from flask_session import Session
from Models import *
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
import SL4Report_filter_new
import Naton_Wise_Report
import trainer_prodctivity_report
import candidate_report
import user_subproject_download
import batch_report
import ecp_report_down
import mobilizer_report_down
import batch_candidate_download
from Models import DownloadDump
from lib.ms_sql import MsSql
from lib.postgre_sql import PostgreSql
import urllib.request
import urllib.parse
import random
from pandas_schema import Column, Schema
from pandas_schema.validation import CustomElementValidation
import numpy as np
import requests
from email.utils import parseaddr
#import hyperlink
#import excel_validation
#String check
def check_str(st):
    try:
        st = str(st)
        return re.match(r"[A-Za-z0-9!@#$%&|\*\.\,\+-_\s\\]+",st).group()==st
    except:
        return False

def check_mob_number(mob):
    try:
        mob = str(mob)
        mob = mob.replace(' ','')
        mob = mob.replace('-','')
        return (len(mob)==10)and(mob.isnumeric())or(mob=='')
        if mob[0:3]=='+91':
            return (len(mob)==13)and(mob.isnumeric())
        else:
            return (len(mob)==10)and(mob.isnumeric())
    except:
        return False

def check_pincode(pincode):
    try:
        pincode = str(pincode)
        pincode = pincode.replace(' ','')
        pincode = pincode.replace('-','')
        return (len(pincode)==6)and(pincode.isnumeric())
    except:
        return False
def check_dob(date_age):
    try:
        date_age = str(date_age)
        return re.match(r"[A-Za-z0-9!@#$%\\&\*\.\,\+-_\s]+",date_age).group()==date_age
    except:
        return False

str_validation = [CustomElementValidation(lambda d: check_str(d), 'invalid String')]
mob_validation = [CustomElementValidation(lambda d: check_mob_number(d), 'invalid mobile number (dont use +91)')]
pincode_validation = [CustomElementValidation(lambda d: check_pincode(d), 'invalid pincode')]
null_validation = [CustomElementValidation(lambda d: d is not np.nan, 'this field cannot be null')]
dob_validation = [CustomElementValidation(lambda d: check_dob(d), 'either date or age is not valid')]
status_validation = [CustomElementValidation(lambda d: d.lower() in ['certified','notcertified'], 'invalid status (certified, notcertified allowed)')]
flt_validation = [CustomElementValidation(lambda d: str(d).replace('.', '', 1).isdigit(), 'invalid score (number allowed)')]
yea_no_validation = [CustomElementValidation(lambda d: str(d).lower() in ['yes','no'], 'invalid option (yes/no allwed)')]
int_validation = [CustomElementValidation(lambda d: str(d).isdigit(), 'invalid score (whole number allowed)')]
#from lib.log import Log
#from lib.log import log

app = Flask(__name__)
CORS(app)
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
    g.user_role_name = None
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
        g.user_role_name = session['user_role_name']
        g.user_region_id=session['user_region_id']
        g.base_url = session['base_url']
        g.COL_url=session['COL_url']
        g.AWS_path = session['AWS_path']
        # print(g.user,g.user_id,g.user_role)
        g.User_detail_with_ids.append(g.user)
        g.User_detail_with_ids.append(g.user_id)
        g.User_detail_with_ids.append(g.user_role)
        g.User_detail_with_ids.append(g.user_role_name)
        g.User_detail_with_ids.append(g.base_url)
        g.User_detail_with_ids.append(g.user_region_id)
        g.User_detail_with_ids.append(g.COL_url)
        g.User_detail_with_ids.append(g.AWS_path)
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
    if 'partner_id' in session.keys():
        g.partner_id = session['partner_id']
    if 'candidate_id' in session.keys():
        g.candidate_id = session['candidate_id']
    if 'candidate_stage_id' in session.keys():
        g.candidate_stage_id = session['candidate_stage_id']

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

class clear_config_msg(Resource):
    @staticmethod
    def get():
        if request.method == 'GET':
            config.displaymsg=""
            return {"sucess":True}
api.add_resource(clear_config_msg,'/clear_config_msg')
    
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
        role_id = request.form['hdn_login_userrole_id']
        role_name = request.form['hdn_login_userrole_name']
        #return(role_id)
        tr = Database.Login(email,passw)
        if tr != []:
            if tr[0]['Is_Active'] == 1:
                session['user_name'] = tr[0]['User_Name'] 
                session['user_id'] = tr[0]['User_Id']
                session['user_role_id'] = role_id #tr[0]['User_Role_Id']
                session['user_role_name'] = role_name
                session['user_region_id'] = tr[0]['Region_Id']  
                session['base_url'] = config.Base_URL
                session['COL_url'] = config.COL_URL
                session['AWS_path'] = config.aws_location
                config.displaymsg=""
                return redirect(url_for('home'))
                #assign_sessions()
            elif tr[0]['Is_Active'] == 0:
                config.displaymsg="Please contact admin because this user is inactive."
                return redirect(url_for('index'))
            else:
                config.displaymsg="wrong"
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
            country_id=request.form['CenterCountry']
            satet_id=request.form['CenterState']
            location_name=request.form['LocationName']
            address=request.form['Address']
            pinCode=request.form['PinCode']
            District=request.form['District']
            partner_id=request.form['PartnerId']
            geolocation=request.form['geolocation']
            return Master.add_center(center_name,user_id,is_active,center_id,center_type_id,country_id,satet_id,location_name,address,pinCode,District,partner_id,geolocation)

class get_center_details(Resource):
    @staticmethod
    def get():
        if request.method == 'GET':
            return jsonify(Master.get_center_details(g.center_id))

class get_all_BU(Resource):
    @staticmethod
    def get():
        if request.method == 'GET':
            return Master.get_all_BU()

class Get_all_Sponser(Resource):
    @staticmethod
    def get():
        if request.method == 'GET':
            return Master.Get_all_Sponser()
class get_all_Cluster_Based_On_Region(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            region_id=request.form['region_id']
            return  Master.get_all_Cluster_Based_On_Region(region_id)

api.add_resource(get_all_BU,'/Get_all_BU')
api.add_resource(Get_all_Sponser,'/Get_all_Sponser')
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
            CourseId=request.form['CourseId']
            CourseName=request.form['CourseName']
            CourseCode=request.form['CourseCode']
            Sector=request.form['Sector']
            Qp=request.form['Qp']
            Parent_Course=request.form['Parent_Course']
            Course_Duration_day=request.form['Course_Duration_day']
            Course_Duration_hour=request.form['Course_Duration_hour']
            is_ojt_req = request.form['is_ojt_req']
            OJT_Duration_hour = request.form['OJT_Duration_hour']
            isactive=request.form['isactive']
            user_id=g.user_id
            return Content.add_course(CourseId, CourseName, CourseCode, Sector, Qp, Parent_Course, Course_Duration_day, Course_Duration_hour, is_ojt_req,OJT_Duration_hour,isactive, user_id)
            
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
            Act_status_id=request.form['Act_status_id']
            
            project_ids=request.form['project_ids']
            #print(user_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw,dept_ids,role_ids,entity_ids,region_ids,RM_Role_ids,R_mangager_ids,filter_role_id,user_region_id,user_role_id,status_ids,project_ids)
            return UsersM.user_list(user_id,filter_role_id,user_region_id,user_role_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw, dept_ids, role_ids, entity_ids, region_ids, RM_Role_ids, R_mangager_ids,status_ids,project_ids,Act_status_id)
            

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
        if int(g.user_role) in [12,13,18]:
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
            customer_status = request.form['customer_status']
            
            # Planned_actual = request.form['Planned_actual']
            # StartFromDate = request.form['StartFromDate']
            # StartToDate = request.form['StartToDate']
            # EndFromDate = request.form['EndFromDate']
            # EndToDate = request.form['EndToDate']
            status = request.form['status']
            Planned_actual=''
            if 'Planned_actual' in request.form:
                Planned_actual = request.form['Planned_actual']
            StartFromDate=''
            if 'StartFromDate' in request.form:
                StartFromDate = request.form['StartFromDate']
            StartToDate=''
            if 'StartToDate' in request.form:
                StartToDate = request.form['StartToDate']
            EndFromDate=''
            if 'EndFromDate' in request.form:
                EndFromDate = request.form['EndFromDate']
            EndToDate=''
            if 'EndToDate' in request.form:
                EndToDate = request.form['EndToDate']
            BU=''
            if 'BU' in request.form:
                BU = request.form['BU']            
            course_ids=''
            if 'course_ids' in request.form:
                course_ids=request.form['course_ids']
            batch_codes=''
            if 'BatchCodes' in request.form:
                batch_codes=request.form['BatchCodes']

            start_index = request.form['start']
            page_length = request.form['length']
            search_value = request.form['search[value]']
            order_by_column_position = request.form['order[0][column]']
            order_by_column_direction = request.form['order[0][dir]']
            draw=request.form['draw']

            #print(order_by_column_position)
            
            return Batch.batch_list_updated(batch_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw,user_id,user_role_id, status, customer, project, sub_project, region, center, center_type,course_ids, batch_codes,BU, Planned_actual, StartFromDate, StartToDate, EndFromDate, EndToDate,customer_status)
class batch_list_assessment(Resource):
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
            # Planned_actual = request.form['Planned_actual']
            # StartFromDate = request.form['StartFromDate']
            # StartToDate = request.form['StartToDate']
            # EndFromDate = request.form['EndFromDate']
            # EndToDate = request.form['EndToDate']
            status = request.form['status']
            Planned_actual=''
            if 'Planned_actual' in request.form:
                Planned_actual = request.form['Planned_actual']
            StartFromDate=''
            if 'StartFromDate' in request.form:
                StartFromDate = request.form['StartFromDate']
            StartToDate=''
            if 'StartToDate' in request.form:
                StartToDate = request.form['StartToDate']
            EndFromDate=''
            if 'EndFromDate' in request.form:
                EndFromDate = request.form['EndFromDate']
            EndToDate=''
            if 'EndToDate' in request.form:
                EndToDate = request.form['EndToDate']
            BU=''
            if 'BU' in request.form:
                BU = request.form['BU']            
            course_ids=''
            if 'course_ids' in request.form:
                course_ids=request.form['course_ids']
            if 'assessment_stage_id' in request.form:
                assessment_stage_id=request.form['assessment_stage_id']
            start_index = request.form['start']
            page_length = request.form['length']
            search_value = request.form['search[value]']
            order_by_column_position = request.form['order[0][column]']
            order_by_column_direction = request.form['order[0][dir]']
            draw=request.form['draw']

            #print(order_by_column_position)
            
            return Batch.batch_list_assessment(batch_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw,user_id,user_role_id, status, customer, project, sub_project, region, center, center_type,course_ids, assessment_stage_id,BU, Planned_actual, StartFromDate, StartToDate, EndFromDate, EndToDate)

class batch_list_certification(Resource):
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
            # Planned_actual = request.form['Planned_actual']
            # StartFromDate = request.form['StartFromDate']
            # StartToDate = request.form['StartToDate']
            # EndFromDate = request.form['EndFromDate']
            # EndToDate = request.form['EndToDate']
            status = request.form['status']
            Planned_actual=''
            if 'Planned_actual' in request.form:
                Planned_actual = request.form['Planned_actual']
            StartFromDate=''
            if 'StartFromDate' in request.form:
                StartFromDate = request.form['StartFromDate']
            StartToDate=''
            if 'StartToDate' in request.form:
                StartToDate = request.form['StartToDate']
            EndFromDate=''
            if 'EndFromDate' in request.form:
                EndFromDate = request.form['EndFromDate']
            EndToDate=''
            if 'EndToDate' in request.form:
                EndToDate = request.form['EndToDate']
            BU=''
            if 'BU' in request.form:
                BU = request.form['BU']            
            course_ids=''
            if 'course_ids' in request.form:
                course_ids=request.form['course_ids']
            assessment_stage_id=''
            certification_stage_id=''
            if 'assessment_stage_id' in request.form:
                assessment_stage_id=request.form['assessment_stage_id']
            if 'certification_stage_id' in request.form:
                certification_stage_id=request.form['certification_stage_id']
            start_index = request.form['start']
            page_length = request.form['length']
            search_value = request.form['search[value]']
            order_by_column_position = request.form['order[0][column]']
            order_by_column_direction = request.form['order[0][dir]']
            draw=request.form['draw']

            #print(order_by_column_position)
            
            return Batch.batch_list_certification(batch_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw,user_id,user_role_id, status, customer, project, sub_project, region, center, center_type,course_ids, assessment_stage_id,certification_stage_id,BU, Planned_actual, StartFromDate, StartToDate, EndFromDate, EndToDate)

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
            OJTStartDate=request.form['OJTStartDate']
            OJTEndDate=request.form['OJTEndDate']
            user_id=g.user_id
            isactive=request.form['isactive']
            Product=request.form['Product']
            Course=request.form['Course']
            SubProject=request.form['SubProject']
            Cofunding=request.form['Cofunding']
            room_ids=request.form['room_ids']
            planned_batch_id=0
            if 'PlannedBatchId' in request.form:
                planned_batch_id=request.form['PlannedBatchId']
            return Batch.add_batch(BatchName, Product, Center, Course, SubProject, Cofunding, Trainer, isactive, PlannedStartDate, PlannedEndDate, ActualStartDate, ActualEndDate, StartTime, EndTime, BatchId, user_id, room_ids,planned_batch_id,OJTStartDate, OJTEndDate)


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

class trainers_based_on_sub_project(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            sub_project_id=request.form['sub_project_id']
            return Batch.AllTrainersOnSubProject(sub_project_id)

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
class candidates_enrolled_in_batch(Resource):
    @staticmethod
    def get():
         if request.method == 'GET':  
            batch_id=request.args.get('batch_id',0,type=int)  
            assessment_id=request.args.get('assessmentId',0,type=int)  
            candidate_id=request.args.get('candidate_id','',type=str)          
            return Batch.candidate_enrolled_in_batch(batch_id,assessment_id,candidate_id)


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
        skilling_ids=request.form['skilling_ids']
        batch_id=request.form['batch_id']
        course_id=request.form['course_id']
        user_id= request.form['user_id']
        drop_remark = request.form['drop_remark']
        return Batch.drop_edit_candidate_batch(skilling_ids,batch_id,course_id,user_id,drop_remark)
class tag_sponser_candidate(Resource):
    @staticmethod
    def post():
        skilling_ids=request.form['skilling_ids'] 
        user_id= request.form['user_id']
        sponser_ids = request.form['sponser_ids']
        return Batch.tag_sponser_candidate(skilling_ids,sponser_ids,user_id)
class untag_users_from_sub_project(Resource):
    @staticmethod
    def post():
        map_subproject_user_ids=request.form['user_ids']
        sub_project_id=request.form['sub_project_id']
        return Master.untag_users_from_sub_project(map_subproject_user_ids,sub_project_id)
class tag_users_from_sub_project(Resource):
    @staticmethod
    def post():
        user_id=request.form['user_id']
        user_role_id=request.form['user_role_id']
        sub_project_id=request.form['sub_project_id']
        tagged_by= session['user_id']
        return Master.tag_users_from_sub_project(user_id,user_role_id,sub_project_id,tagged_by)
class assign_batch_candidates(Resource):
    @staticmethod
    def post():
        candidates=request.form['candidate_id']
        batch_id=request.form['batch_id']
        tagged_by= session['user_id']
        return Master.assign_batch_candidates(candidates,batch_id,tagged_by)
class tag_user_roles(Resource):
    @staticmethod
    def post():
        login_user_id=request.form['login_user_id']
        user_id=request.form['user_id']
        neo_role=request.form['neo_role']
        jobs_role=request.form['jobs_role']
        crm_role=request.form['crm_role']  
        isactive=request.form['isactive']  
        return UsersM.tag_user_roles(login_user_id,user_id,neo_role,jobs_role,crm_role,isactive)
class cancel_planned_batch(Resource):
    @staticmethod
    def post():
        user_id=request.form['user_id']
        planned_batch_code=request.form['planned_batch_code']
        cancel_reason=request.form['cancel_reason']               
        return Master.cancel_planned_batch(user_id,planned_batch_code,cancel_reason)
class cancel_actual_batch(Resource):
    @staticmethod
    def post():
        user_id=request.form['user_id']
        actual_batch_id=request.form['actual_batch_id']
        cancel_reason=request.form['cancel_reason']               
        return Master.cancel_actual_batch(user_id,actual_batch_id,cancel_reason)

api.add_resource(batch_list, '/batch_list')
api.add_resource(batch_list_updated, '/batch_list_updated')
api.add_resource(batch_list_assessment, '/batch_list_assessment')
api.add_resource(batch_list_certification, '/batch_list_certification')
api.add_resource(add_batch_details, '/add_batch_details')
api.add_resource(get_batch_details, '/GetBatchDetails')
api.add_resource(all_course_list, '/AllCourseList')
api.add_resource(centers_based_on_course, '/CentersBasedOnCourse')
api.add_resource(trainers_based_on_center, '/TrainersBasedOnCenter')
api.add_resource(trainers_based_on_sub_project, '/TrainersBasedOnSubProject')
api.add_resource(center_manager_based_on_center, '/CenterManagerBasedOnCenter')
api.add_resource(candidates_based_on_course,'/ALLCandidatesBasedOnCourse')
api.add_resource(candidates_maped_in_batch,'/ALLCandidatesMapedInBatch')
api.add_resource(candidates_enrolled_in_batch,'/ALLCandidatesEnrolledInBatch')
api.add_resource(add_edit_map_candidate_batch,'/add_edit_map_candidate_batch')
api.add_resource(drop_edit_map_candidate_batch,'/drop_edit_candidate_batch')
api.add_resource(tag_sponser_candidate,'/tag_sponser_candidate')
api.add_resource(untag_users_from_sub_project,'/untag_users_from_sub_project')
api.add_resource(tag_users_from_sub_project,'/tag_users_from_sub_project')
api.add_resource(assign_batch_candidates,'/assign_batch_candidates')
api.add_resource(sub_center_based_on_center, '/SubCenterBasedOnCenter')
api.add_resource(tag_user_roles,'/tag_user_roles')
api.add_resource(cancel_planned_batch,'/cancel_planned_batch')
api.add_resource(cancel_actual_batch,'/cancel_actual_batch')
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
            sector=request.form['Sector']
            user_id=g.user_id
            is_active=request.form['isactive']
            qp_id=g.qp_id
            return Content.add_qp(qp_name,qp_code,user_id,is_active,qp_id,sector)

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
            batch_id = request.form['batch_id']
            project = request.form['project']
            region = request.form['region']
            customer = request.form['customer']
            status = request.form['status']
            center_type = request.form['center_type']
            center = request.form['center']
            user_id=request.form['user_id']
            user_role_id=request.form['user_role_id']
            Contracts = request.form["Contracts"]
            #candidate_stage = request.form["candidate_stage"]
            from_date = request.form["from_date"]
            to_date = request.form["to_date"]
            
            #print(Contracts, candidate_stage, from_date, to_date)
            
            start_index = request.form['start']
            page_length = request.form['length']
            search_value = request.form['search[value]']
            order_by_column_position = request.form['order[0][column]']
            order_by_column_direction = request.form['order[0][dir]']
            draw=request.form['draw']
            
            #print(candidate_id,customer,project,sub_project,region,center,center_type,status,user_id,user_role_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)
            return Candidate.candidate_list(candidate_id,customer,project,sub_project,batch_id,region,center,center_type,status,user_id,user_role_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw, Contracts, candidate_stage, from_date, to_date)

class user_sub_project_list(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            sub_project = request.form['sub_project']
            project = request.form['project']
            region = request.form['region']
            customer = request.form['customer']
            user_id=request.form['user_id']
            user_role_id=request.form['user_role_id']
            employee_status=request.form['user_status']
            sub_project_status=request.form['sub_project_status']
            status_id=request.form['status_id']
            
            #print(Contracts, candidate_stage, from_date, to_date)
            start_index = request.form['start']
            page_length = request.form['length']
            search_value = request.form['search[value]']
            order_by_column_position = request.form['order[0][column]']
            order_by_column_direction = request.form['order[0][dir]']
            draw=request.form['draw']
            
            return Report.user_sub_project_list(customer,project,sub_project,region,user_id,user_role_id,employee_status,sub_project_status,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw, status_id)

class user_sub_project_list_download(Resource):
    @staticmethod
    def post():
        if request.method=='POST':
            sub_project = request.form['sub_project']
            project = request.form['project']
            region = request.form['region']
            customer = request.form['customer']
            user_id=request.form['user_id']
            user_role_id=request.form['user_role_id']
            employee_status=request.form['user_status']
            sub_project_status=request.form['sub_project_status']
            month=request.form['month']
            year=request.form['year']
            status_id=request.form['status_id']

            file_name='user_sub_project_report.xlsx'
            resp = user_subproject_download.create_report(sub_project,project,region,customer,user_id,user_role_id,employee_status,sub_project_status,month,year,status_id,file_name)
            return resp
          
api.add_resource(candidate_list, '/candidate_list')
api.add_resource(user_sub_project_list, '/user_sub_project_list')
api.add_resource(user_sub_project_list_download, '/user_sub_project_list_download')
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

            POC_details=request.form['POC_details']
            #print(POC_details)
            user_id=g.user_id
            is_active=request.form['isactive']
            client_id=g.client_id
            return Master.add_client(client_name,client_code,user_id,is_active,client_id,FundingSource, CustomerGroup, IndustryType, CategoryType, POC_details)

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
        return render_template("home.html",values=g.User_detail_with_ids,html="sub_project")
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
            customer_status = request.form['customer_status']
            
            user_id = request.form['user_id']
            user_role_id = request.form['user_role_id'] 
            user_region_id = request.form['user_region_id']
            start_index = request.form['start']
            page_length = request.form['length']
            search_value = request.form['search[value]']
            order_by_column_position = request.form['order[0][column]']
            order_by_column_direction = request.form['order[0][dir]']
            draw=request.form['draw']
            #print(start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)
            return Master.project_list(user_id,user_role_id,user_region_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw,entity,customer,p_group,block,practice,bu,product,status,customer_status)

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
            CourseIds=''
            if 'course_ids' in request.form:
                CourseIds=request.form['course_ids']
            
            user_id=g.user_id
            project_id=g.project_id
            isactive=request.form['isactive']
            return Master.add_project_details(ProjectName, ProjectCode, ClientName, ContractName, Practice, BU, projectgroup, ProjectType, Block, Product, ProjectManager, ActualEndDate, ActualStartDate, PlannedEndDate, PlannedStartDate, isactive, project_id, user_id,CourseIds)
                    
class client_all(Resource):
    @staticmethod
    def get():
        if request.method == 'GET':
            user_id=request.args.get('user_id',0,type=int)
            user_role_id=request.args.get('user_role_id',0,type=int)
            return Master.all_client(user_id,user_role_id)
class client_all_based_on_status(Resource):
    @staticmethod
    def get():
        if request.method == 'GET':
            user_id=request.args.get('user_id',0,type=int)
            user_role_id=request.args.get('user_role_id',0,type=int)
            status_id=request.args.get('status_id',0,type=int)
            return Master.client_all_based_on_status(user_id,user_role_id,status_id)

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
api.add_resource(client_all_based_on_status, '/GetALLClientBasedOnStatus')
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
            TrainerType= request.form['TrainerType']
            return UsersM.trainer_list(user_id,user_region_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw,user_role_id, centers, status, Region_id, Cluster_id, Dept,entity_ids,project_ids,sector_ids,TrainerType)

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
class AllAssessmentStages(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            response=[]
            try:
                UserId=request.args.get('user_id',0,type=int)
                UserRoleId=request.args.get('user_role_id',0,type=int)
                response=Report.AllAssessmentStages(UserId,UserRoleId)
                return {'AssessmentStages':response}
            except Exception as e:
                return {'exception':str(e)}

api.add_resource(AllAssessmentStages,'/AllAssessmentStages')

class AllCertificationStages(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            response=[]
            try:
                UserId=request.args.get('user_id',0,type=int)
                UserRoleId=request.args.get('user_role_id',0,type=int)
                response=Report.AllCertificationStages(UserId,UserRoleId)
                return {'CertificationStages':response}
            except Exception as e:
                return {'exception':str(e)}

api.add_resource(AllCertificationStages,'/AllCertificationStages')

class AllCertificateNames(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            response=[]
            try:
                batch_id=request.args.get('batch_id',0,type=int)
                stage=request.args.get('stage',0,type=int)
                response=Assessments.AllCertificateNames(batch_id,stage)
                return {'Certificates':response}
            except Exception as e:
                print(e)
                return {'exception':str(e)}

api.add_resource(AllCertificateNames,'/AllCertificateNames')


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
                sub_project_ids = request.form['sub_project_ids']
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
                #print(region_id,sub_project_ids,course_ids,trainer_ids,from_date,to_date,batch_stage_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)
                response=Report.TrainerDeploymentBatches(region_id,sub_project_ids,course_ids,trainer_ids,from_date,to_date,batch_stage_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)
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
                user_id = request.form['user_id']
                user_role_id  = request.form['user_role_id']
                region_id = request.form['region_id']
                sub_project_ids = request.form['sub_project_ids']
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
                #print(region_id,center_id,course_ids,trainer_ids,from_date,to_date,batch_stage_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)
                response=Report.ReportAttendanceBatches(region_id,sub_project_ids,course_ids,trainer_ids,from_date,to_date,batch_stage_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw, user_id, user_role_id)
                
                return response
            except Exception as e:
                #print(str(e))
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
                #print(batch_id,course_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)
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
            response={"TrainerActivity":Report.GetSessionTrainerActivity(batch_id,session_id),"TMAStageLogImagePath":config.Base_URL + '/GetDocumentForExcel?image_path=trainer_stage_images&image_name='}
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
            response={"CandidateAttendance":Report.GetCandidateSessionAttendance(batch_id,session_id),"GroupAttendance":GrpAttendance,"TMACandidateImagePath":config.Base_URL + '/GetDocumentForExcel?image_path=attendance_images&image_name='}
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
    return render_template('recoverpw.html', html_path=config.Base_URL)

class recover_pass(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            reco_email = request.args['reco_email']
            
            data = Database.recover_pass_db(reco_email)
            if len(data)>0:
                res = sent_mail.forget_password(reco_email,data[0][1],data[0][3] + ' ' + data[0][4])
                if res['status']:
                    msg = {"success":True,"message":res['description'], "title":'Sucess',"UserId":data[0][0]}
                else:
                    msg = {"success":False,"message":res['description'], "title":'Unable to sent',"UserId":data[0][0]}
            else:
                msg = {"success":False, "message":'Please check email or contact to admin',"title":'Invalid Email',"UserId":0}

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
    filename = r"{}data/{}".format(config.ReportDownloadPathLocal,path)
    #print(filename)
    if not(os.path.exists(filename)):
        filename = r"{}No-image-found.jpg".format(config.ReportDownloadPathLocal + 'data/')
    #return filename 
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
            status_id = request.form['status_id'] 
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
            return Master.contract_list(user_id,user_role_id,contract_id,customer_ids,stage_ids,status_id,from_date,to_date,entity_ids,sales_category_ids,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)

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
    #print(path)
    filename = r"{}{}".format(config.DownloadPathLocal_download,path)
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

@app.route("/<path:path>") #/report file
def get_tma_file(path):
    """Download a file."""
    filename = r"{}{}".format(config.neo_report_file_path,path)
    #print(filename)
    if not(os.path.exists(filename)):
        
        filename = r"{}No-image-found.jpg".format(config.ReportDownloadPathWeb)
    return send_file(filename)

class download_trainer_filter(Resource):
    @staticmethod
    def post():
        if request.method=='POST':
            try:
                user_id = request.form['user_id']
                user_role_id=request.form['user_role_id']
                centers=request.form['centers']
                entity_ids=request.form['entity_ids']
                Dept = request.form['Dept']
                Region_id=request.form['Region_id']
                Cluster_id=request.form['Cluster_id']
                status=request.form['status']
                TrainerType = request.form['TrainerType']
                user_region_id=request.form['user_region_id']
                project_ids=request.form['project_ids']
                sector_ids=request.form['sector_ids']
                
                resp = Report.create_download_trainer_filter(user_id, user_role_id, centers, entity_ids, Dept, Region_id, Cluster_id, status, TrainerType, user_region_id, project_ids, sector_ids)
                return resp
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
                user_id = request.form['user_id']
                user_role_id  = request.form['user_role_id']
                from_date = request.form["from_date"]
                to_date = request.form["to_date"]
                Customers = request.form["Customers"]
                SubProject =request.form["SubProject"]
                Courses = request.form["Courses"]
                
                file_name='tma_report_'+str(datetime.now().strftime('%Y%m%d_%H%M%S'))+'.xlsx'
                resp = filter_tma_report_new.create_report(from_date, to_date, Customers, SubProject, Courses, file_name,user_id,user_role_id)
                return resp
                
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

class All_role_neo(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            try:
                response = Database.All_role_neo_db()
                return {'Role':response}
            except Exception as e:
                return {'exception':str(e)}
api.add_resource(All_role_neo,'/All_role_neo')

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

class GetBatchDetailsAssessment(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            batch_code=request.args.get('batch_code','',type=str)
            response={"Batches":Master.GetBatchDetailsAssessment(batch_code)}
            return response
api.add_resource(GetBatchDetailsAssessment,'/GetBatchDetailsAssessment')

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

class get_batches_basedon_sub_proj_multiple(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            sub_project_id=request.form['SubProjectId']
            user_id=0
            if 'user_id' in request.form:
                user_id=request.form['user_id']
            user_role_id=0
            if 'user_role_id' in request.form:
                user_role_id=request.form['user_role_id']
            return {"Batches": Database.get_batches_basedon_sub_proj_multiple(user_id,user_role_id,sub_project_id)} 
api.add_resource(get_batches_basedon_sub_proj_multiple,'/get_batches_basedon_sub_proj_multiple')


class get_batches_based_on_project_type(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            project_type=request.form['project_type']
            user_id=0
            if 'user_id' in request.form:
                user_id=request.form['user_id']
            user_role_id=0
            if 'user_role_id' in request.form:
                user_role_id=request.form['user_role_id']
            return {"Batches": Database.get_batches_based_on_project_type(user_id,user_role_id,project_type)} 
api.add_resource(get_batches_based_on_project_type,'/get_batches_based_on_project_type')
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
@app.route("/Jobs_Dashboard_page")
def Jobs_Dashboard_page():
    if g.user:
        return render_template("Report-powerbi/Jobs Dashboard.html")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/Placement_Dashboard")
def Placement_Dashboard():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="Jobs_Dashboard_page")
    else:
        return render_template("login.html",error="Session Time Out!!")

class get_user_details_new(Resource):
    @staticmethod
    def get():
        if request.method == 'GET':
            user_id=int(request.args['user_id'])
            return UsersM.get_user(user_id)
api.add_resource(get_user_details_new,'/get_user_details_new')

class get_user_role_details_new(Resource):
    @staticmethod
    def get():
        if request.method == 'GET':
            user_id=int(request.args['user_id'])
            return UsersM.get_user_role_details_for_role_update(user_id)
api.add_resource(get_user_role_details_new,'/get_user_role_details_new')

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
                Stage=request.args.get('Stage',0,type=int)
                response = Assessments.GetBatchAssessments(BatchId,Stage)
                return response 
            except Exception as e:
                return {'exception':str(e)}
api.add_resource(GetBatchAssessments,'/GetBatchAssessments')

class GetBatchAssessmentsHistory(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            try:
                AssessmentId=request.args.get('AssessmentId',0,type=int)               
                response = Assessments.GetBatchAssessmentsHistory(AssessmentId)
                return response 
            except Exception as e:
                return {'exception':str(e)}
api.add_resource(GetBatchAssessmentsHistory,'/GetBatchAssessmentsHistory')

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
            assessment_date=request.form['assessment_date']
            assessment_type_id=request.form['assessment_type_id']
            assessment_agency_id=request.form['assessment_agency_id']
            assessment_id=request.form['assessment_id']
            partner_id=request.form['partner_id']
            current_stage_id=request.form['current_stage_id']
            present_candidate=request.form['Present_Candidate']
            absent_candidate=request.form['Absent_Candidate']
            assessor_name=request.form['Assessor_Name']
            assessor_email=request.form['Assessor_Email']
            assessor_mobile=request.form['Assessor_Mobile']
            reassessment_flag=request.form['reassessment_flag']
            return Assessments.ScheduleAssessment(batch_id,user_id,requested_date,scheduled_date,assessment_date,assessment_type_id,assessment_agency_id,assessment_id,partner_id,current_stage_id,present_candidate,absent_candidate,assessor_name,assessor_email,assessor_mobile,reassessment_flag)
class ConfirmedAssessedAssessmentFromUAP(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            batch_id=Database.get_batchid_from_batch_code(request.form['batch_id'])
            #user_id=request.form['user_id']
            #requested_date=request.form['requested_date']
            scheduled_date=request.form['planned_assessment_date']
            assessment_date=request.form['actual_assessment_date']
            #assessment_type_id=request.form['assessment_type_id']
            #assessment_agency_id=request.form['assessment_agency_id']
            #assessment_id=request.form['assessment_id']
            #partner_id=request.form['partner_id']
            current_stage_id=request.form['stage_id']
            present_candidate=request.form['present_candidate']
            absent_candidate=request.form['absent_candidate']
            assessor_name=request.form['assessor_name']
            assessor_email=request.form['assessor_email']
            assessor_mobile=request.form['assessor_mobile']
            #reassessment_flag=request.form['reassessment_flag']
            return Assessments.ScheduleAssessment(batch_id,1,'',scheduled_date,assessment_date,0,0,-1,0,current_stage_id,present_candidate,absent_candidate,assessor_name,assessor_email,assessor_mobile,0)
class ChangeCertificationStage(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            print(request.form['remark'])
            batch_id = request.form['batch_id']
            batch_code = request.form['batch_code']
            user_id = request.form['user_id']
            current_stage_id = request.form['current_stage_id']
            enrollment_ids = request.form['enrollment_ids']
            sent_printing_date = request.form['sent_printing_date']
            sent_center_date = request.form['sent_center_date']
            expected_arrival_date = request.form['expected_arrival_date']
            received_date = request.form['received_date']
            planned_distribution_date = request.form['planned_distribution_date']
            actual_distribution_date = request.form['actual_distribution_date']
            cg_name = request.form['cg_name']
            cg_desig = request.form['cg_desig']
            cg_org = request.form['cg_org']
            cg_org_loc = request.form['cg_org_loc']
            remark = request.form['remark']
            courier_number = request.form['courier_number']
            courier_name = request.form['courier_name']
            courier_url = request.form['courier_url']
            print(batch_id,batch_code,user_id,current_stage_id,enrollment_ids,sent_printing_date,sent_center_date,expected_arrival_date,received_date,planned_distribution_date,actual_distribution_date,cg_name,cg_desig,cg_org,cg_org_loc,remark,courier_number,courier_name,courier_url)
            return Assessments.ChangeCertificationStage(batch_id,batch_code,user_id,current_stage_id,enrollment_ids,sent_printing_date,sent_center_date,expected_arrival_date,received_date,planned_distribution_date,actual_distribution_date,cg_name,cg_desig,cg_org,cg_org_loc,remark,courier_number,courier_name,courier_url)
api.add_resource(ScheduleAssessment,'/ScheduleAssessment')
api.add_resource(ChangeCertificationStage,'/ChangeCertificationStage')
api.add_resource(ConfirmedAssessedAssessmentFromUAP,'/ConfirmedAssessedAssessmentFromUAP')

api.add_resource(DownloadAssessmentResult,'/DownloadAssessmentResult')
api.add_resource(DownloadAssessmentResultUploadTemplate,'/DownloadAssessmentResultUploadTemplate')
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

@app.route("/Customer_Dashboard_Page")
def Customer_Dashboard_Page():
    if g.user:
        return render_template("Report-powerbi/Customer_Dashboard.html")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/Customer_Dashboard")
def Customer_Dashboard():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="Customer_Dashboard_Page")
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

class ALLCandidatesBasedOnCertifiactionStage(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            try:
                batch_id=request.args.get('batch_id',0,type=int)
                stage_id=request.args.get('stage_id',0,type=int)
                response = Database.ALLCandidatesBasedOnCertifiactionStage(batch_id,stage_id)
                return response 
            except Exception as e:
                return {'exception':str(e)}
api.add_resource(ALLCandidatesBasedOnCertifiactionStage,'/ALLCandidatesBasedOnCertifiactionStage')

class CandidateFamilyDetails(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            try:
                candidate_id=request.args.get('candidate_id',0,type=int)
                response = Database.CandidateFamilyDetails(candidate_id)
                return response 
            except Exception as e:
                return {'exception':str(e)}
api.add_resource(CandidateFamilyDetails,'/CandidateFamilyDetails')

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
#################################################################################

@app.route("/sub_project_list_page")
def sub_project_list_page():
    if g.user:
        project_id=request.args.get('project_id',0,type=int)
        customer_id=request.args.get('customer_id',0,type=int)
        print(project_id)
        return render_template("Master/sub-project-list.html",project_id=project_id,customer_id=customer_id)
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/sub_project")
def sub_project():
    if g.user:
        project_id=request.args.get('project_id',0,type=int)
        customer_id=request.args.get('customer_id',0,type=int) 
        print(project_id)
        html_str="sub_project_list_page?project_id=" + str(project_id)+"&customer_id="+ str(customer_id)
        return render_template("home.html",values=g.User_detail_with_ids,html=html_str)
    else:
        return render_template("login.html",error="Session Time Out!!")

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

class sub_project_list(Resource):
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
            customer_status = request.form['customer_status']  
            user_id = request.form['user_id']
            user_role_id = request.form['user_role_id'] 
            user_region_id = request.form['user_region_id']
            project=request.form['project']
            start_index = request.form['start']
            page_length = request.form['length']
            search_value = request.form['search[value]']
            order_by_column_position = request.form['order[0][column]']
            order_by_column_direction = request.form['order[0][dir]']
            draw=request.form['draw']
            #print(user_id,user_role_id,user_region_id,entity,customer,p_group,block,practice,bu,product,status)
            return Master.sub_project_list(user_id,user_role_id,user_region_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw,entity,customer,p_group,block,practice,bu,product,status,project,customer_status)
api.add_resource(sub_project_list, '/sub_project_list')

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
            project_code = request.form['project_id']      
            isactive=request.form['isactive']
            is_ojt_req=request.form['is_ojt_req']
            mobilization_type=request.form['mobilization_type']
            
            return Master.add_subproject_details(SubProjectName, SubProjectCode, Region, State, Centers, Course, PlannedStartDate, PlannedEndDate, ActualStartDate, ActualEndDate, user_id, subproject_id, project_code, isactive, is_ojt_req, mobilization_type)
api.add_resource(add_subproject_details,'/add_subproject_details')

#############################################################################
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
                batch = request.form["batch"]
                region = request.form["region"]
                center = request.form["center"]
                center_type = request.form["center_type"]
                Contracts = request.form["Contracts"]
                candidate_stage = request.form["candidate_stage"]
                from_date = request.form["from_date"]
                to_date = request.form["to_date"]
                #print(Contracts, candidate_stage, from_date, to_date)
                
                file_name='candidate_report_'+str(user_id) +'_'+ str(datetime.now().strftime('%Y%m%d_%H%M%S'))+'.xlsx'
                #print(candidate_id, user_id, user_role_id, status, customer, project, sub_project, region, center, center_type, file_name)

                resp = candidate_report.create_report(candidate_id, user_id, user_role_id, status, customer, project, sub_project, batch, region, center, center_type, file_name,Contracts, candidate_stage, from_date, to_date)
                
                return resp
                #return {'FileName':"abc.excel",'FilePath':'lol', 'download_file':''}
            except Exception as e:
                #print(str(e))
                return {"exceptione":str(e)}
api.add_resource(candidate_download_report,'/candidate_download_report')

#PLACEMENT AGEING

@app.route("/candidate_placement_ageing_page")
def candidate_placement_ageing_page():
    if g.user:
        return render_template("Reports/candidate_placement_ageing.html")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/candidate_placement_ageing")
def candidate_placement_ageing():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="candidate_placement_ageing_page")
    else:
        return render_template("login.html",error="Session Time Out!!")

class GetPlacementAgeingReportData(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            try:
                user_id=request.args.get('user_id',0,type=int)
                user_role_id=request.args.get('user_role_id',0,type=int)
                customer_ids=request.args.get('customer_ids','',type=str)
                contract_ids=request.args.get('contract_ids','',type=str)
                from_date=request.args.get('from_date','',type=str)
                to_date=request.args.get('to_date','',type=str)
                status_id=request.args.get('status_id',-1,type=int)
                stage_ids=request.args.get('stage_ids','',type=str)

                response = Report.GetPlacementAgeingReportData(user_id,user_role_id,customer_ids,contract_ids,from_date,to_date, status_id, stage_ids)
                return response 
            except Exception as e:
                return {'exception':str(e)}
api.add_resource(GetPlacementAgeingReportData,'/GetPlacementAgeingReportData')


class GetCandidatesBasedOnPlacementStage(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            try:
                user_id=request.args.get('user_id',0,type=int)
                user_role_id=request.args.get('user_role_id',0,type=int)
                placement_stage=request.args.get('placement_stage',0,type=int)
                sub_project_code=request.args.get('sub_project_code','',type=str)
                customer_ids=request.args.get('customer_ids','',type=str)
                contract_ids=request.args.get('contract_ids','',type=str)                
                from_date=request.args.get('from_date','',type=str)
                to_date=request.args.get('to_date','',type=str)
                status_id=request.args.get('status_id',-1,type=int)
                stage_ids=request.args.get('stage_ids','',type=str)
                   
                response = Report.GetCandidatesBasedOnPlacementStage(user_id,user_role_id,placement_stage,sub_project_code,customer_ids,contract_ids,from_date,to_date, status_id, stage_ids)
                return response 
            except Exception as e:
                return {'exception':str(e)}
api.add_resource(GetCandidatesBasedOnPlacementStage,'/GetCandidatesBasedOnPlacementStage')

class GetPlacementAgeingReportDonload(Resource):
    @staticmethod
    def get():
        if request.method == 'GET':
            user_id=request.args.get('user_id',0,type=int)
            user_role_id=request.args.get('user_role_id',0,type=int)
            customer_ids=request.args.get('customer_ids','',type=str)
            contract_ids=request.args.get('contract_ids','',type=str)
            from_date=request.args.get('from_date','',type=str)
            to_date=request.args.get('to_date','',type=str)
            status_id=request.args.get('status_id',-1,type=int)
            stage_ids=request.args.get('stage_ids','',type=str)
            
            resp = Report.GetPlacementAgeingReportDonload(user_id,user_role_id,customer_ids,contract_ids,from_date,to_date, status_id, stage_ids)
            return resp
api.add_resource(GetPlacementAgeingReportDonload,'/GetPlacementAgeingReportDonload')

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
                customer_ids=request.args.get('customer_ids','',type=str)
                contract_ids=request.args.get('contract_ids','',type=str)
                region_ids=request.args.get('region_ids','',type=str)
                from_date=request.args.get('from_date','',type=str)
                to_date=request.args.get('to_date','',type=str)
                stage_ids=request.args.get('stage_ids','',type=str)
                status_id=request.args.get('status_id',0,type=int)
                response = Report.GetECPReportData(user_id,user_role_id,customer_ids,contract_ids,region_ids,from_date,to_date,stage_ids,status_id)
                return response 
            except Exception as e:
                return {'exception':str(e)}
api.add_resource(GetECPReportData,'/GetECPReportData')
###############################################################################

class GetContractsBasedOnCustomer(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            try:
                user_id=request.args.get('user_id',0,type=int)
                user_role_id=request.args.get('user_role_id',0,type=int)
                customer_id=request.args.get('customer_id','',type=str)
                response = Master.GetContractsBasedOnCustomer(user_id,user_role_id,customer_id)
                return response 
            except Exception as e:
                return {'exception':str(e)}
api.add_resource(GetContractsBasedOnCustomer,'/GetContractsBasedOnCustomer')

class GetContractsBasedOnCustomerAndStage(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            try:
                user_id=request.args.get('user_id',0,type=int)
                user_role_id=request.args.get('user_role_id',0,type=int)
                customer_id=request.args.get('customer_id','',type=str)
                contract_stage_ids=request.args.get('contract_stage_ids','',type=str)
                response = Master.GetContractsBasedOnCustomerAndStage(user_id,user_role_id,customer_id,contract_stage_ids)
                return response 
            except Exception as e:
                return {'exception':str(e)}
api.add_resource(GetContractsBasedOnCustomerAndStage,'/GetContractsBasedOnCustomerAndStage')


class GetBillingMilestones(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            response={"BillingMilestones":Master.GetBillingMilestones()}
            return response
api.add_resource(GetBillingMilestones,'/GetBillingMilestones')

class GetUnitTypes(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            response={"UnitTypes":Master.GetUnitTypes()}
            return response
api.add_resource(GetUnitTypes,'/GetUnitTypes')

class SaveProjectBillingMilestones(Resource):
    @staticmethod
    def post():
        if request.method=='POST':            
            json_string=''
            if 'JsonString' in request.form:
                json_string=request.form["JsonString"] 
            project_id=0
            if 'project_id' in request.form:
                project_id=request.form["project_id"]
            user_id=0
            if 'user_id' in request.form:
                user_id=request.form["user_id"] 
                           
            return Master.SaveProjectBillingMilestones(json_string,project_id,user_id)
api.add_resource(SaveProjectBillingMilestones,'/SaveProjectBillingMilestones')

class GetProjectMilestones(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            project_id=request.args.get('project_id',0,type=int)
            response={"MileStones":Master.GetProjectMilestones(project_id)}
            return response
api.add_resource(GetProjectMilestones,'/GetProjectMilestones')

class GetSubProjectCourseMilestones(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            sub_project_id=request.args.get('sub_project_id',0,type=int)
            course_id=request.args.get('course_id',0,type=int)
            response={"MileStones":Master.GetSubProjectCourseMilestones(sub_project_id,course_id)}
            return response
api.add_resource(GetSubProjectCourseMilestones,'/GetSubProjectCourseMilestones')

class SaveSubProjectCourseMilestones(Resource):
    @staticmethod
    def post():
        if request.method=='POST':            
            json_string=''
            if 'JsonString' in request.form:
                json_string=request.form["JsonString"] 
            sub_project_id=0
            if 'sub_project_id' in request.form:
                sub_project_id=request.form["sub_project_id"]
            user_id=0
            if 'user_id' in request.form:
                user_id=request.form["user_id"] 
                           
            return Master.SaveSubProjectCourseMilestones(json_string,sub_project_id,user_id)
api.add_resource(SaveSubProjectCourseMilestones,'/SaveSubProjectCourseMilestones')

class GetCoursesBasedOnSubProject(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            sub_project_id=request.args.get('sub_project_id',0,type=int)
            response={"Courses":Master.GetCoursesBasedOnSubProject(sub_project_id)}
            return response
api.add_resource(GetCoursesBasedOnSubProject,'/GetCoursesBasedOnSubProject')

class GetUsersBasedOnSubProject(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            sub_project_id=request.args.get('sub_project_id',0,type=int)
            response={"Users":Master.GetUsersBasedOnSubProject(sub_project_id)}
            print(response)
            return response
api.add_resource(GetUsersBasedOnSubProject,'/GetUsersBasedOnSubProject')

class GetUserListForSubProject(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            sub_project_id=request.args.get('sub_project_id',0,type=int)
            response={"Users":Master.GetUserListForSubProject(sub_project_id)}
            return response
api.add_resource(GetUserListForSubProject,'/GetUserListForSubProject')
class GetCentersbasedOnSubProject(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            sub_project_id=request.args.get('sub_project_id',0,type=int)
            response={"Centers":Master.GetCentersbasedOnSubProject(sub_project_id)}
            return response
api.add_resource(GetCentersbasedOnSubProject,'/GetCentersbasedOnSubProject')

class GetTrainersBasedOnType(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            trainer_flag=request.args.get('trainer_flag',0,type=int)
            response={"Users":Master.GetTrainersBasedOnType(trainer_flag)}
            return response
api.add_resource(GetTrainersBasedOnType,'/GetTrainersBasedOnType')

class GetUsersBasedOnRole(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            user_role_id=request.args.get('user_role_id',0,type=int)
            #print(user_role_id)
            response={"Users":Master.GetUsersBasedOnRole(user_role_id)}
            #print(response)
            return response
api.add_resource(GetUsersBasedOnRole,'/GetUsersBasedOnRole')

class GetUserRole(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            response={"UserRole":Master.GetUserRole()}
            return response
api.add_resource(GetUserRole,'/GetUserRole')

class SaveSubProjectCourseCenterUnitPrice(Resource):
    @staticmethod
    def post():
        if request.method=='POST':            
            json_string=''
            if 'JsonString' in request.form:
                json_string=request.form["JsonString"] 
            primary_key_id=0
            if 'primary_key_id' in request.form:
                primary_key_id=request.form["primary_key_id"]
            user_id=0
            if 'user_id' in request.form:
                user_id=request.form["user_id"] 
                           
            return Master.SaveSubProjectCourseCenterUnitPrice(json_string,primary_key_id,user_id)
api.add_resource(SaveSubProjectCourseCenterUnitPrice,'/SaveSubProjectCourseCenterUnitPrice')

class GetSubProjectCourseCenterUnitRates(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            sub_project_id=request.args.get('sub_project_id',0,type=int)
            primary_key=request.args.get('primary_key',0,type=int)
            response={"Centers":Master.GetSubProjectCourseCenterUnitRates(sub_project_id,primary_key)}
            return response
api.add_resource(GetSubProjectCourseCenterUnitRates,'/GetSubProjectCourseCenterUnitRates')


class check_user_pass(Resource):
    @staticmethod
    def get():
        if request.method == 'GET':
            client_id = str(request.args['client_id'])
            client_key = str(request.args['client_key'])
            username = str(request.args['username'])
            password = str(request.args['password'])
            app_version = str(request.args['app_version'])
            device_model = str(request.args['device_model'])
            imei_num = str(request.args['imei_num'])
            android_version = str(request.args['android_version'])

            if (client_id==config.API_secret_id) and (client_key==config.API_secret_key):
                out = Database.check_password(username,password,app_version,device_model,imei_num,android_version)
            else:
                out = {'success': False, 'description': "client name and password not matching", 'app_status':True}
            return jsonify(out)

#Base URL + "/login" api will provide all the unzynched QP data as response
api.add_resource(check_user_pass, '/login')

class otp_send(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            client_id = str(request.form['client_id'])
            client_key = str(request.form['client_key'])
            if (client_id==config.API_secret_id) and (client_key==config.API_secret_key):
                try:
                    flag = int(request.form['flag'])
                    mobile_no = str(request.form['mobile_no'])
                    app_name = str(request.form['app_name'])
                    cand_name = str(request.form['cand_name'])
                    is_otp=1
                    if 'is_otp' in request.form:
                        is_otp=int(request.form['is_otp'])
                    candidate_id=0
                    if 'candidate_id' in request.form:
                        candidate_id=int(request.form['candidate_id'])
                except Exception as e:
                    res = {'success': False, 'description': "unable to read data " + str(e)}
                    return jsonify(res)
                otp = ''
                for i in range(6):
                    otp += str(random.randint(0,9))

                out = Database.otp_send_db(otp, mobile_no, app_name, flag,candidate_id)
                print(out)
                if out[0]:
                    res = {'success': False, 'description': "Mobile number already registered"}
                    return jsonify(res)
                else:
                    otp=out[1]
                    def sendSMS(apikey, numbers, sender, message):
                        #make parameter value of test as True for testing to save the msg credits.
                        data =  urllib.parse.urlencode({'apikey': apikey, 'numbers': numbers, 'message' : message.encode('utf-8'), 'sender': sender,'test':False,'tracking_links':True})
                        data = data.encode('utf-8')
                        request = urllib.request.Request("https://api.textlocal.in/send/?")
                        f = urllib.request.urlopen(request, data)
                        fr = f.read()
                        return(fr)
                    #short_url='{}/wv?n={}&m={}&o={}'.format(config.Base_URL,cand_name.replace(' ','%20'),mobile_no,otp)
                    name=cand_name[0:18] if len(cand_name)>=18 else cand_name
                    param={"n":name,"m":mobile_no,"o":otp}
                    param_str=urllib.parse.urlencode(param)
                    short_url='{}/wv?'.format(config.Base_URL)
                    short_url=short_url+param_str
                    #sms_msg=   'Hi {},\n\nThank you for getting in touch with Labournet.\nYour OTP is {}.\n\nThanks,\nNEO Teams.'.format(cand_name, otp)
                    #sms_msg='Hi {},\n\nYour OTP is {}.\nOR\nClick here to verify {}\n\nThanks,\nNEO Team.'.format(name, otp,short_url)
                    if is_otp==1:
                        sms_msg='Hi {},\n\nThank you for getting in touch with Labournet.\nYour OTP for mobile number verification is {}.\n\nThanks,\nNEO Teams.'.format(name, otp)
                        #sms_msg='Hi {},\n\nThank you for getting in touch with Labournet.\nYour Registration Number is {}.\n\nThanks,\nNEO Teams.'.format(name, otp)
                    elif is_otp==0:
                        sms_msg='Hi {},\n\nClick to verify your mobile number with Labournet.{}.\n\nNEO Team.'.format(name,short_url)
                    #print(sms_msg)
                    resp =  sendSMS('vAHJXKhB9AY-bJF1Ozs3XkCW2uv6UYRiHShavkGySL', '91{}'.format(mobile_no), 'NEOLNS'.upper(),sms_msg)
                    #print (resp)
                    data = json.loads(resp.decode("utf-8"))
                    if data['status'] == 'success':
                        res = {'success': True, 'description': "SMS Sent Successfully"}
                        return jsonify(res)
                    else:
                        res = {'success': False, 'description': data['errors'][0]['message']}
                        return jsonify(res)
            else:
                res = {'success': False, 'description': "client name and password not matching"}
                return jsonify(res)
        else:
            res = {'success': False, 'description': "Method is wrong"}
            return jsonify(res)

#Base URL + "/otp_send" api will do mobile number verificaiton in web and app.
api.add_resource(otp_send, '/otp_send')

class otp_verification(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            client_id = str(request.form['client_id'])
            client_key = str(request.form['client_key'])

            if (client_id==config.API_secret_id) and (client_key==config.API_secret_key):
                try:
                    otp = str(request.form['otp'])
                    mobile_no = str(request.form['mobile_no'])
                    app_name = str(request.form['app_name'])
                    web_flag=0
                    if 'web_flag' in request.form:
                        web_flag=request.form['web_flag']
                except Exception as e:
                    res = {'success': False, 'description': "unable to read data " + str(e)}
                    return jsonify(res)
                out = Database.otp_verification_db(otp, mobile_no, app_name,web_flag)

                if out==True:
                    res = {'success': True, 'description': "Mobile number verified successfully"}
                else:
                    res = {'success': False, 'description': "Mobile number verification failed"}
                
                return jsonify(res)   
                
            else:
                res = {'success': False, 'description': "client name and password not matching"}
                return jsonify(res)
        else:
            res = {'success': False, 'description': "Method is wrong"}
            return jsonify(res)

#Base URL + "/otp_verification" api will provide all the unzynched QP data as response
api.add_resource(otp_verification, '/otp_verification')

class get_candidate_list_updated(Resource):
    @staticmethod
    def get():
        if request.method == 'GET':
            client_id = str(request.args['client_id'])
            client_key = str(request.args['client_key'])
            
            user_id = int(request.args['user_id'])
            role_id = int(request.args['role_id'])
            #user_id = 'NULL' if user_id==0 else user_id
            cand_stage = int(request.args['cand_stage'])
            #cand_stage = 'NULL' if cand_stage==0 else cand_stage
            app_version = request.args['app_version']
            
            if (client_id==config.API_secret_id) and (client_key==config.API_secret_key):
                out = Database.get_candidate_list_updated(user_id,role_id,cand_stage,app_version)
                return jsonify(out)
                
            else:
                res = {'success': False, 'description': "client name and password not matching", 'app_status':True}
                return jsonify(res)

#Base URL + "/get_candidate_list" api will provide all the unzynched QP data as response
api.add_resource(get_candidate_list_updated, '/get_candidate_list_updated')

@app.route("/XML/<path:path>")
def get_xml_file(path):
    """Download a file."""
    filename = r"{}{}".format(config.candidate_xmlPath,path)
    #print(filename)
    if not(os.path.exists(filename)):
        filename = r"{}No-image-found.jpg".format(config.ReportDownloadPathWeb)
    return send_file(filename)

class submit_candidate_updated(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            client_id = str(request.form['client_id'])
            client_key = str(request.form['client_key'])
            
            user_id = int(request.form['user_id'])
            role_id = int(request.form['role_id'])
            cand_stage = int(request.form['cand_stage'])
            xml = str(request.form['xml'])
            latitude = str(request.form['latitude'])
            longitude = str(request.form['longitude'])
            timestamp = str(request.form['timestamp'])
            app_version = str(request.form['app_version'])
            device_model = str(request.form['device_model'])
            imei_num = str(request.form['imei_num'])
            android_version = str(request.form['android_version'])
            if (client_id==config.API_secret_id) and (client_key==config.API_secret_key):
                if cand_stage==1:
                    out = Database.get_submit_candidate_mobi(user_id, role_id, xml, latitude, longitude, timestamp, app_version,device_model,imei_num,android_version)
                elif cand_stage==2:
                    out = Database.get_submit_candidate_reg(user_id, role_id, xml, latitude, longitude, timestamp, app_version,device_model,imei_num,android_version)
                elif cand_stage==3:
                    out = Database.get_submit_candidate_enr(user_id, role_id, xml, latitude, longitude, timestamp, app_version,device_model,imei_num,android_version)
                elif cand_stage==4:
                    out = Database.get_submit_candidate_re_enr(user_id, role_id, xml, latitude, longitude, timestamp, app_version,device_model,imei_num,android_version)
                else:
                    out = {'success': False, 'validation_error':False, 'description': "incorrect stage", 'app_status':True}
                return jsonify(out)
            
            else:
                res = {'success': False, 'validation_error':False, 'description': "client name and password not matching", 'app_status':True}
                return jsonify(res)

#Base URL + "/submit_candidate_updated" api will provide all the unzynched QP data as response
api.add_resource(submit_candidate_updated, '/submit_candidate_updated')


class GetContractProjectTargets(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            try:
                contact_id=request.args.get('contract_id',0,type=int)
                user_id=request.args.get('user_id',0,type=int)
                user_role_id=request.args.get('user_role_id',0,type=int)
                region_id=request.args.get('region_id',0,type=int)
                from_date=request.args.get('from_date','',type=str)
                to_date=request.args.get('to_date','',type=str)
                   
                response = {"Targets":Master.GetContractProjectTargets(contact_id,user_id,user_role_id,region_id,from_date,to_date)}
                return response 
            except Exception as e:
                return {'exception':str(e)}
api.add_resource(GetContractProjectTargets,'/GetContractProjectTargets')

class get_batch_list_updated(Resource):
    @staticmethod
    def get():
        if request.method == 'GET':
            client_id = str(request.args['client_id'])
            client_key = str(request.args['client_key'])
            
            user_id = int(request.args['user_id'])
            candidate_id = int(request.args['candidate_id'])
            role_id = int(request.args['role_id'])
            mobilization_type=request.args.get('mobilization_type',1,type=int)
            if (client_id==config.API_secret_id) and (client_key==config.API_secret_key):
                out = Database.get_batch_list_updated(user_id,candidate_id,role_id,mobilization_type)
                return jsonify(out)
                
            else:
                res = {'success': False, 'description': "client name and password not matching"}
                return jsonify(res)

#Base URL + "/get_candidate_list" api will provide all the unzynched QP data as response
api.add_resource(get_batch_list_updated, '/get_batch_list_updated')

@app.route("/mobilization_page")
def mobilization_page():
    if g.user:
        #status=request.args.get('status',-1,type=int)
        return render_template("Candidate/mobilization_list.html")
    else:
        return render_template("login.html",error="Session Time Out!!")


@app.route("/mobilization")
def mobilization():
    if g.user:
        #status=request.args.get('status',-1,type=int) 
        html_str="mobilization_page"    #?status=" + str(status)
        return render_template("home.html",values=g.User_detail_with_ids,html=html_str)
    else:
        return render_template("login.html",error="Session Time Out!!")

class mobilized_list_updated(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            candidate_id=request.form['candidate_id']
            region_ids=request.form['region_ids']
            state_ids = request.form["state_ids"]
            MinAge=request.form['MinAge']
            MaxAge = request.form["MaxAge"]
            created_by = request.form["created_by"]
            ToDate = request.form["ToDate"]
            FromDate = request.form["FromDate"]
            search_type = request.form["search_type"]
            search_keyword = request.form["search_keyword"]
            
            user_id = request.form["user_id"]
            user_role_id = request.form["user_role_id"]
            
            start_index = request.form['start']
            page_length = request.form['length']
            search_value = request.form['search[value]']
            order_by_column_position = request.form['order[0][column]']
            order_by_column_direction = request.form['order[0][dir]']
            draw=request.form['draw']
            
            return Candidate.mobilized_list(candidate_id,region_ids, state_ids, MinAge, MaxAge,search_type,search_keyword, user_id, user_role_id, start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw,created_by,FromDate, ToDate)
api.add_resource(mobilized_list_updated, '/mobilized_list_updated')

class DownloadMobTemplate(Resource):
    report_name = "Trainerwise_TMA_Registration_Compliance"+datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    @staticmethod
    def post():
        if request.method=='POST':
            try:
                user_id = request.form["user_id"]
                user_role_id = request.form["user_role_id"]
                Project_Tpye = int(request.form["Project_Tpye"])
                if Project_Tpye==1:
                    filename = 'CandidateBulkUpload_Mobilization_DELL.xlsx'
                elif Project_Tpye==2:
                    filename = 'CandidateBulkUpload_Mobilization_SHE.xlsx'
                else:
                    filename = 'CandidateBulkUpload_Mobilization.xlsx'
                
                return {'Description':'Downloaded Template', 'Status':True, 'filename':filename}
            except Exception as e:
                #print(str(e))
                return {"exceptione":str(e)}
api.add_resource(DownloadMobTemplate,'/DownloadMobTemplate')

class upload_bulk_upload(Resource):
    @staticmethod
    def post():
        if request.method=='POST':
            #try:
            f = request.files['filename']
            cand_stage =request.form['cand_stage']
            user_id = request.form["user_id"]
            user_role_id = request.form["user_role_id"]
            ProjectType = int(request.form["ProjectType"])
            All_Filenames = request.form["All_Filenames"]
            filename_prefix = request.form["filename_prefix"]
            
            #print (f.filename, cand_stage,user_id,user_role_id,ProjectType,All_Filenames,filename_prefix)
            all_image_files = [] if All_Filenames=='' else All_Filenames.split(',')

            file_name = config.bulk_upload_path + str(user_id) + '_'+ str(datetime.now().strftime('%Y%m%d_%H%M%S'))+'_'+f.filename
            f.save(file_name)
            all_email=Database.all_email_validation(cand_stage)
            email_validation = [CustomElementValidation(lambda d: d.lower() in all_email, 'Invalid mobilizer')]
            all_state=Database.all_state_validation()
            
            #regex = r'^[A-Za-z0-9]+[\._A-Za-z0-9]+[@]\w+[.]\w+$'
            #regex = r'^[A-Za-z0-9]+[\._A-Za-z0-9]+[@]\w+[\.A-Za-z]+\w+$'
            regex = r'^[A-Za-z0-9]+[\._A-Za-z0-9]+[A-Za-z0-9]+[@]\w+[.][\.A-Za-z]+\w+$'
            regex2 = '[\.]{2,}'
            state_validation = [CustomElementValidation(lambda d: d.lower() in all_state, 'Invalid State')]
            cand_email_format_validation = [CustomElementValidation(lambda d: ((re.search(regex2,d)==None)and(re.search(regex,d)!=None)), 'Inavalid email format. Please provide correct email')]
            cand_email_validation = [CustomElementValidation(lambda d: Database.app_email_validation(d.lower()), 'Email already exists')]
            cand_mobile_validation = [CustomElementValidation(lambda d: Database.app_mobile_validation(d), 'mobile number already exists')]
            pass_fail_validation = [CustomElementValidation(lambda d: str(d).lower() in ['pass','fail'], 'invalid option (Pass/Fail allwed)')]
            images_validation = [CustomElementValidation(lambda d: d in all_image_files, 'Image not available with this name.')]
            
            #dob_validation = [CustomElementValidation(lambda d: , 'invalid format. please provide in "MM-DD-YYYY')]
            if cand_stage==str(1):
                df= pd.read_excel(file_name,sheet_name='Mobilizer')
                if len(df['Primary contact  No*'])!=len(df['Primary contact  No*'].unique()):
                    return {"Status":False, "message":"Duplicate Primary contact No Not Allowed"}
                elif len(df['Email id*'])!=len(df['Email id*'].unique()):
                    return {"Status":False, "message":"Duplicate Email Id Not Allowed"}
                elif df.values.tolist() == []:
                    return {"Status":False, "message":"Please fill all the mandatory fileds to uplaod the file" }
                df = df.fillna('')
                df['date_age']=df['Age*'].astype(str)+df['Date of Birth*'].astype(str)
                schema = Schema([
                        #nan check column non mandate
                        Column('Candidate Photo',null_validation),
                        Column('Middle Name',null_validation),
                        Column('Last Name',null_validation),
                        Column('Secondary Contact  No',null_validation),
                        Column('Email id*',cand_email_validation + cand_email_format_validation + str_validation + null_validation),
                        Column('Present Panchayat',null_validation),
                        Column('Present Taluk/Block',null_validation),
                        Column('Present Address line1',null_validation),
                        Column('Present Address line2',null_validation),
                        Column('Present Village',null_validation),
                        Column('Permanent Address line1',null_validation),
                        Column('Permanent Address line2',null_validation),
                        Column('Permanent Village',null_validation),
                        Column('Permanent Panchayat',null_validation),
                        Column('Permanent Taluk/Block',null_validation),
                        Column('Whatsapp Number',mob_validation + null_validation),
                        #str+null check
                        Column('Fresher/Experienced?*',str_validation + null_validation),
                        Column('Salutation*',str_validation + null_validation),
                        Column('First Name*',str_validation + null_validation),
                        Column('Gender*',str_validation + null_validation),
                        Column('Marital Status*',str_validation + null_validation),
                        Column('Caste*',str_validation + null_validation),
                        Column('Disability Status*',str_validation + null_validation),
                        Column('Religion*',str_validation + null_validation),
                        Column('Source of Information*',str_validation + null_validation),
                        Column('Present District*',str_validation + null_validation),
                        Column('Present State*',state_validation + str_validation + null_validation),
                        Column('Present Country*',str_validation + null_validation),
                        Column('Permanent District*',str_validation + null_validation),
                        Column('Permanent State*',state_validation + str_validation + null_validation),
                        Column('Permanent Country*',str_validation + null_validation),
                        #pincode check
                        Column('Present Pincode*',pincode_validation + null_validation),
                        Column('Permanent Pincode*',pincode_validation + null_validation),
                        #mobile number check
                        Column('Primary contact  No*',cand_mobile_validation + mob_validation + null_validation),
                        #date of birth and age pass(null check)
                        Column('Date of Birth*',null_validation),
                        Column('Age*',null_validation),
                        Column('date_age',dob_validation),
                        #Email validation
                        Column('Mobilized By*',email_validation+str_validation)
                        ])
                errors = schema.validate(df)
                errors_index_rows = [e.row for e in errors]

                #df_clean = df.drop(index=errors_index_rows)
                #df_clean.to_csv('clean_data.csv',index=None)
                len_error = len(errors_index_rows)
                os.remove(file_name)
                if len_error>0:
                    file_name = str(user_id) + '_'+ str(datetime.now().strftime('%Y%m%d_%H%M%S'))+'_' + 'errors.csv'
                    pd.DataFrame({'col':errors}).to_csv(config.bulk_upload_path + 'Error/' + file_name)
                    return {"Status":False, "message":"Validation_Error", "error":"Validation Error <a href='/Bulk Upload/Error/{}' >Download error log</a>".format(file_name) }
                else:
                    out = Database.mobilization_web_inser(df,user_id,ProjectType)
                    return out

            elif cand_stage==str(2):
                df= pd.read_excel(file_name,sheet_name='Registration')
                df = df.fillna('')
                df['date_age']=df['Age*'].astype(str)+df['Date of Birth*'].astype(str)
                df['ids']=df['Aadhar No'].astype(str)+df['Identity number'].astype(str)
                #print(df.columns.to_list())
                if ProjectType==1:
                    #print(df['Candidate Photo*'])
                    img_column ='Candidate Photo*,Aadhar Image,Document copy,Income Certificate,Educational Marksheet*'
                    schema = Schema([
                        #nan check column non mandate
                        Column('Candidate_id',null_validation),
                        Column('Middle Name',null_validation),
                        Column('Last Name',null_validation),
                        Column('Secondary Contact  No',null_validation),
                        Column('Email id*',str_validation + null_validation),
                        Column('Present Panchayat',null_validation),
                        Column('Present Taluk/Block',null_validation),
                        Column('Present Address line1',null_validation),
                        Column('Present Address line2',null_validation),
                        Column('Present Village',null_validation),
                        Column('Permanent Address line1',null_validation),
                        Column('Permanent Address line2',null_validation),
                        Column('Permanent Village',null_validation),
                        Column('Permanent Panchayat',null_validation),
                        Column('Permanent Taluk/Block',null_validation),
                        Column('Document copy',null_validation),
                        Column('BOCW Registration Id',null_validation),
                        Column('Whatsapp Number',mob_validation + null_validation),
                        Column('Aadhar Image',null_validation),
                        Column('Educational Marksheet*', null_validation),
                        
                        
                        #str+null check
                        Column('Candidate Photo*', null_validation),
                        Column('Fresher/Experienced?*',str_validation + null_validation),
                        Column('Salutation*',str_validation + null_validation),
                        Column('First Name*',str_validation + null_validation),
                        Column('Gender*',str_validation + null_validation),
                        Column('Marital Status*',str_validation + null_validation),
                        Column('Caste*',str_validation + null_validation),
                        Column('Disability Status*',str_validation + null_validation),
                        Column('Religion*',str_validation + null_validation),
                        Column('Mother Tongue*',str_validation + null_validation),
                        Column('Occupation*',str_validation + null_validation),
                        Column('Average annual income*',str_validation + null_validation),
                        Column('Source of Information*',str_validation + null_validation),
                        Column('Interested Course*',str_validation + null_validation),
                        Column('Product*',str_validation + null_validation),
                        Column('Present District*',str_validation + null_validation),
                        Column('Present State*',state_validation + str_validation + null_validation),
                        Column('Present Country*',str_validation + null_validation),
                        Column('Permanent District*',str_validation + null_validation),
                        Column('Permanent State*',state_validation + str_validation + null_validation),
                        Column('Permanent Country*',str_validation + null_validation),                            
                        Column('Employment Type*',str_validation + null_validation),
                        Column('Preferred Job Role*',str_validation + null_validation),
                        Column('Years Of Experience*',str_validation + null_validation),
                        Column('Relevant Years of Experience*',str_validation + null_validation),
                        Column('Current/Last CTC*',str_validation + null_validation),
                        Column('Preferred Location*',str_validation + null_validation),
                        Column('Willing to travel?*',str_validation + null_validation),
                        Column('Willing to work in shifts?*',str_validation + null_validation),
                        Column('Expected CTC*',str_validation + null_validation),
                        #pincode check
                        Column('Present Pincode*',pincode_validation + null_validation),
                        Column('Permanent Pincode*',pincode_validation + null_validation),
                        #mobile number check
                        Column('Primary contact  No*',mob_validation + null_validation),
                        #date of birth and age pass(null check)
                        Column('Date of Birth*',null_validation),
                        Column('Age*',null_validation),
                        Column('date_age',dob_validation),
                        #ID Validation pass(null check)
                        Column('Aadhar No',null_validation),
                        Column('Identifier Type',null_validation),
                        Column('Identity number',null_validation),
                        Column('ids',null_validation),
                        #Email validation
                        Column('Registered by*',email_validation+str_validation),
                        #DELL
                        Column('Aspirational District*',str_validation + null_validation),
                        Column('Income Certificate', null_validation)
                        ])
                else:
                    if ProjectType==2:
                        df_MCL= pd.read_excel(file_name,sheet_name='SHE MCL')
                        df_MCL = df_MCL.fillna('')
                        schema_MCL = Schema([
                            #nan check column non mandate
                            Column('Candidate_id',null_validation),
                            Column('First Name*',str_validation + null_validation),
                            Column('Primary contact  No*',mob_validation + null_validation),
                            Column('Email id*',str_validation + null_validation),

                            Column('Date of birth -Is age between 18 to 40?',yea_no_validation + null_validation),
                            Column('Are you 8th Pass?',yea_no_validation + null_validation),
                            Column('Are you able to read and write local language?',yea_no_validation + null_validation),
                            Column('Do you have a smart phone?',yea_no_validation + null_validation),
                            Column('Are you??willing to buy a smartphone?',yea_no_validation + null_validation),
                            Column('Do you own two wheeler?',yea_no_validation + null_validation),
                            Column('Do you have any work experience',yea_no_validation + null_validation),
                            Column('Will you able to work full time or at least 6 hours a day?',yea_no_validation + null_validation),
                            Column('Are you willing to serve the community at this time of COVID-19 pandemic as Sanitization & Hygiene Entrepreneurs (SHE)?',yea_no_validation + null_validation),
                            Column('Willing to travel for work',yea_no_validation + null_validation),
                            Column('Are you willing to work and sign the work contract with LN?',yea_no_validation + null_validation),
                            Column('Are you willing to adopt digital transactions in your business?',yea_no_validation + null_validation),
                            Column('Do you have a bank account?',yea_no_validation + null_validation),
                            Column('Have you availed any loan in the past?',yea_no_validation + null_validation),
                            Column('Do you have any active loan?',yea_no_validation + null_validation),
                            Column('Are you willing to take up a loan to purchase tools and consumables?',yea_no_validation + null_validation),
                            Column('Are you covered under any health insurance?',yea_no_validation + null_validation),
                            Column('Are you allergic to any chemicals and dust?',yea_no_validation + null_validation),
                            Column('Are you willing to follow  Environment, Health and Safety Norms in your business?',yea_no_validation + null_validation),
                            Column('Have you ever been subjected to any legal enquiry for Non ethical work/business?',yea_no_validation + null_validation),
                            Column('Result',pass_fail_validation + null_validation)
                            ])

                    img_column ='Aadhar Image,Document copy,Educational Marksheet'
                    schema = Schema([
                        #nan check column non mandate
                        Column('Candidate_id',null_validation),
                        #Column('Candidate Photo',null_validation),
                        Column('Middle Name',null_validation),
                        Column('Last Name',null_validation),
                        Column('Secondary Contact  No',null_validation),
                        Column('Email id*',str_validation + null_validation),
                        Column('Present Panchayat',null_validation),
                        Column('Present Taluk/Block',null_validation),
                        Column('Present Address line1',null_validation),
                        Column('Present Address line2',null_validation),
                        Column('Present Village',null_validation),
                        Column('Permanent Address line1',null_validation),
                        Column('Permanent Address line2',null_validation),
                        Column('Permanent Village',null_validation),
                        Column('Permanent Panchayat',null_validation),
                        Column('Permanent Taluk/Block',null_validation),
                        Column('Document copy',null_validation),
                        Column('BOCW Registration Id',null_validation),
                        Column('Whatsapp Number',mob_validation + null_validation),
                        Column('Aadhar Image',null_validation),
                        Column('Educational Marksheet', null_validation),
                        
                        #str+null check
                        Column('Fresher/Experienced?*',str_validation + null_validation),
                        Column('Salutation*',str_validation + null_validation),
                        Column('First Name*',str_validation + null_validation),
                        Column('Gender*',str_validation + null_validation),
                        Column('Marital Status*',str_validation + null_validation),
                        Column('Caste*',str_validation + null_validation),
                        Column('Disability Status*',str_validation + null_validation),
                        Column('Religion*',str_validation + null_validation),
                        Column('Mother Tongue*',str_validation + null_validation),
                        Column('Occupation*',str_validation + null_validation),
                        Column('Average annual income*',str_validation + null_validation),
                        Column('Source of Information*',str_validation + null_validation),
                        Column('Interested Course*',str_validation + null_validation),
                        Column('Product*',str_validation + null_validation),
                        Column('Present District*',str_validation + null_validation),
                        Column('Present State*',state_validation + str_validation + null_validation),
                        Column('Present Country*',str_validation + null_validation),
                        Column('Permanent District*',str_validation + null_validation),
                        Column('Permanent State*',state_validation + str_validation + null_validation),
                        Column('Permanent Country*',str_validation + null_validation),                            
                        Column('Employment Type*',str_validation + null_validation),
                        Column('Preferred Job Role*',str_validation + null_validation),
                        Column('Years Of Experience*',str_validation + null_validation),
                        Column('Relevant Years of Experience*',str_validation + null_validation),
                        Column('Current/Last CTC*',str_validation + null_validation),
                        Column('Preferred Location*',str_validation + null_validation),
                        Column('Willing to travel?*',str_validation + null_validation),
                        Column('Willing to work in shifts?*',str_validation + null_validation),
                        Column('Expected CTC*',str_validation + null_validation),
                        #pincode check
                        Column('Present Pincode*',pincode_validation + null_validation),
                        Column('Permanent Pincode*',pincode_validation + null_validation),
                        #mobile number check
                        Column('Primary contact  No*',mob_validation + null_validation),
                        #date of birth and age pass(null check)
                        Column('Date of Birth*',null_validation),
                        Column('Age*',null_validation),
                        Column('date_age',dob_validation),
                        #ID Validation pass(null check)
                        Column('Aadhar No',null_validation),
                        Column('Identifier Type',null_validation),
                        Column('Identity number',null_validation),
                        Column('ids',null_validation),
                        #Email validation
                        Column('Registered by*',email_validation+str_validation)
                        ])
                errors = schema.validate(df)
                errors_index_rows = [e.row for e in errors]

                #df_clean = df.drop(index=errors_index_rows)
                #df_clean.to_csv('clean_data.csv',index=None)
                len_error = len(errors_index_rows)
                os.remove(file_name)
                if len_error>0:
                    file_name = str(user_id) + '_'+ str(datetime.now().strftime('%Y%m%d_%H%M%S'))+'_' + 'errors.csv'
                    pd.DataFrame({'col':errors}).to_csv(config.bulk_upload_path + 'Error/' + file_name)
                    return {"Status":False, "message":"Validation_Error", "error":"Validation Error <a href='/Bulk Upload/Error/{}' >Download error log</a>".format(file_name) }
                else:
                    df_all_image=[]
                    for i in img_column.split(','):
                        df_all_image += df[i].tolist()
                    df_all_image = list(filter(lambda x: ((x!='') and (not(pd.isna(x)))), df_all_image))
                    df_all_image = df_all_image if df_all_image==[] else ','.join(df_all_image).split(',')

                    for i in img_column.split(','):
                        df[i]=df[i].map(lambda x: x if (x=='' or pd.isna(x)) else ','.join([filename_prefix+j for j in x.split(',')]))
                    #print(str(set(df_all_image)) + ',' + str(set(all_image_files)))
                    if set(all_image_files)==set(df_all_image):
                        if ProjectType==2:
                            errors = schema_MCL.validate(df_MCL)
                            errors_index_rows = [e.row for e in errors]
                            len_error = len(errors_index_rows)
                            if len_error>0:
                                file_name = str(user_id) + '_'+ str(datetime.now().strftime('%Y%m%d_%H%M%S'))+'_' + 'errors.csv'
                                pd.DataFrame({'col':errors}).to_csv(config.bulk_upload_path + 'Error/' + file_name)
                                out = {"Status":False, "message":"Validation_Error", "error":"Validation Error <a href='/Bulk Upload/Error/{}' >Download error log</a>".format(file_name)}
                            else:
                                df_MCL['Result']=df_MCL['Result'].map(lambda x:1 if x.lower()=='pass' else 0)
                                out = Database.registration_web_inser(df,user_id,ProjectType,df_MCL)
                        else:
                            out = Database.registration_web_inser(df,user_id,ProjectType)
                    
                    elif (set(all_image_files)-set(df_all_image))!=set():
                        out = {"Status":False, "message":"Unable to upload {} ,image name missing in the excel template.".format(','.join(set(all_image_files)-set(df_all_image)))}
                    else:
                        out = {"Status":False, "message":"No such image found : {}".format(','.join(set(df_all_image)-set(all_image_files)))}
                    return out
                    
            elif cand_stage==str(3):
                if ProjectType==2:
                    img_column = 'Bank Copy*,Candidate Photo*,Education qualification Proof,Age Proof,Signed Mou*'
                    df= pd.read_excel(file_name,sheet_name='Enrollment',header=1)
                    df = df.fillna('')
                    df['date_age']=df['Age*'].astype(str)+df['Date of Birth*'].astype(str)
                    df['ids']=df['Aadhar No'].astype(str)+df['Identity number'].astype(str)

                    schema = Schema([
                        #nan check column non mandate
                        Column('Candidate_id',null_validation),
                        Column('Middle Name',null_validation),
                        Column('Last Name',null_validation),
                        Column('Secondary Contact  No',null_validation),
                        Column('Email id*',str_validation + null_validation),
                        Column('Present Panchayat',null_validation),
                        Column('Present Taluk/Block',null_validation),
                        Column('Present Address line2',null_validation),
                        Column('Present Village',null_validation),
                        Column('Permanent Address line2',null_validation),
                        Column('Permanent Village',null_validation),
                        Column('Permanent Panchayat',null_validation),
                        Column('Permanent Taluk/Block',null_validation),
                        Column('Name of Institute',null_validation),
                        Column('University',null_validation),
                        Column('Year Of Pass',null_validation),
                        Column('Percentage',null_validation),
                        Column('Date Of birth',null_validation),
                        Column('Age',null_validation),
                        Column('Primary contact',null_validation),
                        Column('Email Address',null_validation),
                        Column('Occupation',null_validation),
                        Column('Branch Name',null_validation),
                        Column('Branch Code',null_validation),
                        Column('Account type',null_validation),
                        #Column('Document copy'),
                        Column('BOCW Registration Id'),
                        Column('Whatsapp Number',mob_validation),
                        #Column('Aadhar Image',null_validation),
                        #str+null check
                        Column('Fresher/Experienced?*',str_validation + null_validation),
                        #Column('Candidate Photo*',str_validation + null_validation),
                        Column('Salutation*',str_validation + null_validation),
                        Column('First Name*',str_validation + null_validation),
                        Column('Gender*',str_validation + null_validation),
                        Column('Marital Status*',str_validation + null_validation),
                        Column('Caste*',str_validation + null_validation),
                        Column('Disability Status*',str_validation + null_validation),
                        Column('Religion*',str_validation + null_validation),
                        Column('Mother Tongue*',str_validation + null_validation),
                        Column('Occupation*',str_validation + null_validation),
                        Column('Average annual income*',str_validation + null_validation),
                        Column('Source of Information*',str_validation + null_validation),
                        Column('Interested Course*',str_validation + null_validation),
                        Column('Product*',str_validation + null_validation),
                        Column('Present Address line1*',str_validation + null_validation),
                        Column('Present District*',str_validation + null_validation),
                        Column('Present State*',state_validation + str_validation + null_validation),
                        Column('Present Country*',str_validation + null_validation),
                        Column('Permanent Address line1*',str_validation + null_validation),
                        Column('Permanent District*',str_validation + null_validation),
                        Column('Permanent State*',state_validation + str_validation + null_validation),
                        Column('Permanent Country*',str_validation + null_validation),
                        #Column('Document copy*',str_validation + null_validation),
                        Column('Employment Type*',str_validation + null_validation),
                        Column('Preferred Job Role*',str_validation + null_validation),
                        Column('Years Of Experience*',str_validation + null_validation),
                        Column('Relevant Years of Experience*',str_validation + null_validation),
                        Column('Current/Last CTC*',str_validation + null_validation),
                        Column('Preferred Location*',str_validation + null_validation),
                        Column('Willing to travel?*',str_validation + null_validation),
                        Column('Willing to work in shifts?*',str_validation + null_validation),
                        Column('Expected CTC*',str_validation + null_validation),
                        Column('Highest Qualification*',str_validation + null_validation),
                        Column('Stream/Specialization*',str_validation + null_validation),
                        Column('Computer Knowledge*',str_validation + null_validation),
                        Column('Technical Knowledge*',str_validation + null_validation),
                        Column('family_Salutation*',str_validation + null_validation),
                        Column('Member Name*',str_validation + null_validation),
                        Column('family_Gender*',str_validation + null_validation),
                        Column('Education Qualification*',str_validation + null_validation),
                        Column('Relationship*',str_validation + null_validation),
                        Column('Average Household Income*',str_validation + null_validation),
                        Column('batch_id*',str_validation + null_validation),
                        #pincode check
                        Column('Present Pincode*',pincode_validation + null_validation),
                        Column('Permanent Pincode*',pincode_validation + null_validation),
                        #mobile number check
                        Column('Primary contact  No*',mob_validation + null_validation),
                        #date of birth and age pass(null check)
                        Column('Date of Birth*',null_validation),
                        Column('Age*',null_validation),
                        Column('date_age',dob_validation),
                        #ID Validation pass(null check)
                        Column('Aadhar No',null_validation),
                        Column('Identifier Type',null_validation),
                        Column('Identity number',null_validation),
                        Column('ids',null_validation),
                        #Email validation
                        Column('Enrolled_By*',email_validation + str_validation),
                        #SHE PRORJECT
                        Column('Candidate Photo*',str_validation + null_validation),
                        Column('Bank Copy*',str_validation + null_validation),
                        Column('Bank Name*',str_validation + null_validation),
                        Column('Account Number*',str_validation + null_validation),

                        Column('Rented Or Own House?',null_validation),
                        Column('Size Of The House',null_validation),
                        Column('Ration Card (Apl Or Bpl)',null_validation),
                        Column('Tv',null_validation),
                        Column('Refrigerator',null_validation),
                        Column('Washing Machine',null_validation),
                        Column('Ac /Cooler',null_validation),
                        Column('Car',null_validation),
                        Column('Medical Insurance',null_validation),
                        Column('Life Insurance',null_validation),
                        Column('Farm Land',null_validation),
                        Column('Others',null_validation),
                        Column('Address As Per Aadhar Card (Incl Pin Code)*',null_validation),
                        Column('Education qualification Proof',null_validation),
                        Column('Age Proof',null_validation),
                        Column('Signed Mou*',str_validation + null_validation),
                        Column('Mou Signed Date',null_validation)
                        ])
                elif ProjectType==1:
                    img_column = 'Bank Copy'
                    df= pd.read_excel(file_name,sheet_name='Enrollment')
                    df = df.fillna('')
                    df['date_age']=df['Age*'].astype(str)+df['Date of Birth*'].astype(str)
                    df['ids']=df['Aadhar No'].astype(str)+df['Identity number'].astype(str)

                    schema = Schema([
                        Column('Candidate_id',null_validation),
                        Column('Middle Name',null_validation),
                        Column('Last Name',null_validation),
                        Column('Secondary Contact  No',null_validation),
                        Column('Email id*',str_validation + null_validation),
                        Column('Present Panchayat',null_validation),
                        Column('Present Taluk/Block',null_validation),
                        Column('Present Address line2',null_validation),
                        Column('Present Village',null_validation),
                        Column('Permanent Address line2',null_validation),
                        Column('Permanent Village',null_validation),
                        Column('Permanent Panchayat',null_validation),
                        Column('Permanent Taluk/Block',null_validation),
                        Column('Name of Institute',null_validation),
                        Column('University',null_validation),
                        Column('Year Of Pass',null_validation),
                        Column('Percentage',null_validation),
                        Column('Date Of birth',null_validation),
                        Column('Age',null_validation),
                        Column('Primary contact',null_validation),
                        Column('Email Address',null_validation),
                        Column('Occupation',null_validation),
                        Column('Branch Name',null_validation),
                        Column('Branch Code',null_validation),
                        Column('Account type',null_validation),
                        Column('Bank Copy',null_validation),
                        #Column('Candidate Photo') if ProjectType==1 else Column('Candidate Photo*',str_validation+null_validation),
                        #Column('Document copy'),
                        Column('Bank Name'),
                        Column('Account Number'),
                        Column('BOCW Registration Id'),
                        Column('Whatsapp Number',mob_validation),             
                        #Column('Aadhar Image',null_validation),           
                        #str+null check
                        Column('Fresher/Experienced?*',str_validation + null_validation),
                        #Column('Candidate Photo*',str_validation + null_validation),
                        Column('Salutation*',str_validation + null_validation),
                        Column('First Name*',str_validation + null_validation),
                        Column('Gender*',str_validation + null_validation),
                        Column('Marital Status*',str_validation + null_validation),
                        Column('Caste*',str_validation + null_validation),
                        Column('Disability Status*',str_validation + null_validation),
                        Column('Religion*',str_validation + null_validation),
                        Column('Mother Tongue*',str_validation + null_validation),
                        Column('Occupation*',str_validation + null_validation),
                        Column('Average annual income*',str_validation + null_validation),
                        Column('Source of Information*',str_validation + null_validation),
                        Column('Interested Course*',str_validation + null_validation),
                        Column('Product*',str_validation + null_validation),
                        Column('Present Address line1*',str_validation + null_validation),
                        Column('Present District*',str_validation + null_validation),
                        Column('Present State*',state_validation + str_validation + null_validation),
                        Column('Present Country*',str_validation + null_validation),
                        Column('Permanent Address line1*',str_validation + null_validation),
                        Column('Permanent District*',str_validation + null_validation),
                        Column('Permanent State*',state_validation + str_validation + null_validation),
                        Column('Permanent Country*',str_validation + null_validation),
                        #Column('Document copy*',str_validation + null_validation),
                        Column('Employment Type*',str_validation + null_validation),
                        Column('Preferred Job Role*',str_validation + null_validation),
                        Column('Years Of Experience*',str_validation + null_validation),
                        Column('Relevant Years of Experience*',str_validation + null_validation),
                        Column('Current/Last CTC*',str_validation + null_validation),
                        Column('Preferred Location*',str_validation + null_validation),
                        Column('Willing to travel?*',str_validation + null_validation),
                        Column('Willing to work in shifts?*',str_validation + null_validation),
                        Column('Expected CTC*',str_validation + null_validation),
                        Column('Highest Qualification*',str_validation + null_validation),
                        Column('Stream/Specialization*',str_validation + null_validation),
                        Column('Computer Knowledge*',str_validation + null_validation),
                        Column('Technical Knowledge*',str_validation + null_validation),
                        Column('family_Salutation*',str_validation + null_validation),
                        Column('Member Name*',str_validation + null_validation),
                        Column('family_Gender*',str_validation + null_validation),
                        Column('Education Qualification*',str_validation + null_validation),
                        Column('Relationship*',str_validation + null_validation),
                        Column('Average Household Income*',str_validation + null_validation),
                        Column('batch_id*',str_validation + null_validation),
                        #pincode check
                        Column('Present Pincode*',pincode_validation + null_validation),
                        Column('Permanent Pincode*',pincode_validation + null_validation),
                        #mobile number check
                        Column('Primary contact  No*',mob_validation + null_validation),
                        #date of birth and age pass(null check)
                        Column('Date of Birth*',null_validation),
                        Column('Age*',null_validation),
                        Column('date_age',dob_validation),
                        #ID Validation pass(null check)
                        Column('Aadhar No',null_validation),
                        Column('Identifier Type',null_validation),
                        Column('Identity number',null_validation),
                        Column('ids',null_validation),
                        #Email validation
                        Column('Enrolled_By*',email_validation + str_validation)
                        ])
                else:
                    img_column = 'Bank Copy,Candidate Photo*'
                    df= pd.read_excel(file_name,sheet_name='Enrollment')
                    df = df.fillna('')
                    df['date_age']=df['Age*'].astype(str)+df['Date of Birth*'].astype(str)
                    df['ids']=df['Aadhar No'].astype(str)+df['Identity number'].astype(str)

                    schema = Schema([
                        Column('Candidate_id',null_validation),
                        Column('Middle Name',null_validation),
                        Column('Last Name',null_validation),
                        Column('Secondary Contact  No',null_validation),
                        Column('Email id*',str_validation + null_validation),
                        Column('Present Panchayat',null_validation),
                        Column('Present Taluk/Block',null_validation),
                        Column('Present Address line2',null_validation),
                        Column('Present Village',null_validation),
                        Column('Permanent Address line2',null_validation),
                        Column('Permanent Village',null_validation),
                        Column('Permanent Panchayat',null_validation),
                        Column('Permanent Taluk/Block',null_validation),
                        Column('Name of Institute',null_validation),
                        Column('University',null_validation),
                        Column('Year Of Pass',null_validation),
                        Column('Percentage',null_validation),
                        Column('Date Of birth',null_validation),
                        Column('Age',null_validation),
                        Column('Primary contact',null_validation),
                        Column('Email Address',null_validation),
                        Column('Occupation',null_validation),
                        Column('Branch Name',null_validation),
                        Column('Branch Code',null_validation),
                        Column('Account type',null_validation),
                        Column('Bank Copy',null_validation),
                        Column('Candidate Photo*',str_validation+null_validation),
                        #Column('Candidate Photo') if ProjectType==1 else Column('Candidate Photo*',str_validation+null_validation),
                        #Column('Document copy'),
                        Column('Bank Name'),
                        Column('Account Number'),
                        Column('BOCW Registration Id'),
                        Column('Whatsapp Number',mob_validation),             
                        #Column('Aadhar Image',null_validation),           
                        #str+null check
                        Column('Fresher/Experienced?*',str_validation + null_validation),
                        #Column('Candidate Photo*',str_validation + null_validation),
                        Column('Salutation*',str_validation + null_validation),
                        Column('First Name*',str_validation + null_validation),
                        Column('Gender*',str_validation + null_validation),
                        Column('Marital Status*',str_validation + null_validation),
                        Column('Caste*',str_validation + null_validation),
                        Column('Disability Status*',str_validation + null_validation),
                        Column('Religion*',str_validation + null_validation),
                        Column('Mother Tongue*',str_validation + null_validation),
                        Column('Occupation*',str_validation + null_validation),
                        Column('Average annual income*',str_validation + null_validation),
                        Column('Source of Information*',str_validation + null_validation),
                        Column('Interested Course*',str_validation + null_validation),
                        Column('Product*',str_validation + null_validation),
                        Column('Present Address line1*',str_validation + null_validation),
                        Column('Present District*',str_validation + null_validation),
                        Column('Present State*',state_validation + str_validation + null_validation),
                        Column('Present Country*',str_validation + null_validation),
                        Column('Permanent Address line1*',str_validation + null_validation),
                        Column('Permanent District*',str_validation + null_validation),
                        Column('Permanent State*',state_validation + str_validation + null_validation),
                        Column('Permanent Country*',str_validation + null_validation),
                        #Column('Document copy*',str_validation + null_validation),
                        Column('Employment Type*',str_validation + null_validation),
                        Column('Preferred Job Role*',str_validation + null_validation),
                        Column('Years Of Experience*',str_validation + null_validation),
                        Column('Relevant Years of Experience*',str_validation + null_validation),
                        Column('Current/Last CTC*',str_validation + null_validation),
                        Column('Preferred Location*',str_validation + null_validation),
                        Column('Willing to travel?*',str_validation + null_validation),
                        Column('Willing to work in shifts?*',str_validation + null_validation),
                        Column('Expected CTC*',str_validation + null_validation),
                        Column('Highest Qualification*',str_validation + null_validation),
                        Column('Stream/Specialization*',str_validation + null_validation),
                        Column('Computer Knowledge*',str_validation + null_validation),
                        Column('Technical Knowledge*',str_validation + null_validation),
                        Column('family_Salutation*',str_validation + null_validation),
                        Column('Member Name*',str_validation + null_validation),
                        Column('family_Gender*',str_validation + null_validation),
                        Column('Education Qualification*',str_validation + null_validation),
                        Column('Relationship*',str_validation + null_validation),
                        Column('Average Household Income*',str_validation + null_validation),
                        Column('batch_id*',str_validation + null_validation),
                        #pincode check
                        Column('Present Pincode*',pincode_validation + null_validation),
                        Column('Permanent Pincode*',pincode_validation + null_validation),
                        #mobile number check
                        Column('Primary contact  No*',mob_validation + null_validation),
                        #date of birth and age pass(null check)
                        Column('Date of Birth*',null_validation),
                        Column('Age*',null_validation),
                        Column('date_age',dob_validation),
                        #ID Validation pass(null check)
                        Column('Aadhar No',null_validation),
                        Column('Identifier Type',null_validation),
                        Column('Identity number',null_validation),
                        Column('ids',null_validation),
                        #Email validation
                        Column('Enrolled_By*',email_validation + str_validation)
                        ])

                errors = schema.validate(df)
                errors_index_rows = [e.row for e in errors]

                len_error = len(errors_index_rows)
                os.remove(file_name)

                if len_error>0:
                    file_name = str(user_id) + '_'+ str(datetime.now().strftime('%Y%m%d_%H%M%S'))+'_' + 'errors.csv'
                    pd.DataFrame({'col':errors}).to_csv(config.bulk_upload_path + 'Error/' + file_name)
                    return {"Status":False, "message":"Validation_Error", "error":"Validation Error <a href='/Bulk Upload/Error/{}' >Download error log</a>".format(file_name) }
                else:
                    df_all_image=[]
                    for i in img_column.split(','):
                        df_all_image += df[i].tolist()
                    df_all_image = list(filter(lambda x: ((x!='') and (not(pd.isna(x)))), df_all_image))
                    df_all_image = df_all_image if df_all_image==[] else ','.join(df_all_image).split(',')
                    for i in img_column.split(','):
                        df[i]=df[i].map(lambda x: x if (x=='' or pd.isna(x)) else ','.join([filename_prefix+j for j in x.split(',')]))
                    #print(str(set(df_all_image)) + ',' + str(set(all_image_files)))
                    if set(all_image_files)==set(df_all_image):
                        out = Database.enrollment_web_inser(df,user_id,ProjectType)
                    elif (set(all_image_files)-set(df_all_image))!=set():
                        out = {"Status":False, "message":"Unable to upload {} ,image name missing in the excel template.".format(','.join(set(all_image_files)-set(df_all_image)))}
                    else:
                        out = {"Status":False, "message":"No such image found : {}".format(','.join(set(df_all_image)-set(all_image_files)))}
                    return out
            else:
                return {"Status":False, "message":"Wrong Candidate Stage"}
            #except Exception as e:
            #    return {"Status":False, "message":"Unable to upload " + str(e)}       
api.add_resource(upload_bulk_upload,'/upload_bulk_upload')

@app.route("/registration_list_page")
def registration_list_page():
    if g.user:
        #status=request.args.get('status',-1,type=int)
        return render_template("Candidate/registration_list.html")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/registration")
def registration():
    if g.user:
        #status=request.args.get('status',-1,type=int) 
        html_str="registration_list_page"    #?status=" + str(status)
        return render_template("home.html",values=g.User_detail_with_ids,html=html_str)
    else:
        return render_template("login.html",error="Session Time Out!!")

class registered_list_updated(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            candidate_id=request.form['candidate_id']
            region_ids=request.form['region_ids']
            state_ids = request.form["state_ids"]
            Pincode = request.form["Pincode"]
            ToDate = request.form["ToDate"]
            FromDate = request.form["FromDate"]
            created_by = request.form["created_by"]
            
            user_id = request.form["user_id"]
            user_role_id = request.form["user_role_id"]
            search_type = request.form["search_type"]
            search_keyword = request.form["search_keyword"]
            start_index = request.form['start']
            page_length = request.form['length']
            search_value = request.form['search[value]']
            order_by_column_position = request.form['order[0][column]']
            order_by_column_direction = request.form['order[0][dir]']
            draw=request.form['draw']
            print(FromDate, ToDate)
            return Candidate.registered_list(candidate_id,region_ids, state_ids, Pincode,search_type,search_keyword, created_by, FromDate, ToDate, user_id, user_role_id, start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)
api.add_resource(registered_list_updated, '/registered_list_updated')


class AllCreatedByBasedOnUser(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            try:
                UserId=request.args.get('user_id',0,type=int)
                UserRoleId=request.args.get('user_role_id',1,type=int)                
                response=Database.AllCreatedByBasedOnUser(UserId,UserRoleId)
                return {'CreatedBy':response}
            except Exception as e:
                return {'exception':str(e)}

api.add_resource(AllCreatedByBasedOnUser,'/AllCreatedByBasedOnUser')

class DownloadRegTemplate(Resource):
    report_name = "Trainerwise_TMA_Registration_Compliance"+datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    @staticmethod
    def post():
        if request.method=='POST':
            try:
                user_id = request.form["user_id"]
                user_role_id = request.form["user_role_id"]
                candidate_ids = request.form["candidate_ids"]
                Project_Type = int(request.form["Project_Type"])
                
                resp = Database.download_selected_registration_candidate(candidate_ids)

                if(len(resp['data']) < 1):
                    return({'msg':'No Records Found For Selected Filters!', 'success':False})
                else:
                    df = pd.DataFrame(resp['data'], columns=resp['columns'])
                    col = ['Candidate_Id', 'Isfresher', 'Salutation', 'First_Name', 'Middle_Name', 'Last_Name', 'Date_Of_Birth', 
                    'Age', 'Primary_Contact_No', 'Secondary_Contact_No', 'Email_Id', 'Gender', 'Marital_Status', 'Caste', 'Disability_Status', 'Religion', 
                    'Mother_Tongue', 'Occupation', 'Average_Annual_Income', 'Source_Of_Information', 'Interested_Course', 'Product', 'Present_Address_Line1', 
                    'Present_Address_Line2', 'Present_Village', 'Present_Panchayat', 'Present_Taluk_Block', 'Present_District', 'Present_State', 
                    'Present_Pincode', 'Present_Country', 'Permanent_Address_Line1', 'Permanent_Address_Line2', 'Permanent_Village', 'Permanent_Panchayat', 
                    'Permanent_Taluk_Block', 'Permanent_District', 'Permanent_State', 'Permanent_Pincode', 'Permanent_Country', 'Aadhar_No', 'Identifier_Type', 
                    'Identity_Number', 'Document_Copy_Image_Name', 'Employment_Type', 'Preferred_Job_Role', 'Years_Of_Experience', 'Relevant_Years_Of_Experience', 
                    'Current_Last_Ctc', 'Preferred_Location', 'Willing_To_Travel', 'Willing_To_Work_In_Shifts', 'Bocw_Registration_Id', 'Expected_Ctc', 
                    'Aadhar_Image_Name','Registered_By', 'Whatsapp_Number','Educational Marksheet']

                    Column = ['Candidate_id', 'Fresher/Experienced?*', 'Salutation*', 'First Name*', 'Middle Name', 'Last Name', 'Date of Birth*', 
                    'Age*', 'Primary contact  No*', 'Secondary Contact  No', 'Email id*', 'Gender*', 'Marital Status*', 'Caste*', 'Disability Status*', 'Religion*', 
                    'Mother Tongue*', 'Occupation*', 'Average annual income*', 'Source of Information*', 'Interested Course*', 'Product*', 'Present Address line1', 
                    'Present Address line2', 'Present Village', 'Present Panchayat', 'Present Taluk/Block', 'Present District*', 'Present State*', 
                    'Present Pincode*', 'Present Country*', 'Permanent Address line1', 'Permanent Address line2', 'Permanent Village', 'Permanent Panchayat', 
                    'Permanent Taluk/Block', 'Permanent District*', 'Permanent State*', 'Permanent Pincode*', 'Permanent Country*', 'Aadhar No', 'Identifier Type', 
                    'Identity number', 'Document copy', 'Employment Type*', 'Preferred Job Role*', 'Years Of Experience*', 'Relevant Years of Experience*', 
                    'Current/Last CTC*', 'Preferred Location*', 'Willing to travel?*', 'Willing to work in shifts?*', 'BOCW Registration Id', 'Expected CTC*',
                    'Aadhar Image','Registered by*','Whatsapp Number','Educational Marksheet']
                
                    if Project_Type==1:
                        col = ['Candidate_Id', 'Isfresher', 'Candidate_Photo', 'Salutation', 'First_Name', 'Middle_Name', 'Last_Name', 'Date_Of_Birth', 
                        'Age', 'Primary_Contact_No', 'Secondary_Contact_No', 'Email_Id', 'Gender', 'Marital_Status', 'Caste', 'Disability_Status', 'Religion', 
                        'Mother_Tongue', 'Occupation', 'Average_Annual_Income', 'Source_Of_Information', 'Interested_Course', 'Product', 'Present_Address_Line1', 
                        'Present_Address_Line2', 'Present_Village', 'Present_Panchayat', 'Present_Taluk_Block', 'Present_District', 'Present_State', 
                        'Present_Pincode', 'Present_Country', 'Permanent_Address_Line1', 'Permanent_Address_Line2', 'Permanent_Village', 'Permanent_Panchayat', 
                        'Permanent_Taluk_Block', 'Permanent_District', 'Permanent_State', 'Permanent_Pincode', 'Permanent_Country', 'Aadhar_No', 'Identifier_Type', 
                        'Identity_Number', 'Document_Copy_Image_Name', 'Employment_Type', 'Preferred_Job_Role', 'Years_Of_Experience', 'Relevant_Years_Of_Experience', 
                        'Current_Last_Ctc', 'Preferred_Location', 'Willing_To_Travel', 'Willing_To_Work_In_Shifts', 'Bocw_Registration_Id', 'Expected_Ctc', 
                        'Aadhar_Image_Name','Registered_By', 'Whatsapp_Number','Educational Marksheet']
                        col += ['Aspirational District',  'Income Certificate']

                        Column = ['Candidate_id', 'Fresher/Experienced?*', 'Candidate Photo*', 'Salutation*', 'First Name*', 'Middle Name', 'Last Name', 'Date of Birth*', 
                        'Age*', 'Primary contact  No*', 'Secondary Contact  No', 'Email id*', 'Gender*', 'Marital Status*', 'Caste*', 'Disability Status*', 'Religion*', 
                        'Mother Tongue*', 'Occupation*', 'Average annual income*', 'Source of Information*', 'Interested Course*', 'Product*', 'Present Address line1', 
                        'Present Address line2', 'Present Village', 'Present Panchayat', 'Present Taluk/Block', 'Present District*', 'Present State*', 
                        'Present Pincode*', 'Present Country*', 'Permanent Address line1', 'Permanent Address line2', 'Permanent Village', 'Permanent Panchayat', 
                        'Permanent Taluk/Block', 'Permanent District*', 'Permanent State*', 'Permanent Pincode*', 'Permanent Country*', 'Aadhar No', 'Identifier Type', 
                        'Identity number', 'Document copy', 'Employment Type*', 'Preferred Job Role*', 'Years Of Experience*', 'Relevant Years of Experience*', 
                        'Current/Last CTC*', 'Preferred Location*', 'Willing to travel?*', 'Willing to work in shifts?*', 'BOCW Registration Id', 'Expected CTC*',
                        'Aadhar Image','Registered by*','Whatsapp Number','Educational Marksheet*']
                        Column += ['Aspirational District*', 'Income Certificate']

                        filename = 'CandidateBulkUpload_Registration_DELL_'
                    elif Project_Type==2:
                        col += []
                        Column += []
                        filename = 'CandidateBulkUpload_Registration_SHE_'
                    else:
                        filename = 'CandidateBulkUpload_Registration_'

                    file_name= filename +str(user_id) +'_'+ str(datetime.now().strftime('%Y%m%d_%H%M%S'))+'.xlsx'

                    df = df[col]
                    
                    writer = pd.ExcelWriter(config.bulk_upload_path + file_name, engine='xlsxwriter')
                    workbook  = writer.book

                    header_format = workbook.add_format({
                        'bold': True,
                        #'text_wrap': True,
                        'valign': 'center',
                        'fg_color': '#D7E4BC',
                        'border': 1})
                    df.to_excel(writer, index=None, header=None ,startrow=1 ,sheet_name='Registration') 
                    worksheet = writer.sheets['Registration']

                    for i in range(len(Column)):
                        worksheet.write(0,i ,Column[i], header_format)
                    if Project_Type==2:
                        she_col = ['Candidate_Id', 'First_Name', 'Primary_Contact_No', 'Email_Id']
                        MCL = ['Candidate_id', 'First Name*', 'Primary contact  No*', 'Email id*']
                        MCL += ['Date of birth -Is age between 18 to 40?', 'Are you 8th Pass?', 'Are you able to read and write local language?', 'Do you have a smart phone?', 'Are you\xa0willing to buy a smartphone?', 'Do you own two wheeler?', 'Do you have any work experience', 'Will you able to work full time or at least 6 hours a day?', 'Are you willing to serve the community at this time of COVID-19 pandemic as Sanitization & Hygiene Entrepreneurs (SHE)?', 'Willing to travel for work', 'Are you willing to work and sign the work contract with LN?', 'Are you willing to adopt digital transactions in your business?', 'Do you have a bank account?', 'Have you availed any loan in the past?', 'Do you have any active loan?', 'Are you willing to take up a loan to purchase tools and consumables?', 'Are you covered under any health insurance?', 'Are you allergic to any chemicals and dust?', 'Are you willing to follow  Environment, Health and Safety Norms in your business?', 'Have you ever been subjected to any legal enquiry for Non ethical work/business?','Result']
                        df_2 = df[she_col]
                        df_2.to_excel(writer, index=None, header=None ,startrow=1 ,sheet_name='SHE MCL')
                        worksheet = writer.sheets['SHE MCL']
                        for i in range(len(MCL)):
                            worksheet.write(0,i ,MCL[i], header_format)
                    writer.save()
                    return {'Description':'Downloaded Template', 'Status':True, 'filename':file_name}
            except Exception as e:
                return {'Description':'Error: '+str(e), 'Status':False}
api.add_resource(DownloadRegTemplate,'/DownloadRegTemplate')

class SaveCandidateActivityStatus(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            client_id = str(request.form['client_id'])
            client_key = str(request.form['client_key'])

            if (client_id==config.API_secret_id) and (client_key==config.API_secret_key):
                try:
                    json_string=''
                    if 'JsonString' in request.form:
                        json_string=request.form["JsonString"] 
                    user_id=0
                    role_id=0
                    if 'user_id' in request.form:
                        user_id=request.form["user_id"]
                    if 'role_id' in request.form:
                        role_id = int(request.form['role_id'])
                    latitude = str(request.form['latitude'])
                    longitude = str(request.form['longitude'])
                    timestamp = str(request.form['timestamp'])
                    app_version = str(request.form['app_version'])
                    device_model = str(request.form['device_model'])
                    imei_num = str(request.form['imei_num'])
                    android_version = str(request.form['android_version'])
                    return Master.SaveCandidateActivityStatus(json_string,user_id,role_id,latitude,longitude,timestamp,app_version,device_model,imei_num,android_version)
                except Exception as e:
                    res = {'success': False, 'description': "unable to read data " + str(e)}
                    return jsonify(res)
            else:
                res = {'success': False, 'description': "client name and password not matching"}
                return jsonify(res)
        else:
            res = {'success': False, 'description': "Method is wrong"}
            return jsonify(res)  
api.add_resource(SaveCandidateActivityStatus,'/SaveCandidateActivityStatus')

@app.route("/enrollment_list_page")
def enrollment_list_page():
    if g.user:
        #status=request.args.get('status',-1,type=int)
        return render_template("Candidate/enrollment_list.html")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/enrollment")
def enrollment():
    if g.user:
        #status=request.args.get('status',-1,type=int) 
        html_str="enrollment_list_page"    #?status=" + str(status)
        return render_template("home.html",values=g.User_detail_with_ids,html=html_str)
    else:
        return render_template("login.html",error="Session Time Out!!")

class enrolled_list_updated(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            candidate_id=request.form['candidate_id']
            region_ids=request.form['region_ids']
            state_ids = request.form["state_ids"]
            Pincode = request.form["Pincode"]
            ToDate = request.form["ToDate"]
            FromDate = request.form["FromDate"]
            created_by = request.form["created_by"]
            project_type = request.form["project_type"]
            candidate_stage = request.form["candidate_stage"]
            user_id = request.form["user_id"]
            user_role_id = request.form["user_role_id"]
            search_type = request.form["search_type"]
            search_keyword = request.form["search_keyword"]
            
            start_index = request.form['start']
            page_length = request.form['length']
            search_value = request.form['search[value]']
            order_by_column_position = request.form['order[0][column]']
            order_by_column_direction = request.form['order[0][dir]']
            draw=request.form['draw']
            
            return Candidate.enrolled_list(candidate_id,region_ids, state_ids, Pincode,search_type,search_keyword, created_by,project_type,candidate_stage, FromDate, ToDate, user_id, user_role_id, start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)
api.add_resource(enrolled_list_updated, '/enrolled_list_updated')

class DownloadEnrTemplate(Resource):
    @staticmethod
    def post():
        if request.method=='POST':
            try:
                user_id = request.form["user_id"]
                user_role_id = request.form["user_role_id"]
                candidate_ids = request.form["candidate_ids"]
                Project_Type = int(request.form["Project_Type"])

                file_name='CandidateBulkUpload_Enrolment_'+str(user_id) +'_'+ str(datetime.now().strftime('%Y%m%d_%H%M%S'))+'.xlsx'
                resp = Database.download_selected_enrolled_candidate(candidate_ids)

                if(len(resp['data']) < 1):
                    return({'msg':'No Records Found For Selected Filters!', 'success':False})
                else:
                    df = pd.DataFrame(resp['data'], columns=resp['columns'])
                    df_column = resp['columns']

                    col = df_column[:44]+df_column[45:81] + df_column[82:84]
                    excel_row=0
                    if Project_Type==1:
                        col = df_column[:2]+df_column[3:44]+df_column[45:81] + df_column[82:84]
                        Column = ['Candidate_id', 'Fresher/Experienced?*', 'Salutation*', 'First Name*', 'Middle Name', 'Last Name', 'Date of Birth*', 'Age*', 'Primary contact  No*', 'Secondary Contact  No', 'Email id*', 
                        'Gender*', 'Marital Status*', 'Caste*', 'Disability Status*', 'Religion*', 'Mother Tongue*', 'Occupation*', 'Average annual income*', 'Source of Information*', 'Interested Course*', 'Product*', 'Present Address line1*', 
                        'Present Address line2', 'Present Village', 'Present Panchayat', 'Present Taluk/Block', 'Present District*', 'Present State*', 'Present Pincode*', 'Present Country*', 'Permanent Address line1*', 'Permanent Address line2', 
                        'Permanent Village', 'Permanent Panchayat', 'Permanent Taluk/Block', 'Permanent District*', 'Permanent State*', 'Permanent Pincode*', 'Permanent Country*', 'Aadhar No', 'Identifier Type', 'Identity number', 
                        'Employment Type*', 'Preferred Job Role*', 'Years Of Experience*', 'Relevant Years of Experience*', 'Current/Last CTC*', 'Preferred Location*', 'Willing to travel?*', 'Willing to work in shifts?*', 'BOCW Registration Id', 
                        'Expected CTC*', 'Highest Qualification*', 'Stream/Specialization*', 'Name of Institute', 'University', 'Year Of Pass', 'Percentage', 'Computer Knowledge*', 'Technical Knowledge*', 'family_Salutation*', 'Member Name*', 
                        'Date Of birth', 'Age', 'Primary contact', 'Email Address', 'family_Gender*', 'Education Qualification*', 'Relationship*', 'Occupation', 'Average Household Income*', 'Bank Name', 'Branch Name', 'Branch Code', 
                        'Account type', 'Account Number', 'Bank Copy', 'batch_id*', 'Enrolled_By*', 'Whatsapp Number']
                        Column += []
                        #df = df.iloc[:,:83]
                        filename = 'CandidateBulkUpload_Enrollment_DELL_'
                    elif Project_Type==2:
                        excel_row=1
                        Column = ['Candidate_id', 'Fresher/Experienced?*', 'Candidate Photo*', 'Salutation*', 'First Name*', 'Middle Name', 'Last Name', 'Date of Birth*', 'Age*', 'Primary contact  No*', 'Secondary Contact  No', 'Email id*', 
                        'Gender*', 'Marital Status*', 'Caste*', 'Disability Status*', 'Religion*', 'Mother Tongue*', 'Occupation*', 'Average annual income*', 'Source of Information*', 'Interested Course*', 'Product*', 'Present Address line1*', 
                        'Present Address line2', 'Present Village', 'Present Panchayat', 'Present Taluk/Block', 'Present District*', 'Present State*', 'Present Pincode*', 'Present Country*', 'Permanent Address line1*', 'Permanent Address line2', 
                        'Permanent Village', 'Permanent Panchayat', 'Permanent Taluk/Block', 'Permanent District*', 'Permanent State*', 'Permanent Pincode*', 'Permanent Country*', 'Aadhar No', 'Identifier Type', 'Identity number', 
                        'Employment Type*', 'Preferred Job Role*', 'Years Of Experience*', 'Relevant Years of Experience*', 'Current/Last CTC*', 'Preferred Location*', 'Willing to travel?*', 'Willing to work in shifts?*', 'BOCW Registration Id', 
                        'Expected CTC*', 'Highest Qualification*', 'Stream/Specialization*', 'Name of Institute', 'University', 'Year Of Pass', 'Percentage', 'Computer Knowledge*', 'Technical Knowledge*', 'family_Salutation*', 'Member Name*', 
                        'Date Of birth', 'Age', 'Primary contact', 'Email Address', 'family_Gender*', 'Education Qualification*', 'Relationship*', 'Occupation', 'Average Household Income*', 'Bank Name*', 'Branch Name', 'Branch Code', 
                        'Account type', 'Account Number*', 'Bank Copy*', 'batch_id*', 'Enrolled_By*', 'Whatsapp Number']

                        col += resp['columns'][84:]
                        Column += ['Rented Or Own House?', 'Size Of The House', 'Ration Card (Apl Or Bpl)', 'Tv', 'Refrigerator', 'Washing Machine', 'Ac /Cooler', 'Car', 'Medical Insurance', 'Life Insurance', 
                        'Farm Land', 'Others', 'Address As Per Aadhar Card (Incl Pin Code)*', 'Education qualification Proof', 'Age Proof', 'Signed Mou*', 'Mou Signed Date']
                        filename = 'CandidateBulkUpload_Enrollment_SHE_'
                    else:
                        Column = ['Candidate_id', 'Fresher/Experienced?*', 'Candidate Photo*', 'Salutation*', 'First Name*', 'Middle Name', 'Last Name', 'Date of Birth*', 'Age*', 'Primary contact  No*', 'Secondary Contact  No', 'Email id*', 
                        'Gender*', 'Marital Status*', 'Caste*', 'Disability Status*', 'Religion*', 'Mother Tongue*', 'Occupation*', 'Average annual income*', 'Source of Information*', 'Interested Course*', 'Product*', 'Present Address line1*', 
                        'Present Address line2', 'Present Village', 'Present Panchayat', 'Present Taluk/Block', 'Present District*', 'Present State*', 'Present Pincode*', 'Present Country*', 'Permanent Address line1*', 'Permanent Address line2', 
                        'Permanent Village', 'Permanent Panchayat', 'Permanent Taluk/Block', 'Permanent District*', 'Permanent State*', 'Permanent Pincode*', 'Permanent Country*', 'Aadhar No', 'Identifier Type', 'Identity number', 
                        'Employment Type*', 'Preferred Job Role*', 'Years Of Experience*', 'Relevant Years of Experience*', 'Current/Last CTC*', 'Preferred Location*', 'Willing to travel?*', 'Willing to work in shifts?*', 'BOCW Registration Id', 
                        'Expected CTC*', 'Highest Qualification*', 'Stream/Specialization*', 'Name of Institute', 'University', 'Year Of Pass', 'Percentage', 'Computer Knowledge*', 'Technical Knowledge*', 'family_Salutation*', 'Member Name*', 
                        'Date Of birth', 'Age', 'Primary contact', 'Email Address', 'family_Gender*', 'Education Qualification*', 'Relationship*', 'Occupation', 'Average Household Income*', 'Bank Name', 'Branch Name', 'Branch Code', 
                        'Account type', 'Account Number', 'Bank Copy', 'batch_id*', 'Enrolled_By*', 'Whatsapp Number']
                        #df = df.iloc[:,:83]
                        filename = 'CandidateBulkUpload_Enrollment_'

                    file_name= filename +str(user_id) +'_'+ str(datetime.now().strftime('%Y%m%d_%H%M%S'))+'.xlsx'
                    writer = pd.ExcelWriter(config.bulk_upload_path + file_name, engine='xlsxwriter')
                    workbook  = writer.book

                    header_format = workbook.add_format({
                        'bold': True,
                        #'text_wrap': True,
                        'valign': 'center',
                        'fg_color': '#D7E4BC',
                        'border': 1})
                    df_1 = df[col]
                    df_1.to_excel(writer, index=None, header=None ,startrow=excel_row+1 ,sheet_name='Enrollment') 
                    worksheet = writer.sheets['Enrollment']
                    for i in range(len(Column)):
                        worksheet.write(excel_row,i ,Column[i], header_format)
                    
                    if Project_Type==2:
                        worksheet.merge_range(0, 87, 0, 95, 'Asset List', header_format)
                    writer.save()
                    
                    return {'Description':'Downloaded Template', 'Status':True, 'filename':file_name}
            except Exception as e:
                return {'Description':'Error: '+str(e), 'Status':False}
class DownloadCertificationTemplate(Resource):
    @staticmethod
    def post():
        if request.method=='POST':
            try:
                user_id = request.form["user_id"]
                user_role_id = request.form["user_role_id"]
                batch_id = request.form["batch_id"]
                enrollment_ids = request.form["intervention_values"]

                
                file_name='CandidateCertificateUpload_'+str(user_id) +'_'+ str(datetime.now().strftime('%Y%m%d_%H%M%S'))+'.xlsx'
                resp = Database.download_selected_candidate_certification(batch_id,enrollment_ids)

                if(len(resp['data']) < 1):
                    return({'msg':'No Records Found For Selected Filters!', 'success':False})
                else:
                    df = pd.DataFrame(resp['data'], columns=resp['columns'])
                    col = resp['columns'][:4]
                    
                    excel_row=0
                    Column = ['Enrolment_Id','Candidate_Name', 'Batch_Code','Certificate_Number']
                    col += []
                    Column += []
                    writer = pd.ExcelWriter(config.bulk_upload_path + file_name, engine='xlsxwriter')
                    workbook  = writer.book

                    header_format = workbook.add_format({
                        'bold': True,
                        #'text_wrap': False,
                        'valign': 'center',
                        'fg_color': '#D7E4BC',
                        'border': 1})
                    df_1 = df[col]
                    df_1.to_excel(writer, index=None, header=None ,startrow=excel_row+1 ,sheet_name='Certificate') 
                    worksheet = writer.sheets['Certificate']
                    for i in range(len(Column)):
                        worksheet.write(excel_row,i ,Column[i], header_format)
                    
                    
                    writer.save()
                    
                    return {'Description':'Downloaded Template', 'Status':True, 'filename':file_name}
            except Exception as e:
                return {'Description':'Error: '+str(e), 'Status':False}

api.add_resource(DownloadEnrTemplate,'/DownloadEnrTemplate')
api.add_resource(DownloadCertificationTemplate,'/DownloadCertificationTemplate')

####################################################################################################
#Partner_API's

@app.route("/user_sub_project_report")
def user_sub_project_report():
    if g.user:
        return render_template("Reports/user_sub_project_report.html")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/user_sub_project")
def user_sub_project():
    if g.user:
        #status=request.args.get('status',-1,type=int) 
        html_str="user_sub_project_report"    #?status=" + str(status)
        return render_template("home.html",values=g.User_detail_with_ids,html=html_str)
    else:
        return render_template("login.html",error="Session Time Out!!")
@app.route("/partner_list_page")
def partner_list_page():
    if g.user:
        return render_template("Master/partner-list.html")
    else:
        return render_template("login.html",error="Session Time Out!!")


@app.route("/partner")
def partner():
    if g.user: 
        html_str="partner_list_page"
        return render_template("home.html",values=g.User_detail_with_ids,html=html_str)
    else:
        return render_template("login.html",error="Session Time Out!!")


@app.route("/partner_add_edit")
def partner_add_edit():
    if g.user:
        return render_template("Master/partner-add-edit.html",partner_id=g.partner_id)
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/assign_partner_add_edit_to_home", methods=['GET','POST'])
def assign_partner_add_edit_to_home():
    
    session['partner_id']=request.form['hdn_partner_id']
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="partner_add_edit")
    else:
        return render_template("login.html",error="Session Time Out!!")

class GetPartnerTypes(Resource):
    @staticmethod
    def get():
        if request.method == 'GET':
            return Master.GetPartnerTypes()
api.add_resource(GetPartnerTypes,'/GetPartnerTypes')

class GetAssessmentPartnerTypes(Resource):
    @staticmethod
    def get():
        if request.method == 'GET':
            return Master.GetAssessmentPartnerTypes()
api.add_resource(GetAssessmentPartnerTypes,'/GetAssessmentPartnerTypes')

class partner_list(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            partner_type_ids = request.form['partner_type_ids']
            start_index = request.form['start']
            page_length = request.form['length']
            search_value = request.form['search[value]']
            order_by_column_position = request.form['order[0][column]']
            order_by_column_direction = request.form['order[0][dir]']
            draw=request.form['draw']
            return Master.partner_list(partner_type_ids,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw)
api.add_resource(partner_list,'/partner_list')

class add_partner_details(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            partner_name=request.form['PartnerName']
            user_id=g.user_id
            is_active=request.form['isactive']
            partner_type_id=request.form['ddlPartnerTypes']
            assessment_partner_type_id=request.form['ddlAssessmentPartnerTypes']
            address=request.form['Address']
            partner_id=request.form['PartnerId']
            return Master.add_partner_details(partner_name,user_id,is_active,partner_type_id,assessment_partner_type_id,address,partner_id)
api.add_resource(add_partner_details,'/add_partner_details')

class upload_assessment_certificate_copy(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            certi_name=request.form['file_name']
            user_id=request.form['user_id']
            enrolment_id=request.form['enrollment_id']
            batch_id=request.form['batch_id']    
            return Database.upload_assessment_certificate_copy(certi_name,user_id,enrolment_id,batch_id)
api.add_resource(upload_assessment_certificate_copy,'/upload_assessment_certificate_copy')

class upload_assessment_certificate_copy_bulk_upload(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            certi_name=request.form['file_name']
            user_id=request.form['user_id']
            enrolment_id=request.form['enrollment_id']
            batch_id=request.form['batch_id']    
            return Database.upload_assessment_certificate_copy_bulk_upload(certi_name,user_id,enrolment_id,batch_id)
api.add_resource(upload_assessment_certificate_copy_bulk_upload,'/upload_assessment_certificate_copy_bulk_upload')
class upload_cerification_cand_image(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            certi_name=request.form['file_name']
            user_id=request.form['user_id']
            enrolment_id=request.form['enrollment_id']
            batch_id=request.form['batch_id']    
            return Database.upload_cerification_cand_image(certi_name,user_id,enrolment_id,batch_id)
api.add_resource(upload_cerification_cand_image,'/upload_cerification_cand_image')

class upload_cerification_batch_image(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            certi_name=request.form['file_name']
            user_id=request.form['user_id']
            batch_id=request.form['batch_id']    
            return Database.upload_cerification_batch_image(certi_name,user_id,batch_id)
api.add_resource(upload_cerification_batch_image,'/upload_cerification_batch_image')

@app.route("/after_popup_partner")
def after_popup_partner():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="partner")
    else:
        return render_template("login.html",error="Session Time Out!!")

class get_partner_details(Resource):
    @staticmethod
    def get():
        if request.method == 'GET':
            partner_id=request.args.get('partner_id',-1,type=int)
            return jsonify(Master.get_partner_details(partner_id))
api.add_resource(get_partner_details, '/get_partner_details')

class GetPartnerUsers(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            partner_id=request.args.get('partner_id',0,type=int)
            response=Master.GetPartnerUsers(partner_id)
            return response
api.add_resource(GetPartnerUsers,'/GetPartnerUsers')

class add_edit_partner_user(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            UserName=request.form['UserName']
            user_id=g.user_id
            is_active=request.form['isactive']
            Email=request.form['Email']
            Mobile=request.form['Mobile']
            PartnerId=request.form['PartnerId']
            PartnerUserId=request.form['PartnerUserId']
            return Master.add_edit_partner_user(UserName,user_id,is_active,Email,int(Mobile),PartnerId,PartnerUserId)
api.add_resource(add_edit_partner_user,'/add_edit_partner_user')
###############################################################################

class GetPartners(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            try:
                PartnerTypeId=request.args.get('PartnerTypeId',0,type=int)
                #print(PartnerTypeId)
                response = Master.GetPartners(PartnerTypeId)
                return response 
            except Exception as e:
                return {'exception':str(e)}
api.add_resource(GetPartners,'/GetPartners')

class upload_assessment_result(Resource):
    @staticmethod
    def post():
        if request.method=='POST':
            try:
                f = request.files['filename']
                assessment_id =request.form['assessment_id']
                user_id = request.form["user_id"]
                user_role_id = request.form["user_role_id"]
                batch_id = request.form["batch_id"]
                stage_id = request.form["stage_id"]
                file_name = config.bulk_upload_path + str(user_id) + '_'+ str(datetime.now().strftime('%Y%m%d_%H%M%S'))+'_'+f.filename
                f.save(file_name)
    
                df= pd.read_excel(file_name,sheet_name='Template')
                df = df.fillna('')
                df = df.astype(str)
                def check_dob(date_age):
                    try:
                        date_age = str(date_age)
                        return re.match(r"[A-Za-z0-9!@#$%\\&\*\.\,\+-_\s]+",date_age).group()==date_age
                    except:
                        return False

                schema = Schema([
                        #str+null check
                        Column('Enrolment_No',str_validation + null_validation),
                        Column('First_Name',str_validation + null_validation),
                        Column('Middle_Name'),
                        Column('Last_Name'),
                        Column('Batch_Code',null_validation),
                        Column('Assessment_Type',str_validation + null_validation),
                        Column('Assessment_Date',str_validation + null_validation),
                        Column('Attendance(Absent_Present)',str_validation + null_validation),
                        Column('Score',flt_validation),
                        Column('Grade_Result',str_validation + null_validation),
                        Column('Status(Certified_Notcertified)',status_validation),
                        Column('Attempt',null_validation)
                        ])
                errors = schema.validate(df)
                errors_index_rows = [e.row for e in errors]
                len_error = len(errors_index_rows)
                os.remove(file_name)
                if len_error>0:
                    pd.DataFrame({'col':errors}).to_csv(config.bulk_upload_path + 'Error/' + str(user_id) + '_'+ str(datetime.now().strftime('%Y%m%d_%H%M%S'))+'_'+f.filename+'_' + 'errors.csv')
                    return {"Status":False, "message":"Uploaded Failed (fails to validate data)" }
                else:
                    out = Database.upload_assessment_result(df,user_id,assessment_id,batch_id,stage_id)
                    return out
            except Exception as e:
                 return {"Status":False, "message":"Unable to upload " + str(e)}         
api.add_resource(upload_assessment_result,'/upload_assessment_result')

class upload_assessment_certificate_number(Resource):
    @staticmethod
    def post():
        if request.method=='POST':
            try:
                f = request.files['filename']
                user_id = int(session['user_id'])
                assigned_user_id = int(request.form["assigned_user_id"])
                batch_code = str(request.form["batch_code"])
                batch_id = int(request.form["batch_id"])
                enrollment_ids = str(request.form["enrollment_ids"])
                file_name = config.bulk_upload_path + str(user_id) + '_'+ str(datetime.now().strftime('%Y%m%d_%H%M%S'))+'_'+f.filename
                f.save(file_name)
    
                df= pd.read_excel(file_name,sheet_name='Certificate')
                df = df.fillna('')
                df = df.astype(str)
                schema = Schema([
                        #str+null check
                        Column('Enrolment_Id',str_validation + null_validation),
                        Column('Candidate_Name'),
                        Column('Batch_Code',null_validation),
                        Column('Certificate_Number',str_validation + null_validation)
                        ])
                errors = schema.validate(df)
                errors_index_rows = [e.row for e in errors]
                len_error = len(errors_index_rows)
                os.remove(file_name)
                if len_error>0:
                    pd.DataFrame({'col':errors}).to_csv(config.bulk_upload_path + 'Error/' + str(user_id) + '_'+ str(datetime.now().strftime('%Y%m%d_%H%M%S'))+'_'+f.filename+'_' + 'errors.csv')
                    return {"Status":False, "message":"Upload Failed (fails to validate data)" }
                else:
                    out = Database.upload_assessment_certificate_number(df,user_id,assigned_user_id,batch_code,batch_id,enrollment_ids)
                    return out
            except Exception as e:
                 return {"Status":False, "message":"Unable to upload data " + str(e)}         
api.add_resource(upload_assessment_certificate_number,'/upload_assessment_certificate_number')

class UAP_upload_assessment_result(Resource):
    @staticmethod
    def post():
        if request.method=='POST':
            try:
                batch_id=Database.get_batchid_from_batch_code(request.form['batch_id'])
                stage_id = request.form["stage_id"] 
                batch_attempt_number = request.form["batch_attempt_number"]            
                result_json = request.form["result_json"]
                out = Database.UAP_upload_assessment_result(batch_id,stage_id,batch_attempt_number,result_json)
                return out
            except Exception as e:
                 return {"Status":False, "message":"Unable to upload " + str(e)}         
api.add_resource(UAP_upload_assessment_result,'/UAP_upload_assessment_result')

class batch_download_report(Resource):
    report_name = "Trainerwise_TMA_Registration_Compliance"+datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    @staticmethod
    def post():
        if request.method=='POST':
            try:
                #candidate_id, user_id, user_role_id, status, customer, project, sub_project, region, center, center_type
                batch_id = request.form["batch_id"]
                user_id = request.form["user_id"]
                user_role_id = request.form["user_role_id"]
                status = request.form["status"]
                customer_status = request.form["customer_status"]
                
                customer = request.form["customer"]
                project = request.form["project"]
                sub_project = request.form["sub_project"]
                region = request.form["region"]
                center = request.form["center"]
                center_type = request.form["center_type"]
                BU = request.form["BU"]
                BatchCodes = request.form["BatchCodes"]
                Planned_actual = request.form["Planned_actual"]
                StartFromDate = request.form["StartFromDate"]
                StartToDate = request.form["StartToDate"]
                EndFromDate = request.form["EndFromDate"]
                EndToDate = request.form["EndToDate"]
                file_name='batch_report_'+str(user_id) +'_'+ str(datetime.now().strftime('%Y%m%d_%H%M%S'))+'.xlsx'
                #print(candidate_id, user_id, user_role_id, status, customer, project, sub_project, region, center, center_type, file_name)
                resp = batch_report.create_report(batch_id, user_id, user_role_id, status, customer, project, sub_project, region, center, center_type,BU,BatchCodes ,Planned_actual, StartFromDate, StartToDate, EndFromDate, EndToDate, file_name, customer_status)
                return resp
                #return {'FileName':"abc.excel",'FilePath':'lol', 'download_file':''}
            except Exception as e:
                #print(str(e))
                return {"exceptione":str(e)}
api.add_resource(batch_download_report,'/batch_download_report')

class client_download_report(Resource):
    @staticmethod
    def post():
        if request.method=='POST':
            try:
                #candidate_id, user_id, user_role_id, status, customer, project, sub_project, region, center, center_type
                user_id = request.form['user_id'] 
                user_role_id = request.form['user_role_id'] 
                client_id = request.form['client_id']                
                funding_sources = request.form['funding_sources']
                customer_groups = request.form['customer_groups']
                category_type_ids = request.form['category_type_ids']
                is_active = request.form['is_active']
                resp = Report.create_client_report(user_id, user_role_id, client_id, funding_sources, customer_groups, category_type_ids,is_active)
                return resp
                #return {'FileName':"abc.excel",'FilePath':'lol', 'download_file':''}
            except Exception as e:
                print(str(e))
                return {"exceptione":str(e)}
api.add_resource(client_download_report,'/client_download_report')

class contract_download_report(Resource):
    @staticmethod
    def post():
        if request.method=='POST':
            try:
                user_id = request.form['user_id'] 
                user_role_id = request.form['user_role_id'] 
                contract_id = request.form['contract_id']                
                customer_ids = request.form['customer_ids']
                stage_ids = request.form['stage_ids']
                status_id = request.form['status_id']
                from_date = request.form['from_date']
                to_date = request.form['to_date']
                entity_ids = request.form['entity_ids']
                sales_category_ids = request.form['sales_category_ids']
                resp = Report.create_contract_report(user_id, user_role_id, contract_id, customer_ids, stage_ids,status_id, from_date,to_date,entity_ids,sales_category_ids)
                return resp
                #return {'FileName':"abc.excel",'FilePath':'lol', 'download_file':''}
            except Exception as e:
                print(str(e))
                return {"exceptione":str(e)}
api.add_resource(contract_download_report,'/contract_download_report')

class project_download_report(Resource):
    @staticmethod
    def post():
        if request.method=='POST':
            try:
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
                customer_status = request.form['customer_status']                
                resp = Report.create_project_report(user_id,user_role_id,user_region_id,entity,customer,p_group,block,practice,bu,product,status,customer_status)
                return resp
                #return {'FileName':"abc.excel",'FilePath':'lol', 'download_file':''}
            except Exception as e:
                print(str(e))
                return {"exceptione":str(e)}
api.add_resource(project_download_report,'/project_download_report')

class sub_project_download_report(Resource):
    @staticmethod
    def post():
        if request.method=='POST':
            try:
                entity = request.form['entity']
                customer = request.form['customer']
                p_group = request.form['p_group']
                block = request.form['block']
                practice = request.form['practice']
                bu = request.form['bu']
                product = request.form['product']
                status = request.form['status'] 
                customer_status = request.form['customer_status'] 
                           
                user_id = request.form['user_id']
                user_role_id = request.form['user_role_id'] 
                user_region_id = request.form['user_region_id']
                project=request.form['project']                
                resp = Report.create_sub_project_report(user_id,user_role_id,user_region_id,entity,customer,p_group,block,practice,bu,product,status,project,customer_status)
                return resp
                #return {'FileName':"abc.excel",'FilePath':'lol', 'download_file':''}
            except Exception as e:
                print(str(e))
                return {"exceptione":str(e)}
api.add_resource(sub_project_download_report,'/sub_project_download_report')

class download_centers_list(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            center_id = request.form['center_id']
            user_id = request.form['user_id']
            user_role_id = request.form['user_role_id'] 
            user_region_id = request.form['user_region_id'] 
            center_type_ids = request.form['center_type_ids']
            bu_ids = request.form['bu_ids']
            status = request.form['status']
            regions=request.form['regions']
            clusters=request.form['clusters']
            courses=request.form['courses']    
            resp = Report.download_centers_list(center_id, user_id, user_role_id, user_region_id, center_type_ids, bu_ids, status, regions, clusters, courses)
            
            return resp
api.add_resource(download_centers_list,'/download_centers_list')


class download_courses_list(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            user_id=request.form['user_id']
            user_role_id=request.form['user_role_id']
            course_id = request.form['course_id'] 
            sectors = request.form['sectors']
            qps = request.form['qps']
            status = request.form['status'] 
            resp = Report.download_courses_list(user_id, user_role_id, course_id, sectors, qps, status)
            
            return resp
api.add_resource(download_courses_list,'/download_courses_list')

class shiksha_attandance_report(Resource):
    @staticmethod
    def get():
        if request.method == 'GET':
            user_id=request.args.get('user_id',0,type=int)
            user_role_id=request.args.get('user_role_id',0,type=int)
            Customers = request.args.get('Customers','',type=str)
            from_date = request.args.get('from_date','',type=str)
            to_date = request.args.get('to_date','',type=str)
            status_id=request.args.get('status_id',-1,type=int)
            
            resp = Report.shiksha_attandance_report(user_id, user_role_id, Customers, from_date, to_date, status_id)
            return resp
api.add_resource(shiksha_attandance_report,'/shiksha_attandance_report')


class DownloadEmpTimeAllocationTemplate(Resource):
    @staticmethod
    def post():
        if request.method=='POST':
            try:
                user_id = request.form['user_id']
                user_role_id  = request.form['user_role_id']
                
                file_name='Employee_allocation_template_'+str(datetime.now().strftime('%Y%m%d_%H%M%S'))+'.xlsx'
            
                resp = Report.DownloadEmpTimeAllocationTemplate(file_name, user_id, user_role_id)
                return resp
                
            except Exception as e:
                print({"exceptione":str(e)})
api.add_resource(DownloadEmpTimeAllocationTemplate,'/DownloadEmpTimeAllocationTemplate')


class download_users_list(Resource):
    @staticmethod
    def post():
        
        if request.method == 'POST':
            user_id = request.form['user_id']
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
            resp= Report.download_users_list(user_id,filter_role_id,user_region_id,user_role_id, dept_ids, role_ids, entity_ids, region_ids, RM_Role_ids, R_mangager_ids,status_ids,project_ids)
            return resp
api.add_resource(download_users_list,'/download_users_list')

class GetECPReportDonload(Resource):
    @staticmethod
    def post():
        if request.method=='POST':
            #try:
                #candidate_id, user_id, user_role_id, status, customer, project, sub_project, region, center, center_type
            user_id = request.form["user_id"]
            user_role_id = request.form["user_role_id"]
            customer_ids = request.form["customer_ids"]
            contract_ids = request.form["contract_ids"]
            region_ids = request.form["region_ids"]
            from_date = request.form["from_date"]
            to_date = request.form["to_date"]
            stage_ids = request.form["stage_ids"]
            status_id = request.form["status_id"]
            file_name='ecp_report_report_'+str(user_id) +'_'+ str(datetime.now().strftime('%Y%m%d_%H%M%S'))+'.xlsx'
            #print(candidate_id, user_id, user_role_id, status, customer, project, sub_project, region, center, center_type, file_name)
            resp = ecp_report_down.create_report(user_id, user_role_id, customer_ids, contract_ids, region_ids, from_date, to_date,stage_ids,status_id ,file_name)
            return resp
            #return {'FileName':"abc.excel",'FilePath':'lol', 'download_file':''}
            # except Exception as e:
            #     #print(str(e))
            #     return {"exceptione":str(e)}
api.add_resource(GetECPReportDonload,'/GetECPReportDonload')

class batchcandidate_download_report(Resource):
    @staticmethod
    def post():
        if request.method=='POST':
            batch_id = request.form["batch_id"]
            file_name='batch_candidate_report_'+batch_id +'_'+ str(datetime.now().strftime('%Y%m%d_%H%M%S'))+'.xlsx'
            
            resp = batch_candidate_download.create_report(batch_id, file_name)
            return resp
api.add_resource(batchcandidate_download_report,'/batchcandidate_download_report')

#################################################################################################################################
#ECP REPORT PAGE
@app.route("/qp_wise_report_page")
def qp_wise_report_page():
    if g.user:
        return render_template("Reports/qp-wise-report.html")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/qp_wise_report")
def qp_wise_report():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="qp_wise_report_page")
    else:
        return render_template("login.html",error="Session Time Out!!")

class GetQpWiseReportData(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            try:
                user_id=request.args.get('user_id',0,type=int)
                user_role_id=request.args.get('user_role_id',0,type=int)
                customer_ids=request.args.get('customer_ids','',type=str)
                contract_ids=request.args.get('contract_ids','',type=str)
                from_date=request.args.get('from_date','',type=str)
                to_date=request.args.get('to_date','',type=str)

                status_id=request.args.get('status_id','',type=str)
                stage_ids=request.args.get('stage_ids','',type=str)
                response = Report.GetQpWiseReportData(user_id,user_role_id,customer_ids,contract_ids,from_date,to_date, status_id, stage_ids)
                return response 
            except Exception as e:
                return {'exception':str(e)}
api.add_resource(GetQpWiseReportData,'/GetQpWiseReportData')

class GetQpWiseRegionLevelData(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            try:
                user_id=request.args.get('user_id',0,type=int)
                user_role_id=request.args.get('user_role_id',0,type=int)
                customer_ids=request.args.get('customer_ids','',type=str)
                contract_ids=request.args.get('contract_ids','',type=str)
                from_date=request.args.get('from_date','',type=str)
                to_date=request.args.get('to_date','',type=str)
                qp_id=request.args.get('qp_id',0,type=int)
                response = Report.GetQpWiseRegionLevelData(user_id,user_role_id,customer_ids,contract_ids,from_date,to_date,qp_id)
                return response 
            except Exception as e:
                return {'exception':str(e)}
api.add_resource(GetQpWiseRegionLevelData,'/GetQpWiseRegionLevelData')

class GetQpWiseRegionWiseBatchLevelData(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            try:
                user_id=request.args.get('user_id',0,type=int)
                user_role_id=request.args.get('user_role_id',0,type=int)
                customer_ids=request.args.get('customer_ids','',type=str)
                contract_ids=request.args.get('contract_ids','',type=str)
                from_date=request.args.get('from_date','',type=str)
                to_date=request.args.get('to_date','',type=str)
                qp_id=request.args.get('qp_id',0,type=int)
                region_id=request.args.get('region_id',0,type=int)
                response = Report.GetQpWiseRegionWiseBatchLevelData(user_id,user_role_id,customer_ids,contract_ids,from_date,to_date,qp_id,region_id)
                return response 
            except Exception as e:
                return {'exception':str(e)}
api.add_resource(GetQpWiseRegionWiseBatchLevelData,'/GetQpWiseRegionWiseBatchLevelData')

class DownloadBatchReport(Resource):
    @staticmethod
    def post():
        if request.method=='POST':
            user_id = request.form["user_id"]
            user_role_id = request.form["user_role_id"]
            customer_ids = request.form["customer_ids"]
            contract_ids = request.form["contract_ids"]

            status_id=request.args.get('status_id','',type=str)
            stage_ids=request.args.get('stage_ids','',type=str)
            resp = Report.DownloadBatchReport(user_id,user_role_id,customer_ids,contract_ids, status_id, stage_ids)
            return resp

api.add_resource(DownloadBatchReport,'/DownloadBatchReport')
###############################################################################

class GetALLTrainingPartner(Resource):
    @staticmethod
    def get():
        if request.method == 'GET':
            return jsonify(Database.GetALLTrainingPartnerdb())
api.add_resource(GetALLTrainingPartner,'/GetALLTrainingPartner')

class add_external_trainer_details(Resource):
    @staticmethod
    def post():
        try:
            if request.method == 'POST':
                first_name=request.form['FirstName']
                last_name=request.form['LastName']
                email=request.form['Email']
                mobile=request.form['MobileNumber']
                trainer_tyoe=request.form['trainer_tyoe']
                Partner=request.form['Partner']

                is_active=request.form['isactive']
                created_id=g.user_id
                
                return UsersM.add_ex_treiner(first_name, last_name, email, mobile, trainer_tyoe, Partner, is_active, created_id)
        except Exception as e:
            msg={"message":str(e), "UserId": 0}
            return {"PopupMessage": msg}
api.add_resource(add_external_trainer_details,'/add_external_trainer_details')

@app.route("/External_treiner_add_edit")
def External_treiner_add_edit():
    if g.user:
        return render_template("User_Management/externer_trainer-add-edit.html")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/assign_External_treiner_add_edit", methods=['GET','POST'])
def assign_External_treiner_add_edit():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="External_treiner_add_edit")
    else:
        return render_template("login.html",error="Session Time Out!!")



@app.route("/wv")
def web_verification_page():
    name=request.args.get('n','',type=str)
    mobile=request.args.get('m','',type=str)
    otp=request.args.get('o','',type=str)
    response=Database.web_verification(mobile,otp)
    return render_template("web-verification.html",name=name,msg=response['msg'])

class app_email_validation(Resource):
    @staticmethod
    def get():
        if request.method == 'GET':
            client_id = request.args['client_id']
            client_key = request.args['client_key']
            email = request.args['email']
            candidate_id=request.args.get('candidate_id',0,type=int)
            if (client_id==config.API_secret_id) and (client_key==config.API_secret_key):
                if Database.app_email_validation(email,candidate_id):
                    out = {'success': True, 'description': "Email validation successfully"}  
                else:
                    out = {'success': False, 'description': "Email validation failed(already exists)"}
            else:
                out = {'success': False, 'description': "client name and password not matching"}
            return jsonify(out)

api.add_resource(app_email_validation, '/app_email_validation')


#################################################################################################################################
#Batch Status REPORT PAGE
@app.route("/batch_status_report_page")
def batch_status_report_page():
    if g.user:
        return render_template("Reports/batch-status-report.html")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/batch_status_report")
def batch_status_report():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="batch_status_report_page")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/Planned_Actual_Batch_Report_page")
def Planned_Actual_Batch_Report_page():
    if g.user:
        return render_template("Reports/planned_actual_batch_report.html")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/Planned_Actual_Batch_Report")
def Planned_Actual_Batch_Report():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="Planned_Actual_Batch_Report_page")
    else:
        return render_template("login.html",error="Session Time Out!!")

class GetBatchStatusReportDataList(Resource):
    @staticmethod
    def post():
        if request.method=='POST':
            try:
                user_id=request.form['user_id']
                user_role_id=request.form['user_role_id']
                status_id = request.form['status_id']
                customer_ids = request.form['customer_ids']
                stage_ids = request.form['stage_ids']
                contract_ids = request.form['contract_ids']
                
                contract_status = ''
                batch_status = request.form['batch_status']
                from_date = request.form['from_date']
                to_date = request.form['to_date']

                start_index = request.form['start']
                page_length = request.form['length']
                search_value = request.form['search[value]']
                order_by_column_position = request.form['order[0][column]']
                order_by_column_direction = request.form['order[0][dir]']
                draw=request.form['draw']
                response = Report.GetBatchStatusReportDataList(user_id,user_role_id,customer_ids,contract_ids,contract_status,batch_status,from_date,to_date,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw, status_id, stage_ids)
                return response 
            except Exception as e:
                print({'exception':str(e)})
                return {'exception':str(e)}
api.add_resource(GetBatchStatusReportDataList,'/GetBatchStatusReportDataList')

class DownloadBatchStatusReport(Resource):
    @staticmethod
    def post():
        if request.method=='POST':
            user_id = request.form["user_id"]
            user_role_id = request.form["user_role_id"]
            
            status_id = request.form["status_id"]
            customer_ids = request.form["customer_ids"]
            stage_ids = request.form["stage_ids"]
            contract_ids = request.form["contract_ids"]
            contract_status = request.form["contract_status"]
            batch_status = request.form["batch_status"]
            from_date = request.form["from_date"]
            to_date = request.form["to_date"]
            resp = Report.DownloadBatchStatusReport(user_id,user_role_id,customer_ids,contract_ids,contract_status,batch_status,from_date,to_date, status_id, stage_ids)
            return resp

api.add_resource(DownloadBatchStatusReport,'/DownloadBatchStatusReport')
###############################################################################
class GetCenterRooms(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            center_id=request.args.get('center_id',0,type=int)
            response=Master.GetCenerRoom(center_id)
            return response
api.add_resource(GetCenterRooms,'/GetCenterRooms')

class add_edit_center_room(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            try:
                Room_Name=request.form['Room_Name']
                user_id=g.user_id
                is_active=request.form['isactive']
                Room_Type=request.form['Room_Type']
                Room_Size=request.form['Room_Size']
                Room_Capacity=request.form['Room_Capacity']
                center_id=request.form['center_id']
                room_id=request.form['room_id']
                course_ids=request.form['course_ids']
                room_images = request.form['room_images']
                
                out = Master.add_edit_center_room(Room_Name, user_id, is_active, Room_Type, Room_Size, Room_Capacity, center_id, room_id, room_images, course_ids)
            except Exception as e:
                out = {"PopupMessage":{"message":"Error " + str(e), "status":False}}
            finally:
                return out

api.add_resource(add_edit_center_room,'/add_edit_center_room')


class GetUserTargets(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            user_id=request.args.get('user_id',0,type=int)
            response=UsersM.GetUserTargets(user_id)
            return jsonify(response)
api.add_resource(GetUserTargets,'/GetUserTargets')

class AddeEdittUserTarget(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            try:
                created_by=g.user_id
                From_Date=request.form['From_Date']
                To_Date=request.form['To_Date']
                product=request.form['product']
                target=request.form['target']
                is_active=request.form['isactive']
                user_id=request.form['user_id']
                user_target_id=request.form['user_target_id']
                # for i in (created_by, From_Date, To_Date, target, is_active, user_id, user_target_id):
                #     print(i)
                out = UsersM.add_edit_user_targer(created_by, From_Date, To_Date, product, target, is_active, user_id, user_target_id)
            except Exception as e:
                out = {"PopupMessage":{"message":"Error " + str(e), "status":False}}
            finally:
                return out

api.add_resource(AddeEdittUserTarget,'/AddeEdittUserTarget')

class AddeEdittUserAllocation(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            try:
                allocation=request.form['allocation']
                user_id=request.form['user_id']
                mapping_id=request.form['mapping_id']
                out = UsersM.AddeEdittUserAllocation(mapping_id,allocation,user_id)
            except Exception as e:
                out = {"PopupMessage":{"message":"Error " + str(e), "status":0}}
            finally:
                return out

api.add_resource(AddeEdittUserAllocation,'/AddeEdittUserAllocation')

class upload_batch_target_plan(Resource):
    @staticmethod
    def post():
        if request.method=='POST':
            try:
                f = request.files['filename']
                user_id = request.form["user_id"]
                user_role_id = request.form["user_role_id"]
                file_name = config.bulk_upload_path + str(user_id) + '_'+ str(datetime.now().strftime('%Y%m%d_%H%M%S'))+'_'+f.filename
                f.save(file_name)
                df= pd.read_excel(file_name,sheet_name='Template',dtype={'E Planned Start Date': str, 'E Planned End Date': str,'C Planned Date': str,'P Planned Start Date': str, 'P Planned End Date': str})
                df = df.fillna('')
                schema = Schema([
                        #null check
                        Column('Planned Batch Code'),
                        Column('Sub Project Code*',str_validation+null_validation),
                        Column('Sub Project Name*',str_validation+null_validation),
                        Column('Course Code*',str_validation+null_validation),
                        Column('Course Name*',str_validation+null_validation),
                        Column('E Planned Start Date'),
                        Column('E Planned End Date'),
                        Column('E Target'),
                        Column('C Planned Date'),
                        Column('C Target'),
                        Column('P Planned Start Date'),
                        Column('P Planned End Date'),
                        Column('P Target')
                        ])
                errors = schema.validate(df)
                errors_index_rows = [e.row for e in errors]
                len_error = len(errors_index_rows)
                os.remove(file_name)
                if len_error>0:
                    file_name = 'Error_'+str(user_id) + '_'+ str(datetime.now().strftime('%Y%m%d_%H%M%S'))+'.csv'
                    pd.DataFrame({'col':errors}).to_csv(config.bulk_upload_path + 'Error/' + file_name)
                    return {"Status":False, "message":"Validation_Error", "error":"Validation Error <a href='/Bulk Upload/Error/{}' >Download error log</a>".format(file_name) }
                else:
                    df.columns = df.columns.str.replace(" ", "_")
                    df.columns = df.columns.str.replace("*", "")
                    df.insert(0, 'row_index', range(len(df)))
                    out = Database.upload_batch_target_plan(df,user_id,user_role_id)
                    if out['Status']==False:
                        file_name = 'Error_'+str(user_id) + '_'+ str(datetime.now().strftime('%Y%m%d_%H%M%S'))+'.csv'
                        pd.DataFrame(out['data']).to_csv(config.bulk_upload_path + 'Error/' + file_name)
                        return {"Status":False, "message":"Validation_Error", "error":"Validation Error <a href='/Bulk Upload/Error/{}' >Download error log</a>".format(file_name) }
                    else:
                        return out
                
            except Exception as e:
                 return {"Status":False, "message":"Unable to upload " + str(e)}  
             
api.add_resource(upload_batch_target_plan,'/upload_batch_target_plan')

class upload_user(Resource):
    @staticmethod
    def post():
        if request.method=='POST':
            try:
                f = request.files['filename']
                user_id = request.form["user_id"]
                user_role_id = request.form["user_role_id"]
                file_name = config.bulk_upload_path + str(user_id) + '_'+ str(datetime.now().strftime('%Y%m%d_%H%M%S'))+'_'+f.filename
                f.save(file_name)
                df= pd.read_excel(file_name,sheet_name='Template')
                df = df.fillna('')
                schema = Schema([
                        #null check
                        Column('Employee Code*',str_validation+null_validation),
                        Column('Employee Name*',str_validation+null_validation),
                        Column('Employee Email*',str_validation+null_validation),
                        Column('Reporting Manager Employee Code*',str_validation+null_validation),
                        Column('Mobile Number*',str_validation+null_validation),
                        Column('Employee HR Role*',str_validation+null_validation),
                        Column('Region*',str_validation+null_validation),
                        Column('Grade*',str_validation+null_validation),
                        Column('Designation*',str_validation+null_validation),
                        Column('Employment Status*',str_validation+null_validation),
                        Column('Entity*',str_validation+null_validation),
                        Column('Employee Department*',str_validation+null_validation),
                        Column('Active Status*',str_validation+null_validation)
                        ])
                errors = schema.validate(df)
                errors_index_rows = [e.row for e in errors]
                len_error = len(errors_index_rows)
                os.remove(file_name)
                if len_error>0:
                    #print("1")
                    file_name = 'Error_'+str(user_id) + '_'+ str(datetime.now().strftime('%Y%m%d_%H%M%S'))+'.csv'
                    pd.DataFrame({'col':errors}).to_csv(config.bulk_upload_path + 'Error/' + file_name)
                    return {"Status":False, "message":"Validation_Error", "error":"Validation Error <a href='/Bulk Upload/Error/{}' >Download error log</a>".format(file_name) }
                else:
                    #print("2")
                    df.columns = df.columns.str.replace(" ", "_")
                    df.columns = df.columns.str.replace("*", "")
                    df.insert(0, 'row_index', range(len(df)))
                    out = Database.upload_user(df,user_id,user_role_id)
                    if out['Status']==False:
                        file_name = 'Error_'+str(user_id) + '_'+ str(datetime.now().strftime('%Y%m%d_%H%M%S'))+'.csv'
                        pd.DataFrame(out['data']).to_csv(config.bulk_upload_path + 'Error/' + file_name)
                        return {"Status":False, "message":"Validation_Error", "error":"Validation Error <a href='/Bulk Upload/Error/{}' >Download error log</a>".format(file_name) }
                    else:
                        return out
            except Exception as e:
                 #print(e)
                 return {"Status":False, "message":"Unable to upload " + str(e)}  
             
api.add_resource(upload_user,'/upload_user')

class GetSubProjectPlannedBatches(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            sub_project_id=request.args.get('sub_project_id',0,type=int)
            course_id=request.args.get('course_id',0,type=int)
            is_assigned=request.args.get('is_assigned',0,type=int)
            planned_batch_id=request.args.get('planned_batch_id',0,type=int)
            response=Master.GetSubProjectPlannedBatches(sub_project_id,course_id,is_assigned,planned_batch_id)
            return response
api.add_resource(GetSubProjectPlannedBatches,'/GetSubProjectPlannedBatches')



class get_enrolled_candidates_for_multiple_intervention(Resource):
    @staticmethod
    def get():
        if request.method == 'GET':
            client_id = str(request.args['client_id'])
            client_key = str(request.args['client_key'])            
            user_id = request.args.get('user_id',0,type=int)
            candidate_id = request.args.get('candidate_id',0,type=int)
            app_version =request.args.get('app_version',0,type=int)
            cand_name = request.args.get('cand_name','',type=str)
            cand_mobile = request.args.get('cand_mobile','',type=str)
            cand_email = request.args.get('cand_email','',type=str)
            
            if (client_id==config.API_secret_id) and (client_key==config.API_secret_key):
                out = Database.get_enrolled_candidates_for_multiple_intervention(user_id,app_version,cand_name,cand_mobile,cand_email,candidate_id)
                return jsonify(out)
                
            else:
                res = {'success': False, 'description': "client name and password not matching", 'app_status':True}
                return jsonify(res)

api.add_resource(get_enrolled_candidates_for_multiple_intervention, '/get_enrolled_candidates_for_multiple_intervention')

class get_candidate_details(Resource):
    @staticmethod
    def get():
        if request.method == 'GET':
            client_id = str(request.args['client_id'])
            client_key = str(request.args['client_key'])
            user_id = request.args.get('user_id',0,type=int)
            candidate_id = request.args.get('candidate_id',0,type=int)
            if (client_id==config.API_secret_id) and (client_key==config.API_secret_key):
                out = Database.get_candidate_details(user_id,candidate_id)
                return jsonify(out)
            else:
                res = {'success': False, 'description': "client name and password not matching", 'app_status':True}
                return jsonify(res)

api.add_resource(get_candidate_details, '/get_candidate_details')

class All_Course_basedon_rooms(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            try:
                user_id=request.args.get('user_id',0,type=int)
                user_role_id=request.args.get('user_role_id',0,type=int)
                center_id=request.args['center_id']
                room_ids=request.args['room_ids']
                response = Database.AllCourse_basedon_rooms_db(user_id,user_role_id,center_id, room_ids)
                return {'Courses':response}
            except Exception as e:
                return {'exception':str(e)}
api.add_resource(All_Course_basedon_rooms,'/All_Course_basedon_rooms')

#ECP REPORT PAGE
@app.route("/mobilizer_producticity_report_page")
def mobilizer_producticity_report_page():
    if g.user:
        return render_template("Reports/Mobilizer_Productivity_report.html")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/mobilizer_productivity_report")
def mobilizer_producticity_report():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="mobilizer_producticity_report_page")
    else:
        return render_template("login.html",error="Session Time Out!!")

class GetMobilizerReportData(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            try:
                user_id=request.args.get('user_id',0,type=int)
                user_role_id=request.args.get('user_role_id',0,type=int)
                Role=request.args.get('Role','',type=str)
                Date=request.args.get('Date','',type=str)
                #print(user_id,user_role_id,Role, Date)
                response = Report.GetMobilizerReportData(user_id,user_role_id,Role, Date)
                
                return response 
            except Exception as e:
                return {'exception':str(e)}
api.add_resource(GetMobilizerReportData,'/GetMobilizerReportData')

class GetMobilizerReportDownload(Resource):
    @staticmethod
    def post():
        if request.method=='POST':
            #try:
                #candidate_id, user_id, user_role_id, status, customer, project, sub_project, region, center, center_type
            
            user_id = request.form["user_id"]
            user_role_id = request.form["user_role_id"]
            Role = request.form["Role"]
            Date = request.form["Date"]
            
            file_name='Mobilizer_Productivity_Report_'+str(user_id) +'_'+ str(datetime.now().strftime('%Y%m%d_%H%M%S'))+'.xlsx'
            #print(candidate_id, user_id, user_role_id, status, customer, project, sub_project, region, center, center_type, file_name)
            
            resp = mobilizer_report_down.create_report(user_id, user_role_id, Role, Date, file_name)
            
            return resp
            #return {'FileName':"abc.excel",'FilePath':'lol', 'download_file':''}
            # except Exception as e:
            #     #print(str(e))
            #     return {"exceptione":str(e)}
api.add_resource(GetMobilizerReportDownload,'/GetMobilizerReportDownload')

#################################################################################################################################
#OPS Productivity REPORT PAGE
@app.route("/ops_productivity_report_page")
def ops_productivity_report_page():
    if g.user:
        return render_template("Reports/ops-productivity-report.html")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/ops_productivity_report")
def ops_productivity_report():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="ops_productivity_report_page")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/assessment_productivity_report_page")
def assessment_productivity_report_page():
    if g.user:
        return render_template("Reports/assessment-productivity-report.html")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/assessment_productivity_report")
def assessment_productivity_report():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="assessment_productivity_report_page")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/region_productivity_report_page")
def region_productivity_report_page():
    if g.user:
        return render_template("Reports/region_wise_productivity_report.html")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/region_productivity_report")
def region_productivity_report():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="region_productivity_report_page")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/customer_target_report_page")
def customer_target_report_page():
    if g.user:
        return render_template("Reports/customer_wise_target_report.html")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/customer_productivity_report")
def customer_productivity_report():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="customer_target_report_page")
    else:
        return render_template("login.html",error="Session Time Out!!")


class DownloadOpsProductivityReport(Resource):
    @staticmethod
    def post():
        if request.method=='POST':
            month = request.form["month"]
            role_id = request.form["role_id"]
            customer_ids = request.form["customer_ids"]
            contract_ids = request.form["contract_ids"]
            user_id =  session['user_id']
            user_role_id =  session['user_role_id']
            stage_ids =  request.form['stage_ids']
            status_id =  request.form['status_id']
            resp = Report.DownloadOpsProductivityReport(customer_ids,contract_ids,month,role_id,user_id,user_role_id,stage_ids,status_id)
            return resp

api.add_resource(DownloadOpsProductivityReport,'/DownloadOpsProductivityReport')

@app.route("/Employee_wise_report_page")
def Employee_wise_report_page():
    if g.user:
        return render_template("Reports/employee_wise_report_page.html")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/Employee_wise_report")
def Employee_wise_report():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="Employee_wise_report_page")
    else:
        return render_template("login.html",error="Session Time Out!!")

class DownloadEmployeeWiseReport(Resource):
    @staticmethod
    def post():
        if request.method=='POST':
            month = request.form["month"]
            role_id = request.form["role_id"]

            customer_ids = request.form["customer_ids"]
            contract_ids = request.form["contract_ids"]
            stage_ids = request.form["stage_ids"]
            status_id = request.form["status_id"]
            user_id =  session['user_id']
            user_role_id =  session['user_role_id']
            #DownloadEmployeeWiseReport  stage_ids status_id
            resp = Report.DownloadEmployeeWiseReport(customer_ids,contract_ids,month,role_id,user_id,user_role_id,stage_ids, status_id)
            return resp
api.add_resource(DownloadEmployeeWiseReport,'/DownloadEmployeeWiseReport')

class DownloadAssessmentProductivityReport(Resource):
    @staticmethod
    def post():
        if request.method=='POST':
            month = request.form["month"]
            customer_ids = request.form["customer_ids"]
            contract_ids = request.form["contract_ids"]
            project_ids = request.form["project_ids"]
            sub_project_ids = request.form["sub_project_ids"]
            regions = request.form["regions"]
            user_id =  session['user_id']
            user_role_id =  session['user_role_id']

            status_id =request.form["status_id"]
            resp = Report.DownloadAssessmentProductivityReport(customer_ids,contract_ids,project_ids,sub_project_ids,regions,month,user_id,user_role_id,status_id)
            return resp

api.add_resource(DownloadAssessmentProductivityReport,'/DownloadAssessmentProductivityReport')

class DownloadRegionProductivityReport(Resource):
    @staticmethod
    def post():
        if request.method=='POST':
            month = request.form["month"]
            region_ids = request.form["region_ids"]
            customer_ids = request.form["customer_ids"]
            contract_ids = request.form["contract_ids"]
            status_id = request.form["status_id"]
            stage_ids = request.form["stage_ids"]
            user_id =  session['user_id']
            user_role_id =  session['user_role_id']
            resp = Report.DownloadRegionProductivityReport(customer_ids,contract_ids,month,region_ids,user_id,user_role_id, status_id, stage_ids)
            return resp
api.add_resource(DownloadRegionProductivityReport,'/DownloadRegionProductivityReport')

class DownloadCustomerTargetReport(Resource):
    @staticmethod
    def post():
        if request.method=='POST':
            month = request.form["month"]
            region_ids = request.form["region_ids"]
            customer_ids = request.form["customer_ids"]
            contract_ids = request.form["contract_ids"]
            status_id = request.form["status_id"]
            stage_ids = request.form["stage_ids"]

            user_id =  session['user_id']
            user_role_id =  session['user_role_id']
            resp = Report.DownloadCustomerTargetReport(customer_ids,contract_ids,month,region_ids,user_id,user_role_id, status_id, stage_ids)
            return resp

api.add_resource(DownloadCustomerTargetReport,'/DownloadCustomerTargetReport')
###############################################################################
class All_role_user(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            try:
                email_id=request.args.get('email_id','',type=str)
                password=request.args.get('password','',type=str)
                user_id=request.args.get('user_id','',type=str)
                response = Database.All_role_user(email_id,password,user_id)
                #print(email_id,password)
                return response
            except Exception as e:
                return {'exception':str(e)}
api.add_resource(All_role_user,'/All_role_user')

class SetNewUserRole(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            try:
                user_role_id=request.args.get('user_role_id','',type=str)
                user_role_name=request.args.get('user_role_name','',type=str)
                session['user_role_id'] = int(user_role_id)
                session['user_role_name'] = str(user_role_name)
                return {'Status':True,'Description':'Success'}
            except Exception as e:
                return {'Status':False,'Description':'Error: '+str(e)}
api.add_resource(SetNewUserRole,'/SetNewUserRole')

########################################## TMA APIS #########################################
class GetBatchCandidateList(Resource):
    @staticmethod
    def get():
        try:
            if request.method=='GET':
                batch_id = int(request.args['batch_id'])
                session_id = int(request.args['session_id'])
                if batch_id<1:
                    res = {'status':0,'message':'Missing or invalid batch_id'}
                    return jsonify(res)
                
                candidate_list = TMA.GetBatchCandidateList_db(batch_id,session_id)
                res = {'status':1,'message':'Success','candidate_list':candidate_list}
                """
                if candidate_list[0]==False:
                    res = {'status':0, 'message':'No stage found' }
                else:
                    res = {'status':1,'message':'Success','candidate_list':candidate_list}
                """
                return jsonify(res)
        except Exception as e:
            res={'status':-1,'message':'Error : '+ str(e)}
            response=jsonify(res)
            return response
api.add_resource(GetBatchCandidateList, '/GetBatchCandidateList')

class UploadCandidateAttendanceImages(Resource):
    # secret_id = 'L4b0urN3t'
    # secret_key='N304pp5'
    # if (client_id==UploadCandidateAttendanceImages.secret_id) and (client_key==UploadCandidateAttendanceImages.secret_key):
    upload_path = config.tmapath + 'attendance_images/'
    @staticmethod
    def post():
        if request.method == 'POST':
            client_id = str(request.form['client_id'])
            client_key = str(request.form['client_key'])
            if (client_id==config.API_secret_id) and (client_key==config.API_secret_key):
                try:
                    files = request.files.getlist('files[]')
                except Exception as e:
                    res = {'status':0,'message':"unable to read image " + str(e)}
                    return jsonify(res)
                if len(files)==0:
                    res = {'status':0,'message':"Please select atleast one image"}
                    return jsonify(res)
                for file in files:
                    try:
                        name = file.filename
                        file.save(UploadCandidateAttendanceImages.upload_path + name)
                    except Exception as e:
                        res = {'status':0,'message':"uploaded failed " + str(e)}
                        return jsonify(res)
                res = {'status':1,'message':"uploaded succesfully"}
                return jsonify(res)
            else:
                res = {'status':0,'message':"client name and password not matching"}
                return jsonify(res)
        else:
            res = {'status':-1,'message':"Method is wrong"}
            return jsonify(res)
api.add_resource(UploadCandidateAttendanceImages, '/UploadCandidateAttendanceImages')

class UploadTrainerStageImage(Resource):
    upload_path = config.tmapath + 'trainer_stage_images/'
    @staticmethod
    def post():
        if request.method == 'POST':
            client_id = request.form['client_id']
            client_key = request.form['client_key']

            if (client_id==config.API_secret_id) and (client_key==config.API_secret_key):
                try:
                    file = request.files['file']
                    name = file.filename
                except Exception as e:
                    res = {'status':0,'message':"unable to read image " + str(e)}
                    return jsonify(res)
                if file:
                    try:
                        f=open(UploadTrainerStageImage.upload_path + name,'wb')
                        f.write(file.read())
                        f.close()
                        res = {'status':1,'message':"uploaded succesfully"}
                        #res = {'success': True, 'description': "uploaded succesfully"}
                        return jsonify(res)
                    except Exception as e:
                        res = {'status':0,'message':"uploaded failed " + str(e)}
                        #res = {'success': False, 'description': "uploaded failed " + str(e)}
                        return jsonify(res)        
            else:
                res = {'status':0,'message':"client name and password not matching {}, {}".format(client_id, client_key)}
                #res = {'success': False, 'description': "client name and password not matching"}
                return jsonify(res)
        else:
            res = {'status':-1,'message':"wrong method"}
            return jsonify(res)
api.add_resource(UploadTrainerStageImage, '/UploadTrainerStageImage')

class GetSessionPlanModuleDetailsForCourse(Resource):
    @staticmethod
    def get():
        try:
            if request.method=='GET':
                client_id=str(request.args.get("client_id"))
                client_key=str(request.args.get("client_key"))
                if (client_id==config.API_secret_id) and (client_key==config.API_secret_key):
                    course_id=request.args.get("course_id",0,type=int)
                    qp_id=request.args.get("qp_id",0,type=int)
                    session_plan_module_list = TMA.GetSessionPlanModuleDetailsForCourse(course_id,qp_id)
                    if session_plan_module_list!=None:
                        res={'success':True,'description':'Session Plan(s) are available','session_plan_module_list':session_plan_module_list}
                    else:
                        res={'success':False,'description':'NO response from DB'}
                else:
                    res={'success':False,'description':'Invalid Request'}
                response=jsonify(res)
                return response
        except Exception as e:
            res={'success':False,'description':'Error : '+ str(e)}
            response=jsonify(res)
            return response
api.add_resource(GetSessionPlanModuleDetailsForCourse,'/GetSessionPlanModuleDetailsForCourse')

class GetBatchSessionCurrentStageDetails(Resource):
    @staticmethod
    def post():
        try:
            if request.method=='POST':
                batch_id = int(request.form['batch_id'])
                session_id = int(request.form['session_id'])
                user_id = int(request.form['user_id'])
                if batch_id<1:
                    res = {'status':0,'message':'Missing or invalid batch_id'}
                    return jsonify(res)
                if session_id<1:
                    res = {'status':0,'message':'Missing or invalid session_id'}
                    return jsonify(res)
                current_stage = TMA.GetBatchSessionCurrentStageDetails(batch_id,session_id,user_id)
                #print(current_stage)
                if current_stage ==None:
                    res = {'status':0, 'message':'No stage found' }
                else:
                    res = {'status':1,'message':'Success','user_id':user_id,'batch_id':batch_id,'session_id':session_id,'stage_id':current_stage}
                return jsonify(res)
        except Exception as e:
            res={'status':-1,'message':'Error : '+ str(e)}
            response=jsonify(res)
            return response
api.add_resource(GetBatchSessionCurrentStageDetails, '/GetBatchSessionCurrentStageDetails')

class GetBatchList(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            response=None
            try:
                #app_version_details=Database.GetAppVersionDetails()
                #BatchStatusId UserId CenterId role_id  app_version 
                BatchStatusId=request.args.get('batch_stage_id',2,type=int)
                UserId=request.args.get('user_id',0,type=int)
                CenterId=request.args.get('center_id',0,type=int)
                role_id = request.args.get('role_id',0,type=int)
                app_version = request.args.get('app_version',0,type=str)
                if UserId == 0:
                    res={'status':0,'message':'Invalid User Id','app_status':True}
                    response=jsonify(res)
                    return response
                res = TMA.GetBatchListForTMA(BatchStatusId,UserId,CenterId,role_id,app_version)
                response=jsonify(res)
                return response
            except Exception as e:
                res={'status':-1,'message':'Error : '+ str(e),'app_status':True}
                response=jsonify(res)
                return response
api.add_resource(GetBatchList,'/GetBatchList')

class GetBatchSessionList(Resource):
    @staticmethod
    def get():
        try:
            if request.method=='GET':
                BatchId=request.args.get('batch_id',0,type=int)
                UserId=request.args.get('user_id',0,type=int)
                SessionPlanId=request.args.get('session_plan_id',0,type=int)
                ModuleId=request.args.get('module_id',0,type=int)
                StatusId=request.args.get('status_id',0,type=int)
                SessionName=request.args.get('session_name','')
                app_version = request.args.get('app_version',0,type=str)
                if UserId == 0:
                    res={'status':0,'message':'Invalid User Id','app_status':True}
                    response=jsonify(res)
                    return response
                res = TMA.GetBatchSessionListForTMA(BatchId,UserId,SessionPlanId,ModuleId,StatusId,SessionName,app_version)
                response=jsonify(res)
                return response
        except Exception as e:
            res={'status':-1,'message':'Error : '+ str(e),'app_status':True}
            response=jsonify(res)
            return response
api.add_resource(GetBatchSessionList,'/GetBatchSessionList')

class LogTrainerStageDetails(Resource):
    @staticmethod
    def post():
        try:
            if request.method=='POST':
                session_id = str(request.form['session_id'])
                user_id = int(request.form['user_id'])
                batch_id = int(request.form['batch_id'])
                stage_id = int(request.form['stage_id'])
                latitude = request.form['latitude']
                longitude = request.form['longitude']
                image_file_name = request.form['image_file_name']
                mark_candidate_attendance = int(request.form['mark_candidate_attendance'])
                attendance_data = request.form['attendance_data']
                group_attendance_image_data = request.form['group_attendance_image_data']
                app_version = request.form['app_version']

                if batch_id<1:
                    res = {'status':0,'message':'Missing or invalid batch_id','app_status':True}
                    return jsonify(res)
                if session_id=='':
                    res = {'status':0,'message':'Missing or invalid session_id','app_status':True}
                    return jsonify(res)
                if (stage_id<1 or stage_id>4):
                    res = {'status':0,'message':'Missing or invalid stage_id','app_status':True}
                    return jsonify(res)
                res = TMA.LogTrainerStageDetails(session_id,user_id,batch_id,stage_id,latitude,longitude,image_file_name,mark_candidate_attendance,attendance_data,group_attendance_image_data,app_version)
                response=jsonify(res)
                return response
        except Exception as e:
            res={'status':-1,'message':'Error : '+ str(e),'app_status':True}
            response=jsonify(res)
            return response
api.add_resource(LogTrainerStageDetails,'/LogTrainerStageDetails')

class GetSubProjectsForRegionUser(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            user_id=request.args.get('user_id',0,type=int)
            user_role_id=request.args.get('user_role_id',0,type=int)
            region_id=request.args.get('region_id','',type=str)
            response={"SubProjects":Master.GetSubProjectsForRegionUser(user_id,user_role_id,region_id)}
            return response
api.add_resource(GetSubProjectsForRegionUser,'/GetSubProjectsForRegionUser')

class GetCoursesBasedOnSubProjects(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            sub_project_ids=request.args.get('sub_project_ids','',type=str)
            #print('hi')
            #print(sub_project_ids)
            response={"Courses":Master.GetCoursesBasedOnSubProjects(sub_project_ids)}
            return response
api.add_resource(GetCoursesBasedOnSubProjects,'/GetCoursesBasedOnSubProjects')

class trainers_based_on_sub_projects(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            sub_project_ids=request.form['sub_project_ids']
            return Batch.AllTrainersOnSubProjects(sub_project_ids)
api.add_resource(trainers_based_on_sub_projects,'/trainers_based_on_sub_projects')

class app_get_release_date_msg(Resource):
    @staticmethod
    def get():
        if request.method == 'GET':
            try:
                client_id = request.args['client_id']
                client_key = request.args['client_key']
                if (client_id==config.API_secret_id) and (client_key==config.API_secret_key):
                    out=Database.app_get_release_date_msg()                        
                else:
                    out = {'success': False, 'description': "client name and password not matching"}
                return jsonify(out)
            except Exception as e:
                return {'success': False, 'description': "Error! "+str(e)} 

api.add_resource(app_get_release_date_msg, '/app_get_release_date_msg')

class GetSubProjectsForCustomer(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            customer_ids=request.args.get('customer_ids','',type=str)
            response={"SubProjects":TMA.GetSubProjectsForCustomer(customer_ids)}
            return response
api.add_resource(GetSubProjectsForCustomer,'/GetSubProjectsForCustomer')

class SyncShikshaAttendanceData(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            response=Master.SyncShikshaAttendanceData()
            return response
api.add_resource(SyncShikshaAttendanceData,'/SyncShikshaAttendanceData')

class SyncShikshaCandidateData(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            response=Master.SyncShikshaCandidateData()
            return response
api.add_resource(SyncShikshaCandidateData,'/SyncShikshaCandidateData')

class SyncWeeklyUserSubProjectAllocation(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            response=Master.SyncWeeklyUserSubProjectAllocation()
            return response
api.add_resource(SyncWeeklyUserSubProjectAllocation,'/SyncWeeklyUserSubProjectAllocation')

class SendShikshaCandidateEnrolmentMail(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            response=Master.SendShikshaCandidateEnrolmentMail()
            return response
api.add_resource(SendShikshaCandidateEnrolmentMail,'/SendShikshaCandidateEnrolmentMail')

class SendPulishAssessmentMailEACP(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            print("x")
            #response=Master.SendPulishAssessmentMailEACP()
            
api.add_resource(SendPulishAssessmentMailEACP,'/SendPulishAssessmentMailEACP')

################################### SL4 report
@app.route("/SL4Report_page")
def SL4Report_page():
    if g.user:
        return render_template("Reports/SL4Report.html")
    else:
        return redirect("/")

@app.route("/SL4Report")
def SL4Report():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="SL4Report_page")
    else:
        return render_template("login.html",error="Session Time Out!!")

class updated_new_SL4Report(Resource):
    @staticmethod
    def post():
        if request.method=='POST':
            try:
                user_id = request.form['user_id']
                user_role_id  = request.form['user_role_id']
                from_date = request.form["from_date"]
                to_date = request.form["to_date"]
                Customers = request.form["Customers"]
                projects = request.form["projects"]
                sub_projects = request.form["sub_projects"]
                status_id = request.form["status_id"]
                
                report_name = "Customer_wise_MIS_report_"+str(datetime.now().strftime('%Y%m%d_%H%M%S'))+'.xlsx'
                resp = SL4Report_filter_new.create_report(from_date, to_date, Customers,projects,sub_projects, user_id, user_role_id, report_name, status_id)
                return resp
                
            except Exception as e:
                return {"exceptione":str(e)}
api.add_resource(updated_new_SL4Report,'/updated_new_SL4Report')


@app.route("/candidate_data_page")
def candidate_data_page():
    if g.user:
        return render_template("Reports/candidate-data.html")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/candidate_data")
def candidate_data():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="candidate_data_page")
    else:
        return render_template("login.html",error="Session Time Out!!")


@app.route("/shiksha_attendance_page")
def shiksha_attendance_page():
    if g.user:
        return render_template("Reports/shiksha_attendance.html")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/shiksha_attendance")
def shiksha_attendance():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="shiksha_attendance_page")
    else:
        return render_template("login.html",error="Session Time Out!!")


############################## nation wise report 
@app.route("/NationalReport_page")
def NationalReport_page():
    if g.user:
        return render_template("Reports/Nation wise report.html")
    else:
        return redirect("/")

@app.route("/NationalReport")
def NationalReport():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="NationalReport_page")
    else:
        return render_template("login.html",error="Session Time Out!!")

class updated_new_NationalReport(Resource):
    @staticmethod
    def post():
        if request.method=='POST':
            try:
                user_id = request.form['user_id']
                user_role_id  = request.form['user_role_id']
                month = request.form["month"]
                Customers = request.form["Customers"]
                
                report_name = "Naton_Wise_Report_"+str(datetime.now().strftime('%Y%m%d_%H%M%S'))+'.xlsx'
                resp = Naton_Wise_Report.create_report(month, Customers, user_id, user_role_id, report_name)
                return resp
                
            except Exception as e:
                return {"exceptione":str(e)}
api.add_resource(updated_new_NationalReport,'/updated_new_NationalReport')

############################## Trainer Productivity report 
@app.route("/TrainerProductivityReport_page")
def TrainerProductivityReport_page():
    if g.user:
        return render_template("Reports/Trainer_Productivity_report.html")
    else:
        return redirect("/")

@app.route("/TrainerProductivityReport")
def TrainerProductivityReport():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="TrainerProductivityReport_page")
    else:
        return render_template("login.html",error="Session Time Out!!")

class download_TrainerProductivityReport(Resource):
    @staticmethod
    def post():
        if request.method=='POST':
            try:     
                user_id = request.form['user_id']
                user_role_id  = request.form['user_role_id']
                region_ids = request.form['region_ids']
                t_status  = request.form['t_status']
                trainer_ids = request.form['trainer_ids']
                from_date = request.form['from_date']
                to_date  = request.form['to_date']
                
                report_name = "Trainer_Productivity_Report_"+str(datetime.now().strftime('%Y%m%d_%H%M%S'))+'.xlsx'
                resp = trainer_prodctivity_report.create_report(user_id, user_role_id, region_ids, t_status, trainer_ids, from_date, to_date, report_name)
                return resp
                
            except Exception as e:
                return {"exceptione":str(e)}
api.add_resource(download_TrainerProductivityReport,'/download_TrainerProductivityReport')

class AllTrainerBasedOnUserRegions(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            response=[]
            try:
                RegionIds=request.args.get('RegionIds','',type=str)
                status=request.args.get('status','',type=str)
                UserId=request.args.get('user_id',0,type=int)
                UserRoleId=request.args.get('user_role_id',0,type=int)
                #print((RegionIds, status, UserId,UserRoleId))
                response=Database.AllTrainerBasedOnUserRegions(RegionIds, status, UserId,UserRoleId)
                return {'Trainer':response}
            except Exception as e:
                return {'exception':str(e)}

api.add_resource(AllTrainerBasedOnUserRegions,'/AllTrainerBasedOnUserRegions')

class GetCustomerSpoc(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            customer_id=request.args.get('customer_id',0,type=int)
            response={"SPOC":Master.GetCustomerSpoc(customer_id)}
            return response
api.add_resource(GetCustomerSpoc,'/GetCustomerSpoc')

class download_candidate_data(Resource):
    @staticmethod
    def post():
        if request.method=='POST':
            try:
                #candidate_id, user_id, user_role_id, status, customer, project, sub_project, region, center, center_type
                candidate_id = request.form["candidate_id"]
                user_id = request.form["user_id"]
                user_role_id = request.form["user_role_id"]
                project_types = request.form["project_types"]
                customer = request.form["customer"]
                project = request.form["project"]
                sub_project = request.form["sub_project"]
                batch = request.form["batch"]
                region = request.form["region"]
                center = request.form["center"]
                created_by = request.form["created_by"]
                Contracts = request.form["Contracts"]
                candidate_stage = request.form["candidate_stage"]
                from_date = request.form["from_date"]
                to_date = request.form["to_date"]
                status_id = request.form["status_id"]
                stage_ids = request.form["stage_ids"]
                
                resp = Report.DownloadCandidateData(candidate_id, user_id, user_role_id, project_types, customer, project, sub_project, batch, region, center, created_by, Contracts, candidate_stage, from_date, to_date, status_id, stage_ids)
                
                return resp
            except Exception as e:
                return {"exceptione":str(e)}
api.add_resource(download_candidate_data,'/download_candidate_data')

class GetPOCForCustomer(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            customer_id=request.args.get('customer_id',0,type=int)
            response={"POC":Master.GetPOCForCustomer(customer_id)}
            return response
api.add_resource(GetPOCForCustomer,'/GetPOCForCustomer')

class download_Project_list(Resource):
    @staticmethod
    def post():
        if request.method=='POST':
            try:  
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
                
                #Master.project_list(user_id,user_role_id,user_region_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw,entity,customer,p_group,block,practice,bu,product,status)
                report_name = "Project_List_"+str(datetime.now().strftime('%Y%m%d_%H%M%S'))+'.xlsx'
                resp = Report.project_list_report(user_id,user_role_id,user_region_id,entity,customer,p_group,block,practice,bu,product,status,report_name)
                
                return resp
                
            except Exception as e:
                return {"exceptione":str(e)}
api.add_resource(download_Project_list,'/download_Project_list')

class download_sub_project_list(Resource):
    @staticmethod
    def post():
        if request.method=='POST':
            try:  
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
                project=request.form['project']

                #Master.sub_project_list(user_id,user_role_id,user_region_id,start_index,page_length,search_value,order_by_column_position,order_by_column_direction,draw,entity,customer,p_group,block,practice,bu,product,status,project)
                report_name = "Sub_Project_List_"+str(datetime.now().strftime('%Y%m%d_%H%M%S'))+'.xlsx'
                resp = Report.sub_project_list_report(user_id,user_role_id,user_region_id,entity,customer,p_group,block,practice,bu,product,status,project,report_name)
                
                return resp
                
            except Exception as e:
                return {"exceptione":str(e)}
api.add_resource(download_sub_project_list,'/download_sub_project_list')

class GetDocumentForExcel(Resource):
    @staticmethod
    def get():
        # data/TMA/attendance_images/IMG_652_5156_1598957384498.jpg
        if request.method=='GET':
            image_name=request.args.get('image_name','',type=str)
            image_path=request.args.get('image_path','',type=str)
            path = config.neo_report_file_path + 'data/TMA/' + image_path
            filename = '{}/{}'.format(path,image_name)
            if os.path.exists(filename):
                filename = config.Base_URL + '/data/TMA/' + image_path +'/{}'.format(image_name)
            else:
                path = config.aws_location + 'tms/' + image_path +'/' + image_name
                URL = config.COL_URL + 's3_signed_url_for_file_updated'
                PARAMS = {'file_path':path} 
                r = requests.get(url = URL, params = PARAMS) 
                if r.text !='':
                    filename = r.text
                else:
                    filename = config.Base_URL + '/data/No-image-found.jpg' # no image found
            return redirect(filename)
api.add_resource(GetDocumentForExcel,'/GetDocumentForExcel')

class GetDocumentForExcel_S3_certiplate(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            image_name=request.args.get('image_name','',type=str)
            image_path=request.args.get('image_path','',type=str)

            URL=config.neo_certiplate+image_name
            path = config.aws_location +'neo_app/images/'+image_name
            if image_path!='':
                URL = config.neo_certiplate_def + 'doc' + '/'+ image_name
                path = config.aws_location +'neo_app/'+ image_path + '/'+image_name
            r = requests.get(url = URL) 
            if r.status_code==200:
                filename =  URL
            elif r.status_code==404:
                #path = config.aws_location +'neo_app/images/'+image_name
                URL = config.COL_URL + 's3_signed_url_for_file_updated'
                PARAMS = {'file_path':path} 
                r = requests.get(url = URL, params = PARAMS)
                if r.text !='':
                    filename = r.text
                else:
                    filename = ''
            else:
                filename=''
            if filename =='':
                filename= config.Base_URL + '/data/No-image-found.jpg'
            #return(filename)
            return redirect(filename)
api.add_resource(GetDocumentForExcel_S3_certiplate,'/GetDocumentForExcel_S3_certiplate')

class GetQP_basedon_Sector(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            sector_ids=request.args.get('sector_ids','',type=str)
            return Content.get_qp_for_sector(sector_ids)
api.add_resource(GetQP_basedon_Sector,'/GetQP_basedon_Sector')

class GetAllParentCourse(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            return Content.GetAllParentCourse()
api.add_resource(GetAllParentCourse,'/GetAllParentCourse')

@app.route("/reupload_candidate_image")
def reupload_candidate_image():
    if g.user:
        return render_template("Candidate/reupload_images.html",candidate_id=g.candidate_id,candidate_stage_id=g.candidate_stage_id)
    else:
        return render_template("login.html",error="Session Time Out!!")

## Reupload candidate images
@app.route("/Reupload_Candidate_Images_Web", methods=['GET','POST'])
def Reupload_Candidate_Images_Web():
    session['candidate_id']=request.form['hdn_candidate_id']
    session['candidate_stage_id']=request.form['hdn_candidate_stage_id']
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="reupload_candidate_image")
    else:
        return render_template("login.html",error="Session Time Out!!")

class AllCandidateImages(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            try:
                UserId=request.args.get('user_id',0,type=int)
                UserRoleId=request.args.get('user_role_id',0,type=int)
                candidate_id=request.args.get('candidate_id',0,type=int)
                return Candidate.get_allcandidate_images(UserId,UserRoleId,candidate_id)
            except Exception as e:
                return {'exception':str(e)}
api.add_resource(AllCandidateImages,'/AllCandidateImages')

class ReuploadCandidateImageById(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            try:
                UserId=request.args.get('user_id',0,type=int)
                UserRoleId=request.args.get('user_role_id',0,type=int)
                id=request.args.get('id',0,type=int)
                return Candidate.get_allcandidate_images(UserId,UserRoleId,candidate_id)
            except Exception as e:
                return {'exception':str(e)}
api.add_resource(ReuploadCandidateImageById,'/ReuploadCandidateImageById')

class reupload_candidate_image_web_ui(Resource):
    @staticmethod
    def post():
        if request.method=='POST':
            try:  
                user_id = request.form['user_id']
                user_role_id = request.form['user_role_id'] 
                filename = request.form['filename']
                c_id = request.form['id']
                candidate_id = request.form['candidate_id']
                return Candidate.reupload_candidate_image_web_ui(user_id,user_role_id,filename,c_id,candidate_id)
            except Exception as e:
                out = {'Status': False, 'message': "Error : "+str(e)}
                return out
api.add_resource(reupload_candidate_image_web_ui,'/reupload_candidate_image_web_ui')

@app.route("/after_popup_reload_image")
def after_popup_reload_image():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="reupload_candidate_image")
    else:
        return render_template("login.html",error="Session Time Out!!")
@app.route("/certification_page")
def certification_page():
    if g.user:
        status=request.args.get('status',-1,type=int)
        return render_template("Assessment/certification-batch-list.html", status=status)
    else:
        return render_template("login.html",error="Session Time Out!!")


@app.route("/certification")
def certification():
    if g.user:
        status=request.args.get('status',-1,type=int) 
        html_str="certification_page?status=" + str(status)
        return render_template("home.html",values=g.User_detail_with_ids,html=html_str)
    else:
        return render_template("login.html",error="Session Time Out!!")

class GetOJTBatchCurrentStageDetails(Resource):
    @staticmethod
    def get():
        try:
            if request.method=='GET':
                user_id=request.args.get('user_id',0,type=int)
                batch_id=request.args.get('batch_id',0,type=int)
                user_role_id=request.args.get('user_role_id',0,type=int)
                client_id=request.args.get('client_id','',type=str)
                client_key=request.args.get('client_key','',type=str)
                
                if (client_id==config.API_secret_id) and (client_key==config.API_secret_key):
                    if batch_id<1:
                        res = {'status':0,'message':'Missing or invalid batch_id'}
                        return jsonify(res)
                    
                    current_stage = Database.GetOJTBatchCurrentStageDetails(batch_id,user_id,user_role_id)
                    if current_stage ==None:
                        res = {'status':0, 'message':'No stage found' }
                    else:
                        res = {'status':1,'message':'Success','user_id':user_id,'batch_id':batch_id,'stage_id':current_stage}
                else:
                    res = {'status':0, 'message':'Invalid client credentials'}
            else:
                res = {'status':0, 'message':'Invalid Method'}
            return jsonify(res)  

        except Exception as e:
            res={'status':-1,'message':'Error : '+ str(e)}
            return jsonify(res)
api.add_resource(GetOJTBatchCurrentStageDetails, '/GetOJTBatchCurrentStageDetails')

class LogOJTStageDetails(Resource):
    @staticmethod
    def post():
        try:
            if request.method=='POST':
                client_id = request.form['client_id']
                client_key = request.form['client_key']
                user_id = int(request.form['user_id'])
                user_role_id = int(request.form['user_role_id'])
                batch_id = int(request.form['batch_id'])
                stage_id = int(request.form['stage_id'])
                latitude = request.form['latitude']
                longitude = request.form['longitude']
                timestamp = request.form['timestamp']
                filename = request.form['filename']

                app_version = request.form['app_version']
                device_model = request.form['device_model']
                imei_num = request.form['imei_num']
                android_version = request.form['android_version']
                
                if (client_id==config.API_secret_id) and (client_key==config.API_secret_key):
                    if batch_id<1:
                        res = {'success': False, 'description': "Missing or invalid batch_id", 'app_status':True}
                        return jsonify(res)
                    if (stage_id<1 or stage_id>3):
                        res = {'success': False, 'description':'Missing or invalid stage_id','app_status':True}
                        return jsonify(res)

                    res = Database.LogOBJStageDetails(user_id, batch_id, stage_id, latitude, longitude, timestamp, filename, app_version, device_model, imei_num, android_version)
                else:
                    res = {'success': False, 'description':'Invalid client credentials','app_status':True}
            else:
                res = {'success': False, 'description':'Invalid Method','app_status':True}
            return jsonify(res)
                    
        except Exception as e:
            res = {'success': False, 'description':'Error : '+ str(e),'app_status':True}
            #res={'status':-1,'message':'Error : '+ str(e),'app_status':True}
            response=jsonify(res)
            return response
api.add_resource(LogOJTStageDetails,'/LogOJTStageDetails')

class Upload_OJT_file(Resource):
    #upload_path = config.tmapath + 'trainer_stage_images/'
    @staticmethod
    def post():
        if request.method == 'POST':
            client_id = request.form['client_id']
            client_key = request.form['client_key']
            if (client_id==config.API_secret_id) and (client_key==config.API_secret_key):
                try:
                    file = request.files['file']
                    name = file.filename
                    file_format = name.split('.')[-1]
                except Exception as e:
                    res = {'success': False, 'description': "Unable to read file "}
                    #res = {'status':0,'message':"unable to read image " + str(e)}
                    return jsonify(res)
                if file:
                    try:
                        upload_path = ''
                        if file_format.lower()=='mp3':
                            upload_path = config.neo_report_file_path + 'data/OJT/audio/'
                        elif (file_format.lower() in ['gif', 'jpeg', 'png', 'jpg']):
                            upload_path = config.neo_report_file_path + 'data/OJT/images/'
                        else:
                            #res = {'status':0,'message':"Invalid file Format"}
                            res = {'success': False, 'description': "Invalid file Format "}
                            return jsonify(res)
                        file.save(upload_path + name)
                        
                        #res = {'status':1,'message':"uploaded succesfully"}
                        res = {'success': True, 'description': "uploaded succesfully"}
                        return jsonify(res)
                    except Exception as e:
                        #res = {'status':0,'message':"uploaded failed " + str(e)}
                        res = {'success': False, 'description': "uploaded failed " + str(e)}
                        return jsonify(res) 
                else:
                    res = {'success': False, 'description': "Please select a file "}
                    return jsonify(res) 
            else:
                #res = {'status':0,'message':"client name and password not matching {}, {}".format(client_id, client_key)}
                res = {'success':False,'description':"client name and password not matching {}, {}".format(client_id, client_key)}
                return jsonify(res)
        else:
            res = {'success':False,'description':"wrong method"}
            return jsonify(res)
api.add_resource(Upload_OJT_file, '/Upload_OJT_file')

#ECP REPORT PAGE
@app.route("/OJT_report_page")
def OJT_report_page():
    if g.user:
        return render_template("Reports/OJT-report.html")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/OJT_report")
def OJT_report():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="OJT_report_page")
    else:
        return render_template("login.html",error="Session Time Out!!")

class GetsubprojectbyCustomer(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            try:
                user_id=request.args.get('user_id',0,type=int)
                user_role_id=request.args.get('user_role_id',0,type=int)
                customer_id=request.args.get('customer_id','',type=str)
                response = Database.GetsubprojectbyCustomer(user_id, user_role_id, customer_id)
                return {'sub_projects':response}
            except Exception as e:
                return {'exception':str(e)}
api.add_resource(GetsubprojectbyCustomer,'/GetsubprojectbyCustomer')

class download_ojt_report(Resource):
    @staticmethod
    def post():
        if request.method=='POST':
            try:
                user_id = request.form['user_id']
                user_role_id  = request.form['user_role_id']
                customer_ids = request.form["customer_ids"]
                sub_project_ids = request.form["sub_project_ids"]
                course_ids = request.form["course_ids"]
                batch_code =request.form["batch_code"]
                date_stage = request.form["date_stage"]
                BatchStartFromDate = request.form["BatchStartFromDate"]
                BatchStartToDate = request.form["BatchStartToDate"]
                BatchEndFromDate = request.form["BatchEndFromDate"]
                BatchEndToDate = request.form["BatchEndToDate"]
                OJTStartFromDate = request.form["OJTStartFromDate"]
                OJTStartToDate = request.form["OJTStartToDate"]
                OJTEndFromDate = request.form["OJTEndFromDate"]
                OJTEndToDate = request.form["OJTEndToDate"]
            
                file_name='OJT_Monitoring_Report_'+str(datetime.now().strftime('%Y%m%d_%H%M%S'))+'.xlsx'
            
                resp = Report.download_ojt_report(file_name, user_id, user_role_id, customer_ids, sub_project_ids, course_ids, batch_code, date_stage, BatchStartFromDate,BatchStartToDate,BatchEndFromDate,BatchEndToDate,OJTStartFromDate,OJTStartToDate,OJTEndFromDate,OJTEndToDate)
                return resp
                
            except Exception as e:
                print({"exceptione":str(e)})
api.add_resource(download_ojt_report,'/download_ojt_report')


class GetSessionsForCourse(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            try:
                CourseId=request.args.get('CourseId',0,type=int)
                response = Master.GetSessionsForCourse(CourseId)
                return response
            except Exception as e:
                return {'exception':str(e)}
api.add_resource(GetSessionsForCourse,'/GetSessionsForCourse')

class GetPartnerCenters(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            partner_id=request.args.get('partner_id',0,type=int)
            response=Master.GetPartnerCenters(partner_id)
            return response
api.add_resource(GetPartnerCenters,'/GetPartnerCenters')



class download_emp_target_template(Resource):
    @staticmethod
    def post():
        if request.method=='POST':
            try:
                user_id = request.form['user_id']
                user_role_id  = request.form['user_role_id']
                date = request.form["date"]
                
                file_name='Employee_target_template_'+str(datetime.now().strftime('%Y%m%d_%H%M%S'))+'.xlsx'
            
                resp = Report.download_emp_target_template(file_name, user_id, user_role_id, date)
                return resp
                
            except Exception as e:
                print({"exceptione":str(e)})
api.add_resource(download_emp_target_template,'/download_emp_target_template')

class upload_employee_target_plan(Resource):
    @staticmethod
    def post():
        if request.method=='POST':
            try:
                f = request.files['myFileemp']
                user_id = request.form["user_id"]
                user_role_id = request.form["user_role_id"]
                Month_Year = request.form["month_year"]
                
                Month_Year_excel = datetime.strptime(Month_Year, '%Y-%m-%d').strftime('%b-%Y').upper()
                month_year_validation = [CustomElementValidation(lambda d: datetime.strptime(d, '%b-%Y').strftime('%Y-%m-%d')==Month_Year, "only '{}' date allowed".format(Month_Year_excel))]

                file_name = config.bulk_upload_path + str(user_id) + '_'+ str(datetime.now().strftime('%Y%m%d_%H%M%S'))+'_'+f.filename
                f.save(file_name)
                df= pd.read_excel(file_name,sheet_name='Employee Target') #,dtype={'E Planned Start Date': str, 'E Planned End Date': str,'C Planned Date': str,'P Planned Start Date': str, 'P Planned End Date': str}
                df = df.fillna('')

                schema = Schema([
                        Column('Employee Code(NE)',str_validation+null_validation),
                        Column('Employee name(NE)',str_validation+null_validation),
                        Column('NEO Role(NE)',str_validation+null_validation),
                        Column('Sub Project Code(NE)',str_validation+null_validation),
                        Column('Sub Project Name(NE)',null_validation),
                        Column('Month & Year*',month_year_validation+str_validation+null_validation),

                        Column('Week 1 Registration',int_validation+null_validation),
                        Column('Week 2 Registration',int_validation+null_validation),
                        Column('Week 3 Registration',int_validation+null_validation),
                        Column('Week 4 Registration',int_validation+null_validation),
                        Column('Week 1 Enrollment',int_validation+null_validation),
                        Column('Week 2 Enrollment',int_validation+null_validation),
                        Column('Week 3 Enrollment',int_validation+null_validation),
                        Column('Week 4 Enrollment',int_validation+null_validation),
                        Column('Week 1 Assessment',int_validation+null_validation),
                        Column('Week 2 Assessment',int_validation+null_validation),
                        Column('Week 3 Assessment',int_validation+null_validation),
                        Column('Week 4 Assessment',int_validation+null_validation),
                        Column('Week 1 Certification',int_validation+null_validation),
                        Column('Week 2 Certification',int_validation+null_validation),
                        Column('Week 3 Certification',int_validation+null_validation),
                        Column('Week 4 Certification',int_validation+null_validation),
                        Column('Week 1 Certification Distribution',int_validation+null_validation),
                        Column('Week 2 Certification Distribution',int_validation+null_validation),
                        Column('Week 3 Certification Distribution',int_validation+null_validation),
                        Column('Week 4 Certification Distribution',int_validation+null_validation),
                        Column('Week 1 Placement',int_validation+null_validation),
                        Column('Week 2 Placement',int_validation+null_validation),
                        Column('Week 3 Placement',int_validation+null_validation),
                        Column('Week 4 Placement',int_validation+null_validation)

                        ])
                errors = schema.validate(df)
                errors_index_rows = [e.row for e in errors]
                len_error = len(errors_index_rows)
                os.remove(file_name)
                if len_error>0:
                    file_name = 'Error_'+str(user_id) + '_'+ str(datetime.now().strftime('%Y%m%d_%H%M%S'))+'.csv'
                    pd.DataFrame({'col':errors}).to_csv(config.bulk_upload_path + 'Error/' + file_name)
                    return {"Status":False, "message":"Validation_Error", "error":"Validation Error <a href='/Bulk Upload/Error/{}' >Download error log</a>".format(file_name) }
                else:
                    df.columns = df.columns.str.replace(" ", "_")
                    df.columns = df.columns.str.replace("*", "")
                    df.columns = df.columns.str.replace("(", "_")
                    df.columns = df.columns.str.replace(")", "")
                    df.columns = df.columns.str.replace("&", "")
                    df = df.drop_duplicates()
                    df.insert(0, 'row_index', range(len(df)))

                    col = ['row_index', 'Employee_Code_NE', 'Employee_name_NE', 'NEO_Role_NE', 'Sub_Project_Code_NE', 'Month__Year', 'Week_1_Registration', 'Week_2_Registration', 'Week_3_Registration',
                            'Week_4_Registration', 'Week_1_Enrollment', 'Week_2_Enrollment', 'Week_3_Enrollment', 'Week_4_Enrollment', 'Week_1_Assessment', 'Week_2_Assessment', 'Week_3_Assessment', 'Week_4_Assessment', 
                            'Week_1_Certification', 'Week_2_Certification', 'Week_3_Certification', 'Week_4_Certification', 'Week_1_Certification_Distribution', 'Week_2_Certification_Distribution', 'Week_3_Certification_Distribution',
                            'Week_4_Certification_Distribution', 'Week_1_Placement', 'Week_2_Placement', 'Week_3_Placement', 'Week_4_Placement']
                    df = df[col]
                    
                    out = Database.upload_employee_target_plan(df,user_id,user_role_id)
                    return out
            except Exception as e:
                 return {"Status":False, "message":"Unable to upload " + str(e)}            
api.add_resource(upload_employee_target_plan,'/upload_employee_target_plan')

class upload_employee_allocation_plan(Resource):
    @staticmethod
    def post():
        if request.method=='POST':
            try:
                f = request.files['myFileemp']
                user_id = request.form["user_id"]
                user_role_id = request.form["user_role_id"]
                #time_regex='/^(100(\.00?)?|[1-9]?\d(\.\d\d?)?)$/'
                #Month_Year_excel = datetime.strptime(Month_Year, '%Y-%m-%d').strftime('%b-%Y').upper()
                #month_year_validation = [CustomElementValidation(lambda d: datetime.strptime(d, '%b-%Y').strftime('%Y-%m-%d')==Month_Year, "only '{}' date allowed".format(Month_Year_excel))]
                #time_validation = [CustomElementValidation(lambda d: (re.search(time_regex,d)!=None), 'Inavalid time format. Please provide correct allocation time')]

                file_name = config.bulk_upload_path + str(user_id) + '_'+ str(datetime.now().strftime('%Y%m%d_%H%M%S'))+'_'+f.filename
                f.save(file_name)
                df= pd.read_excel(file_name,sheet_name='Employee Allocation') #,dtype={'E Planned Start Date': str, 'E Planned End Date': str,'C Planned Date': str,'P Planned Start Date': str, 'P Planned End Date': str}
                df = df.fillna('')

                schema = Schema([
                        Column('Employee Code',str_validation+null_validation),
                        Column('Employee Name',str_validation+null_validation),
                        Column('Sub Project Code',str_validation+null_validation),
                        Column('Sub Project Name',null_validation),
                        
                        Column('Allocation(In Percentage)',null_validation),
                       
                        ])
                errors = schema.validate(df)
                errors_index_rows = [e.row for e in errors]
                len_error = len(errors_index_rows)
                os.remove(file_name)
                if len_error>0:
                    file_name = 'Error_'+str(user_id) + '_'+ str(datetime.now().strftime('%Y%m%d_%H%M%S'))+'.csv'
                    pd.DataFrame({'col':errors}).to_csv(config.bulk_upload_path + 'Error/' + file_name)
                    return {"Status":False, "message":"Validation_Error", "error":"Validation Error <a href='/Bulk Upload/Error/{}' >Download error log</a>".format(file_name) }
                else:
                    df.columns = df.columns.str.replace(" ", "_")
                    df.columns = df.columns.str.replace("*", "")
                    df.columns = df.columns.str.replace("(", "_")
                    df.columns = df.columns.str.replace(")", "")
                    df.columns = df.columns.str.replace("&", "")
                    #df.columns = df.columns.str.replace("::", "_")
                    df = df.drop_duplicates()
                    df.insert(0, 'row_index', range(len(df)))

                    col = ['Employee_Code', 'Employee_Name', 'Sub_Project_Code','Sub_Project_Name', 'Allocation_In_Percentage']
                    df = df[col]
                    
                    out = Database.upload_employee_allocation_plan(df,user_id,user_role_id)
                    return out
            except Exception as e:
                print('Exc'+str(e))
                return {"Status":False, "message":"Unable to upload " + str(e)}            
api.add_resource(upload_employee_allocation_plan,'/upload_employee_allocation_plan')
@app.route("/Assessment_report_page")
def Assessment_report_page():
    if g.user:
        return render_template("Reports/Assessment_Report.html")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/Assessment_report")
def Assessment_report():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="Assessment_report_page")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/Certification_Distribution_Report_page")
def Certification_Distribution_Report_page():
    if g.user:
        return render_template("Reports/Certification_Distribution_Report.html")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/Certification_Distribution_Report")
def Certification_Distribution_Report():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="Certification_Distribution_Report_page")
    else:
        return render_template("login.html",error="Session Time Out!!")

class download_Assessment_report(Resource):
    @staticmethod
    def post():
        if request.method=='POST':
            try:
                user_id=request.form['user_id']
                user_role_id=request.form['user_role_id']
                
                customer = request.form['customer']
                project = request.form['project']
                sub_project = request.form['sub_project']
                region = request.form['region']
                centers = request.form['centers']
                Batches = request.form['Batches']
                FromDate = request.form['FromDate']
                ToDate = request.form['ToDate']
                status_id = request.form['status_id']
                file_name='Assessment_Report_'+str(datetime.now().strftime('%Y%m%d_%H%M%S'))+'.xlsx'
            
                resp = Report.download_Assessment_report(file_name,user_id,user_role_id,customer,project,sub_project,region,centers,Batches,FromDate,ToDate, status_id)
                return resp
                
            except Exception as e:
                return({"exceptione":str(e)})
api.add_resource(download_Assessment_report,'/download_Assessment_report')

class download_Certification_Distribution_Report(Resource):
    @staticmethod
    def post():
        if request.method=='POST':
            try:
                user_id=request.form['user_id']
                user_role_id=request.form['user_role_id']
                
                customer = request.form['customer']
                project = request.form['project']
                sub_project = request.form['sub_project']
                region = request.form['region']
                centers = request.form['centers']
                Batches = request.form['Batches']
                FromDate = request.form['FromDate']
                ToDate = request.form['ToDate']
                status_id = request.form['status_id']

                file_name='Certification_Distribution_Report_'+str(datetime.now().strftime('%Y%m%d_%H%M%S'))+'.xlsx'
            
                resp = Report.download_Certification_Distribution_Report(file_name,user_id,user_role_id,customer,project,sub_project,region,centers,Batches,FromDate,ToDate,status_id)
                return resp
                
            except Exception as e:
                return({"exceptione":str(e)})
api.add_resource(download_Certification_Distribution_Report,'/download_Certification_Distribution_Report')

@app.route("/Certification_Distribution_productivity_report_page")
def Certification_Distribution_productivity_report_page():
    if g.user:
        return render_template("Reports/Certification_Distribution_Productivity_Report.html")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/Certification_Distribution_productivity_report")
def Certification_Distribution_productivity_report():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="Certification_Distribution_productivity_report_page")
    else:
        return render_template("login.html",error="Session Time Out!!")

class DownloadCertification_DistributionProductivityReport(Resource):
    @staticmethod
    def post():
        if request.method=='POST':
            month = request.form["month"]
            status_id = request.form["status_id"]
            customer_ids = request.form["customer_ids"]
            project_ids = request.form["project_ids"]
            sub_project_ids = request.form["sub_project_ids"]
            regions = request.form["regions"]
            
            user_id =  session['user_id']
            user_role_id =  session['user_role_id']
            resp = Report.DownloadCertificate_distributionProductivityReport(month, customer_ids, project_ids, sub_project_ids, regions, user_id, user_role_id, status_id)
            return resp
api.add_resource(DownloadCertification_DistributionProductivityReport,'/DownloadCertification_DistributionProductivityReport')

class download_Partner_Target_dump(Resource):
    @staticmethod
    def post():
        if request.method=='POST':
            try:  
                user_id = request.form['user_id']
                user_role_id = request.form['user_role_id'] 
                user_region_id = request.form['user_region_id']
                
                report_name = "Partner_Target_Dump_"+str(datetime.now().strftime('%Y%m%d_%H%M%S'))+'.xlsx'
                resp = Report.download_Partner_Target_dump(user_id,user_role_id,user_region_id,report_name)
                
                return resp
                
            except Exception as e:
                return {"exceptione":str(e)}
api.add_resource(download_Partner_Target_dump,'/download_Partner_Target_dump')

class upload_partner_target_plan(Resource):
    @staticmethod
    def post():
        if request.method=='POST':
            try:
                f = request.files['filename']
                user_id = request.form["user_id"]
                user_role_id = request.form["user_role_id"]
                file_name = config.bulk_upload_path + str(user_id) + '_'+ str(datetime.now().strftime('%Y%m%d_%H%M%S'))+'_'+f.filename
                f.save(file_name)
                
                d = ['E Planned Start Date', 'E Planned End Date', 'A Planned Date', 'Certification distribution date', 'P Planned Start Date', 'P Planned End Date']
                dtype_dict = dict.fromkeys(d,str)

                df= pd.read_excel(file_name,sheet_name='Template',dtype=dtype_dict)
                df = df.fillna('')
                os.remove(file_name)

                schema = Schema([
                        #null check
                        Column('Partner/Vendor code*'),

                        Column('Partner/Vendor name*',str_validation+null_validation),
                        Column('Sub Project Code*',str_validation+null_validation),
                        Column('Sub Project Name*',str_validation+null_validation),
                        Column('Course Code*',str_validation+null_validation),
                        Column('Course Name*',str_validation+null_validation),

                        Column('E Planned Start Date',str_validation+null_validation),
                        Column('E Planned End Date',str_validation+null_validation),
                        Column('E Target',str_validation+null_validation),
                        Column('A Planned Date',str_validation+null_validation),
                        Column('A Target',str_validation+null_validation),
                        Column('Certification distribution date',str_validation+null_validation),
                        Column('CD Target',str_validation+null_validation),
                        Column('P Planned Start Date',str_validation+null_validation),
                        Column('P Planned End Date',str_validation+null_validation),
                        Column('P Target',str_validation+null_validation)
                        ])
                errors = schema.validate(df)
                errors_index_rows = [e.row for e in errors]
                len_error = len(errors_index_rows)
                # os.remove(file_name)
                if len_error>0:
                    file_name = 'Error_'+str(user_id) + '_'+ str(datetime.now().strftime('%Y%m%d_%H%M%S'))+'.csv'
                    pd.DataFrame({'col':errors}).to_csv(config.bulk_upload_path + 'Error/' + file_name)
                    return {"Status":False, "message":"Validation_Error", "error":"Validation Error <a href='/Bulk Upload/Error/{}' >Download error log</a>".format(file_name) }
                else:
                    df.columns = df.columns.str.replace(" ", "_")
                    df.columns = df.columns.str.replace("*", "")
                    df.columns = df.columns.str.replace('/','_')
                    df.columns = df.columns.str.replace(' ','_')

                    df.insert(0, 'row_index', range(len(df)))

                    out = Database.upload_partner_target_plan(df,user_id,user_role_id)
                    if out['Status']==False:
                        file_name = 'Error_'+str(user_id) + '_'+ str(datetime.now().strftime('%Y%m%d_%H%M%S'))+'.csv'
                        pd.DataFrame(out['data']).to_csv(config.bulk_upload_path + 'Error/' + file_name)
                        return {"Status":False, "message":"Validation_Error", "error":"Validation Error <a href='/Bulk Upload/Error/{}' >Download error log</a>".format(file_name) }
                    else:
                        return out
            except Exception as e:
                return {"Status":False, "message":"Unable to upload " + str(e)}
api.add_resource(upload_partner_target_plan,'/upload_partner_target_plan')

@app.route("/partner_productivity_report_page")
def partner_productivity_report_page():
    if g.user:
        return render_template("Reports/partner_productivity_report.html")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/partner_productivity_report")
def partner_productivity_report():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="partner_productivity_report_page")
    else:
        return render_template("login.html",error="Session Time Out!!")

class DownloadPartnerProductivityReport(Resource):
    @staticmethod
    def post():
        if request.method=='POST':
            month = request.form["month"]
            partner_ids = request.form["partner_ids"]
            customer_ids = request.form["customer_ids"]
            #contract_ids = request.form["contract_ids"]
            project_ids = request.form["project_ids"]
            sub_project_ids = request.form["sub_project_ids"]
            
            user_id =  session['user_id']
            user_role_id =  session['user_role_id']
            resp = Report.DownloadPartnerProductivityReport(partner_ids,customer_ids,project_ids,sub_project_ids,month,user_id,user_role_id)
            return resp
api.add_resource(DownloadPartnerProductivityReport,'/DownloadPartnerProductivityReport')

class SaveRmInfo(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            client_id = str(request.form['client_id'])
            client_key = str(request.form['client_key'])
            user_id = int(request.form['user_id'])
            batch_id = int(request.form['batch_id'])
            
            CompanyName = str(request.form['CompanyName'])
            Address = str(request.form['Address'])
            RMName = str(request.form['RMName'])
            RMmobilenumber = str(request.form['RMmobilenumber'])
            RMemailid = str(request.form['RMemailid'])
            
            if (client_id==config.API_secret_id) and (client_key==config.API_secret_key):
                try:
                    out = Database.SaveRmInfo(user_id, batch_id, CompanyName, Address, RMName, RMmobilenumber, RMemailid)
                except Exception as e:
                    out = {'success': False, 'description': "Error : "+str(e), 'app_status':True}
                finally:
                    return jsonify(out)
            else:
                res = {'success': False, 'description': "client name and password not matching", 'app_status':True}
                return jsonify(res)
api.add_resource(SaveRmInfo, '/SaveRmInfo')

class get_OJT_History(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            try:
                user_id=request.args.get('user_id',0,type=int)
                batch_id=request.args.get('batch_id',0,type=int)
                client_id=request.args.get('client_id','',type=str)
                client_key=request.args.get('client_key','',type=str)
                if (client_id==config.API_secret_id) and (client_key==config.API_secret_key):
                    res = Database.get_OJT_History(user_id, batch_id)
                else:
                    res = {'success': False, 'description': "client name and password not matching", 'app_status':True}
                return jsonify(res)
            except Exception as e:
                return {'success': False, 'description': "Error : "+str(e), 'app_status':True}
api.add_resource(get_OJT_History,'/get_OJT_History')

class Sync_UserSubProjectCF_TargetData(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            now = datetime.now()
            y = int(now.strftime('%Y'))
            m = int(now.strftime('%m'))

            mon = ['DEC','JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV']
            date = lambda m,y : mon[m%12]+'-'+str(y)
            c_my = date(m,y)
            p_my = date(m-1,y-1 if m==1 else y)

            response=Master.Sync_UserSubProjectCF_TargetData(c_my, p_my)
            return response
api.add_resource(Sync_UserSubProjectCF_TargetData,'/Sync_UserSubProjectCF_TargetData')


class add_center_attachment_session(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            #UserId, UserRoleId, CenterId, FromDate, ToDate, Agreement_Type, Commercial_Agreement_Type, OtherRemark
            UserId = int(request.form['UserId'])
            UserRoleId = int(request.form['UserRoleId'])
            CenterId = int(request.form['CenterId'])
            FromDate = str(request.form['FromDate'])
            ToDate = str(request.form['ToDate'])
            Agreement_Type = int(request.form['Agreement_Type'])
            Commercial_Agreement_Type = int(request.form['Commercial_Agreement_Type'])
            OtherRemark = str(request.form['OtherRemark'])
            value = str(request.form['value'])

            try:
                out = Database.add_center_attachment_session(UserId, UserRoleId, CenterId, FromDate, ToDate, Agreement_Type, Commercial_Agreement_Type, OtherRemark, value)
            except Exception as e:
                out = {'Status': False, 'Message': "Error : "+str(e)}
            finally:
                return jsonify(out)
api.add_resource(add_center_attachment_session, '/add_center_attachment_session')

class get_center_attachment_session(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            try:
                CenterId=request.args.get('CenterId','',type=str)
                res = Database.get_center_attachment_session(CenterId)
                return jsonify(res)
            except Exception as e:
                return jsonify({"Status":False,'Message':"Error : "+str(e)})
api.add_resource(get_center_attachment_session,'/get_center_attachment_session')

class get_map_attachment_session(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            try:
                SessionId=request.args.get('SessionId','',type=str)
                res = Database.get_map_attachment_session(SessionId)
                return jsonify(res)
            except Exception as e:
                return jsonify({"Status":False,'Message':"Error : "+str(e)})
api.add_resource(get_map_attachment_session,'/get_map_attachment_session')

class remove_map_attachment_session(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            try:
                session_attachment_id=request.args.get('session_attachment_id','',type=str)
                #print('session_attachment_id' + session_attachment_id)
                out = Database.remove_map_attachment_session(session_attachment_id)   
            except Exception as e:
                out = {'Status': False, 'Message': "Error : "+str(e)}
            finally:
                return jsonify(out)
api.add_resource(remove_map_attachment_session,'/remove_map_attachment_session')

class upload_center_attachment(Resource):
    @staticmethod
    def post():
        if request.method=='POST':
            try:  
                user_id = request.form['user_id']
                user_role_id = request.form['user_role_id'] 
                filename = request.form['filename']
                session_id = request.form['session_id']
                return Master.upload_center_attachment(user_id,user_role_id,filename,session_id)
            except Exception as e:
                out = {'Status': False, 'message': "Error : "+str(e)}
                return out
api.add_resource(upload_center_attachment,'/upload_center_attachment')

class GetDocumentForExcel_S3(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            image_name=request.args.get('image_name','',type=str)
            image_path=request.args.get('image_path','',type=str)

            path = config.aws_location + image_path + '/'+image_name
            URL = config.COL_URL + 's3_signed_url_for_file_updated'
            PARAMS = {'file_path':path} 
            r = requests.get(url = URL, params = PARAMS)
            if r.text !='':
                filename = r.text
            else:
                filename = ''
            if filename =='':
                filename= config.Base_URL + '/data/No-image-found.jpg'
            return redirect(filename)
api.add_resource(GetDocumentForExcel_S3,'/GetDocumentForExcel_S3')

class GetPartnerContract(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            partner_id=request.args.get('partner_id',0,type=int)
            response=Master.GetPartnerContract(partner_id)
            return response
api.add_resource(GetPartnerContract,'/GetPartnerContract')

class GetTrainerProfile(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            trainer_id=request.args.get('trainer_id',0,type=int)
            response=Master.GetTrainerProfile(trainer_id)
            return response
api.add_resource(GetTrainerProfile,'/GetTrainerProfile')
class add_edit_trainer_profile(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            #Contract_Name, ContractCode, StartDate, EndDate, filename, PartnerId, JSON, is_active, user_id, PartnerContractId

            certificate_name=request.form['certificate_name']
            sector_id=request.form['sector_id']
            start_date=request.form['start_date']
            end_date=request.form['end_date']
            filename=request.form['filename']
            trainer_id=request.form['trainer_id']
            is_active=request.form['is_active']
            trainer_profile_id=request.form['trainer_profile_id']
            user_id=g.user_id
            
            return Master.add_edit_trainer_profile(certificate_name, sector_id, start_date, end_date, filename, trainer_id, is_active, user_id, trainer_profile_id)
api.add_resource(add_edit_trainer_profile,'/add_edit_trainer_profile')

class add_edit_partner_contract(Resource):
    @staticmethod
    def post():
        if request.method == 'POST':
            #Contract_Name, ContractCode, StartDate, EndDate, filename, PartnerId, JSON, is_active, user_id, PartnerContractId

            Contract_Name=request.form['Contract_Name']
            ContractCode=request.form['ContractCode']
            StartDate=request.form['StartDate']
            EndDate=request.form['EndDate']
            filename=request.form['filename']
            PartnerId=request.form['PartnerId']
            JSON=request.form['JSON']
            is_active=request.form['is_active']
            PartnerContractId=request.form['PartnerContractId']
            user_id=g.user_id
            
            return Master.add_edit_partner_contract(Contract_Name, ContractCode, StartDate, EndDate, filename, PartnerId, JSON, is_active, user_id, PartnerContractId)
api.add_resource(add_edit_partner_contract,'/add_edit_partner_contract')
class GetSingleTrainerProfile(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            trainer_profile_id=request.args.get('trainer_profile_id',0,type=int)
            response=Master.GetSingleTrainerProfile(trainer_profile_id)
            return response
api.add_resource(GetSingleTrainerProfile,'/GetSingleTrainerProfile')
class GetPartnerContractMilestones(Resource):
    @staticmethod
    def get():
        if request.method=='GET':
            Partner_Contract_Id=request.args.get('Partner_Contract_Id',0,type=int)
            response=Master.GetPartnerContractMilestones(Partner_Contract_Id)
            return response
api.add_resource(GetPartnerContractMilestones,'/GetPartnerContractMilestones')

@app.route("/revenue_report_page")
def revenue_report_page():
    if g.user:
        return render_template("Reports/Revenue Report.html")
    else:
        return render_template("login.html",error="Session Time Out!!")

@app.route("/revenue_report")
def revenue_report():
    if g.user:
        return render_template("home.html",values=g.User_detail_with_ids,html="revenue_report_page")
    else:
        return render_template("login.html",error="Session Time Out!!")


class DownloadRevenueReport(Resource):
    @staticmethod
    def post():
        if request.method=='POST':
            month = request.form["month"]
            role_id = request.form["role_id"]
            customer_ids = request.form["customer_ids"]
            contract_ids = request.form["contract_ids"]
            user_id =  session['user_id']
            user_role_id =  session['user_role_id']
            stage_ids =  request.form['stage_ids']
            status_id =  request.form['status_id']
            resp = Report.DownloadRevenueReport(customer_ids,contract_ids,month,role_id,user_id,user_role_id,stage_ids,status_id)
            return resp
api.add_resource(DownloadRevenueReport,'/DownloadRevenueReport')


if __name__ == '__main__':
    app.run(host=config.app_host, port=int(config.app_port), debug=True)
